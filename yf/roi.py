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
    seeds = mech.get("seeds")
    if isinstance(seeds, dict):          # docs-shaped block: per-seed list lives under seeds.list
        seeds = seeds.get("list")
    if not seeds:
        raise MissingMechanics("mechanics.yaml: 'seeds.list' is empty — pack prices/odds are redacted until farming opens")
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


def swap_breakeven(sell_tier: dict, buy_tier: dict, n_sell: int, fee_pct: float = 6.0) -> dict:
    """Selling n deeds of one tier to buy another: how many you get and the
    utility multiple the bought tier must carry to break even on output."""
    proceeds = n_sell * sell_tier["floor_eth"] * (1 - fee_pct / 100)
    n_buy = int(proceeds // buy_tier["floor_eth"])
    leftover = proceeds - n_buy * buy_tier["floor_eth"]
    req = (n_sell * sell_tier.get("multiplier", 1) / n_buy) if n_buy else None
    return {"proceeds_eth": proceeds, "n_buy": n_buy, "leftover_eth": leftover,
            "required_multiplier_ratio": req}


def seed_pack_ev(pack_price_eth: float, rarities: dict, payout_pct: float, dues_pct: float = 0.0) -> dict:
    """Expected ETH back per pack. rarities = {name: {p: prob, worth_x: multiple of pack price}}.
    payout_pct = Broker (ETH) or Farmer ($YIELD) payout % of crop value. All inputs from the docs
    once published; refuses on nulls."""
    tot_p = 0.0; ev_x = 0.0
    for name, r in rarities.items():
        if r.get("p") is None or r.get("worth_x") is None:
            raise MissingMechanics(f"seeds.rarities['{name}'] p/worth_x is null (Q8) — farming not yet live")
        tot_p += r["p"]; ev_x += r["p"] * r["worth_x"]
    if abs(tot_p - 1.0) > 1e-6 and abs(tot_p - 100.0) > 1e-6:
        raise ValueError("rarity probabilities must sum to 1 (or 100)")
    if tot_p > 1.5:
        ev_x /= 100.0
    gross = ev_x * pack_price_eth
    net = gross * payout_pct / 100 * (1 - dues_pct / 100)
    return {"ev_crop_value_eth": gross, "ev_payout_eth": net, "ev_ratio": net / pack_price_eth,
            "house_edge_pct": (1 - net / pack_price_eth) * 100}


def burn_vs_sell(root_cellar_eth: float, silo_yield: float, windfall_pct: float, yield_eth: float,
                 tier_floor_eth: float, fee_pct: float = 6.0, rebuild_eth: float = 0.01) -> dict:
    """Burn pays Root Cellar (ETH) + Windfall (share of Silo, in $YIELD). Sell pays floor net of fees
    (and requires unstaking, which destroys the Fert Deck). Positive edge → burn."""
    burn = root_cellar_eth + silo_yield * windfall_pct / 100 * yield_eth
    sell = tier_floor_eth * (1 - fee_pct / 100)
    return {"burn_value_eth": burn, "sell_value_eth": sell, "burn_minus_sell_eth": burn - sell,
            "burn_if": burn > sell}


def fert_deed_yield(fert_units_per_day: float, fert_price_eth: float, tier_floor_eth: float,
                    fertility: int, base_fertility: int = 5, royalty_pct: float = 5.0,
                    opensea_fee_pct: float = 1.0, gas_eth_per_claim: float = 0.0,
                    claims_per_day: float = 1 / 2.5) -> dict:
    """Stage One coupon: Fert Deck output sold on OpenSea. fert_units_per_day is the COMMON (Fertility 5)
    rate observed in-app; output scales linearly with Fertility (docs)."""
    units = fert_units_per_day * fertility / base_fertility
    gross = units * fert_price_eth
    net = gross * (1 - (royalty_pct + opensea_fee_pct) / 100) - gas_eth_per_claim * claims_per_day
    return {"units_per_day": units, "net_eth_per_day": net,
            "payback_days": (tier_floor_eth / net) if net > 0 else None,
            "annualized_pct": (net * 365 / tier_floor_eth * 100) if net > 0 else None}


def farm_vs_buy(pack_price_eth: float, ev_worth_x: float, farmer_pct: float, farmer_dues_pct: float,
                pool_price_eth_per_yield: float, buy_tax_pct: float) -> dict:
    """Cheapest route to accumulate $YIELD. Farming: pack → crop (EV worth multiple) → Farmer pays
    farmer_pct of crop value in $YIELD at pool price, skipping the buy tax, minus Co-op dues.
    Direct: buy on the official pool and pay the buy tax. All inputs are redacted until launch."""
    yield_per_eth_farm = ev_worth_x * farmer_pct / 100 * (1 - farmer_dues_pct / 100) / pool_price_eth_per_yield
    yield_per_eth_buy = (1 - buy_tax_pct / 100) / pool_price_eth_per_yield
    return {"yield_per_eth_farming": yield_per_eth_farm, "yield_per_eth_direct": yield_per_eth_buy,
            "farming_advantage_pct": (yield_per_eth_farm / yield_per_eth_buy - 1) * 100,
            "farm_if": yield_per_eth_farm > yield_per_eth_buy}
