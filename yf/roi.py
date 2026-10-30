"""Parameterized ROI model. Refuses to run while required mechanics are null.

Everything here is arithmetic on numbers YOU put in config/mechanics.yaml from
the docs. No defaults are assumed for any game mechanic.
"""
from __future__ import annotations
from dataclasses import dataclass


class MissingMechanics(Exception):
    pass


def _req(d: dict, path: str):
    cur = d
    for k in path.split("."):
        if not isinstance(cur, dict) or k not in cur or cur[k] is None:
            raise MissingMechanics(f"mechanics.yaml: '{path}' is null — answer the matching "
                                   f"question in docs/04_OPEN_QUESTIONS.md first")
        cur = cur[k]
    return cur


@dataclass
class SeedResult:
    name: str
    cost_yield: float
    harvest_yield: float
    grow_hours: float
    net_per_cycle_yield: float
    cycles_per_day: float
    daily_roi_pct: float
    payback_days: float | None


def seed_roi(mech: dict, fert_mult: float = 1.0, yield_eth: float | None = None,
             price_haircut: float = 0.0) -> list[SeedResult]:
    """Per-seed ROI in $YIELD terms. `price_haircut` (0..1) shrinks harvest
    value to stress-test token price decay between plant and sell."""
    seeds = _req(mech, "seeds")
    if not seeds:
        raise MissingMechanics("mechanics.yaml: 'seeds' is empty (Q8)")
    out = []
    for s in seeds:
        for k in ("name", "cost_yield", "grow_hours", "harvest_yield"):
            if s.get(k) is None:
                raise MissingMechanics(f"seed '{s.get('name')}' missing '{k}' (Q8)")
        harvest = s["harvest_yield"] * fert_mult * (1 - price_haircut)
        net = harvest - s["cost_yield"]
        cpd = 24.0 / s["grow_hours"] if s["grow_hours"] > 0 else 0
        daily_roi = (net / s["cost_yield"] * 100 * cpd) if s["cost_yield"] else float("inf")
        payback = (1 / (daily_roi / 100)) if daily_roi > 0 else None
        out.append(SeedResult(s["name"], s["cost_yield"], harvest, s["grow_hours"], net, cpd,
                              daily_roi, payback))
    return sorted(out, key=lambda r: -r.daily_roi_pct)


@dataclass
class DeedResult:
    tier: str
    multiplier: float
    output_per_day: float
    gross_yield_per_day: float
    upkeep_yield_per_day: float
    net_yield_per_day: float
    net_eth_per_day: float | None
    payback_days_at_floor: float | None
    annualized_pct_on_floor: float | None


def deed_roi(mech: dict, floor_eth: float, yield_eth: float | None, tier: str | None = None,
             gas_eth_per_claim: float = 0.0) -> DeedResult:
    """Deed-loop coupon: output × Fert price − upkeep − gas, vs the floor."""
    tiers = _req(mech, "deed.tiers")
    tier = tier or _req(mech, "deed.owner_tier")
    if tier not in tiers or tiers[tier].get("multiplier") is None:
        raise MissingMechanics(f"deed.tiers['{tier}'].multiplier is null (Q1-2)")
    mult = float(tiers[tier]["multiplier"])
    out_cycle = float(_req(mech, "deed.output_per_cycle")) * mult
    cycle_h = float(_req(mech, "deed.cycle_hours"))
    cpd = 24.0 / cycle_h if cycle_h > 0 else 0
    out_day = out_cycle * cpd
    if _req(mech, "deed.pays_yield_directly"):
        gross = out_day
    else:
        gross = out_day * float(_req(mech, "fert.price_yield"))
    upkeep = float(mech["deed"].get("upkeep_per_cycle") or 0) * cpd
    claims_per_day = cpd if mech["deed"].get("action_required") else 0
    net_yield = gross - upkeep
    net_eth = None
    payback = annual = None
    if yield_eth is not None:
        net_eth = net_yield * yield_eth - claims_per_day * gas_eth_per_claim
        if net_eth > 0:
            payback = floor_eth / net_eth
            annual = net_eth * 365 / floor_eth * 100
    return DeedResult(tier, mult, out_day, gross, upkeep, net_yield, net_eth, payback, annual)


def allocate(budget_usd: float, reserve_pct: float = 25.0, seed_first_usd: float = 1500.0,
             max_extra_deeds: int = 2, floor_usd: float | None = None) -> dict:
    """Rule set R1–R3 from docs/02_STRATEGY_FRAMEWORK.md expressed as numbers."""
    reserve = budget_usd * reserve_pct / 100
    seeds = min(seed_first_usd, budget_usd - reserve)
    remaining = budget_usd - reserve - seeds
    deeds = 0
    deed_spend = 0.0
    if floor_usd:
        deeds = min(max_extra_deeds, int(remaining // floor_usd))
        deed_spend = deeds * floor_usd
    return {"reserve_usd": reserve, "seed_tranche_usd": seeds, "extra_deeds": deeds,
            "deed_spend_usd": deed_spend,
            "undeployed_usd": budget_usd - reserve - seeds - deed_spend}


def tier_relative_value(tiers: dict, base: str = "Common") -> dict:
    """Market-implied vs docs-stated tier value.

    For each tier: price_ratio = floor / base floor; util_ratio = multiplier /
    base multiplier (None until docs fill multipliers); score = util / price.
    score > 1 → tier is cheap relative to its stated utility; < 1 → expensive.
    """
    b = tiers[base]
    out = {}
    for name, t in tiers.items():
        pr = (t["floor_eth"] / b["floor_eth"]) if t.get("floor_eth") and b.get("floor_eth") else None
        scarcity = b["count"] / t["count"] if t.get("count") else None
        ur = None
        if t.get("multiplier") is not None and b.get("multiplier"):
            ur = t["multiplier"] / b["multiplier"]
        out[name] = {"floor_eth": t.get("floor_eth"), "price_ratio": pr, "scarcity_ratio": scarcity,
                     "util_ratio": ur, "score": (ur / pr) if (ur and pr) else None}
    return out


def swap_breakeven(sell_tier: dict, buy_tier: dict, n_sell: int, fee_pct: float = 7.5) -> dict:
    """Selling n deeds of one tier to buy another: how many you get and the
    utility multiple the bought tier must carry to break even on output."""
    proceeds = n_sell * sell_tier["floor_eth"] * (1 - fee_pct / 100)
    n_buy = int(proceeds // buy_tier["floor_eth"])
    leftover = proceeds - n_buy * buy_tier["floor_eth"]
    req = (n_sell * sell_tier.get("multiplier", 1) / n_buy) if n_buy else None
    return {"proceeds_eth": proceeds, "n_buy": n_buy, "leftover_eth": leftover,
            "required_multiplier_ratio": req}
