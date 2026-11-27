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


def _interp(x: float, pts: list[tuple[float, float]]) -> float:
    if x <= pts[0][0]:
        return pts[0][1]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return pts[-1][1]


def exporter_speed(export_frac: float) -> float:
    """Deck speed vs 24 h exports ÷ decks' daily nominal output. Docs chart (3 Nov): 100% up to 25%,
    90% at 30%, 70% at 40%, 50% at ≥50%, linear between points."""
    return _interp(export_frac, [(0.25, 1.0), (0.30, 0.9), (0.40, 0.7), (0.50, 0.5)])


def network_speed(days_in_circulation: float) -> float:
    """Docs chart: 100% up to 7 days of network output in circulation, 70% at 10, 50% at 14+, linear."""
    return _interp(days_in_circulation, [(7, 1.0), (10, 0.7), (14, 0.5)])


def export_policy(nominal_per_day: float, network_rate: float = 1.0) -> list[dict]:
    """For each export fraction, units exported vs kept per day. Exported units are capped at
    50% of nominal (daily export limit). Kept = produced − exported, produced = nominal × speed."""
    rows = []
    for f in (0.0, 0.10, 0.20, 0.25, 0.30, 0.40, 0.50):
        speed = min(exporter_speed(f), network_rate)
        produced = nominal_per_day * speed
        exported = min(f * nominal_per_day, 0.5 * nominal_per_day, produced)
        rows.append({"export_frac": f, "speed": speed, "produced": produced,
                     "exported": exported, "kept": produced - exported})
    return rows


def launch_fert_need(budget_usd: float, pack_price_usd: float, stockpile: float, own_per_day: float = 4.5,
                     window_days: int = 7, slots: int = 25, grow_hours: float | None = None) -> dict:
    """Fert needed to fully fertilize (2 units) every pack the budget buys in the launch window,
    net of stockpile and own production. If grow_hours is given, also reports whether 25 slots
    bind without Fert (capital deploys slower than the window) — the only case where Fert has
    value beyond speed."""
    packs = int(budget_usd // pack_price_usd)
    need = 2 * packs
    have = stockpile + own_per_day * window_days
    out = {"packs": packs, "fert_needed": need, "fert_available": have, "gap": max(0, need - have),
           "fert_cost_per_crop_usd_at": lambda px: 2 * px}
    if grow_hours:
        cycles_no_fert = window_days * 24 / grow_hours
        cycles_fert = window_days * 24 / (grow_hours / 2)
        out["crops_possible_no_fert"] = int(slots * cycles_no_fert)
        out["crops_possible_with_fert"] = int(slots * cycles_fert)
        out["slots_bind_without_fert"] = packs > slots * cycles_no_fert
    del out["fert_cost_per_crop_usd_at"]
    return out


def plots_needed(budget_usd: float, pack_price_usd: float, grow_hours: float, window_days: int = 7,
                 slots: int = 25, fert_per_crop: int = 2, stockpile: float = 120, own_per_day: float = 4.5) -> dict:
    """Minimum fully-allocated plots so the whole budget deploys inside the launch window, with and
    without Fert, and the Fert required to fertilize every crop. Plots beyond this have zero value."""
    import math
    packs = int(budget_usd // pack_price_usd)
    cyc = grow_hours * (1 - 0.25 * fert_per_crop)
    cap_fert = slots * window_days * 24 / cyc
    cap_no = slots * window_days * 24 / grow_hours
    need = fert_per_crop * packs
    have = stockpile + own_per_day * window_days
    return {"packs": packs, "plots_with_fert": max(1, math.ceil(packs / cap_fert)),
            "plots_without_fert": max(1, math.ceil(packs / cap_no)),
            "fert_needed": need, "fert_gap": max(0, need - have),
            "per_cycle_outlay_usd_one_plot": slots * pack_price_usd}


# ---- Launch economics (mirror defaults 2026-11-11; recompute from the Cornhub contract at launch) ----
EV_WORTH_X = 0.995            # Σ p × worth over the 6 seed rarities
SALE_FEE = 0.08               # Market fee on mainnet CornHub (2026-11-23); Farmer fee is 0.06
TRUFFLE_P = 0.10              # official X thread 2026-11-26: "Each crop: 1 in 10 Truffle chance" (was 1 in 20)


def pack_cycle(pack_price_eth: float, fee: float = SALE_FEE, ev_x: float = EV_WORTH_X) -> dict:
    """One pack → crop → sale. ETH-only loop: payout = ev_x × (1 − fee) per ETH; the rest is the rake."""
    payout = ev_x * (1 - fee)
    return {"payout_per_eth": payout, "rake_per_eth": 1 - payout,
            "expected_truffle_weight_per_eth": TRUFFLE_P * ev_x}


def cycling(capital_eth: float, cycles: int, fee: float = SALE_FEE, ev_x: float = EV_WORTH_X) -> dict:
    """Recycle capital through packs → Market → packs. Total pack spend, truffle weight and what is left."""
    r = ev_x * (1 - fee)
    spend = capital_eth * (1 - r ** cycles) / (1 - r)
    return {"total_pack_spend_eth": spend, "capital_left_eth": capital_eth * r ** cycles,
            "rake_paid_eth": capital_eth * (1 - r ** cycles),
            "expected_truffle_weight_eth": TRUFFLE_P * ev_x * spend}


def truffle_cycle_ev(budget_yield_tonight: float, yield_eth: float, total_weight_eth: float,
                     my_pack_spend_eth: float, fee: float = SALE_FEE, ev_x: float = EV_WORTH_X) -> dict:
    """Is one more ETH of pack spend worth it tonight? Expected truffle share of B vs the rake.
    Inputs are what the Truffles tab shows live: 'Pays out today' (B), 'Weight today' (W)."""
    my_w = TRUFFLE_P * ev_x * my_pack_spend_eth
    share = my_w / (total_weight_eth + my_w) if (total_weight_eth + my_w) > 0 else 0
    payout_eth = budget_yield_tonight * 0.95 * share * yield_eth      # 5% Motherlode off the top
    rake = my_pack_spend_eth * (1 - ev_x * (1 - fee))
    return {"my_truffle_weight_eth": my_w, "share": share, "expected_payout_eth": payout_eth,
            "rake_eth": rake, "net_eth": payout_eth - rake, "worth_it": payout_eth > rake}


def farmer_vs_direct(buy_tax_pct: float, fee: float = SALE_FEE, ev_x: float = EV_WORTH_X) -> dict:
    """$YIELD per ETH: Farmer route (pack → crop → Farmer swap, tax-free) vs direct pool buy with tax."""
    farmer = ev_x * (1 - fee)
    direct = 1 - buy_tax_pct / 100
    return {"farmer_yield_per_eth": farmer, "direct_yield_per_eth": direct,
            "farmer_wins": farmer > direct, "breakeven_buy_tax_pct": (1 - farmer) * 100}


def windfall_race(silo_yield: float, burns: list[int]) -> list[dict]:
    """Sequential Silo race: each burn takes min(F×10%,100%) of what is left."""
    out, left = [], silo_yield
    for f in burns:
        share = min(f * 0.10, 1.0); win = left * share; left -= win
        out.append({"fertility": f, "share": share, "wins": win, "silo_left": left})
    return out


# ---- Pre-launch pack sizing (official prices/odds, docs 19 Nov) ----
PACK_ETH = {"Bronze": 0.005, "Silver": 0.01, "Gold": 0.05, "Platinum": 0.1, "Diamond": 0.25}
ODDS = [(0.45, 0.5), (0.31, 1.0), (0.15, 1.6), (0.06, 2.0), (0.025, 3.0), (0.005, 5.0)]
TIER_FACTOR = {"Bronze": 120, "Silver": 116, "Gold": 108, "Platinum": 104, "Diamond": 100}


def pack_mix(mix: dict, fert_per_crop: int = 2, slots: int = 25, fee: float = SALE_FEE) -> dict:
    """mix = {"Platinum": 20, "Gold": 5}. Cost, expected crop value, 1-sigma, truffle odds, Fert, timing."""
    import math
    ev = sum(p * w for p, w in ODDS)
    var_w = sum(p * w * w for p, w in ODDS) - ev * ev
    n = sum(mix.values())
    cost = sum(PACK_ETH[t] * q for t, q in mix.items())
    value = ev * cost
    sd = math.sqrt(sum(q * (PACK_ETH[t] ** 2) * var_w for t, q in mix.items()))
    speed = 1 - 0.25 * fert_per_crop
    slot_hours = sum(q * sum(p * w * 10 * TIER_FACTOR[t] / 500 for p, w in ODDS) for t, q in mix.items()) * speed
    longest = max(5.0 * 10 * TIER_FACTOR[t] / 500 for t in mix) * speed
    return {"packs": n, "cost_eth": cost, "expected_crop_value_eth": value, "sd_eth": sd,
            "sd_pct": sd / value * 100 if value else 0, "after_fee_eth": value * (1 - fee),
            "p_no_truffle": (1 - TRUFFLE_P) ** n, "expected_truffles": TRUFFLE_P * n, "expected_truffle_weight_eth": TRUFFLE_P * value,
            "fert_needed": fert_per_crop * n, "plots_at_once": n / slots,
            "avg_hours_first_cycle": slot_hours / n if n else 0, "approx_hours_to_clear": max(slot_hours / slots, 0),
            "longest_possible_hours": longest, "worst_case_market_exit_loss_eth": cost - value * (1 - fee)}


# ---- First Harvest (official X thread 2026-11-26) ----
TRUFFLE_SEED = 10_000_000       # $YIELD in the Truffle Pool = 10% of supply → total supply 100M
YIELD_SUPPLY = 100_000_000


def seed_release(day: int, days: int = 30, first: float = 441_000, last: float = 226_000) -> float:
    """Daily Truffle release from the 10M launch seed. Official docs 27 Nov: "about 441,000 on day one,
    easing to about 226,000 on day 30" (linear between them sums to ~10.0M)."""
    if not 1 <= day <= days:
        return 0.0
    return first + (last - first) * (day - 1) / (days - 1)


def truffle_day_ev(my_crop_value_eth: float, network_crop_value_eth: float, yield_price_eth: float, day: int = 1,
                   fee: float = SALE_FEE, motherlode: float = 0.05, pig_size: float = 1.0) -> dict:
    """Expected Truffle income for one day's harvests vs the sale fee paid on them. Share is pro-rata on crop
    value harvested by Pig owners that day (expected-value view; the 1-in-10 roll makes any single day lumpy)."""
    budget = seed_release(day) * (1 - motherlode)
    share = my_crop_value_eth * pig_size / network_crop_value_eth if network_crop_value_eth else 0.0   # network weight already includes others' pig sizes
    tokens = budget * share
    fee_eth = my_crop_value_eth * fee
    return {"budget_yield": budget, "share_pct": share * 100, "expected_tokens": tokens,
            "expected_eth": tokens * yield_price_eth, "fee_eth": fee_eth,
            "breakeven_price_eth": fee_eth / tokens if tokens else None,
            "breakeven_mcap_eth": (fee_eth / tokens * YIELD_SUPPLY) if tokens else None}


def deed_coop_value(coop_inflow_usd: float, deed_share: float, fertility: int = 6,
                    tended_fertility: float = 18_235, deed_price_usd: float = 1186.0) -> dict:
    """What one deed receives if the Co-op routes `deed_share` of `coop_inflow_usd` to tended deeds by Fertility.
    Valued at the Co-op's own purchase cost (token price moves after that are a separate bet)."""
    usd = coop_inflow_usd * deed_share * fertility / tended_fertility
    return {"usd_to_this_deed": usd, "pct_of_deed_price": usd / deed_price_usd * 100,
            "coop_inflow_needed_for_payback_usd": deed_price_usd * tended_fertility / fertility / deed_share}


# ---- Launch docs 27 Nov 2026 ----
LAUNCH_TAX_POINTS = [(0, 90.0), (1, 63.0), (2, 41.0), (3, 24.0), (4, 12.0), (6, 2.0)]   # % on buys, hours after launch
BUY_TAX, SELL_TAX, SELL_TAX_MAX = 2.0, 3.0, 20.0
FARMER_FEE, BROKER_FEE = 0.06, 0.08
PIG_SIZE = {1: 1.0, 2: 1.35, 3: 1.7, 4: 2.05, 5: 2.4, 6: 2.52, 7: 2.64, 8: 2.76, 9: 2.88, 10: 3.0}


def launch_buy_tax(hours: float) -> float:
    """Buy tax (%) for a market buyer at `hours` after launch (docs points, linear between; 2% after hour 6)."""
    return _interp(hours, LAUNCH_TAX_POINTS)


def farmer_edge(hours: float, ev_x: float = EV_WORTH_X) -> dict:
    """$YIELD per ETH: Farmer (6% dues, no tax) vs a market buy at that hour."""
    farmer, direct = ev_x * (1 - FARMER_FEE), 1 - launch_buy_tax(hours) / 100
    return {"buy_tax_pct": launch_buy_tax(hours), "farmer_per_eth": farmer, "direct_per_eth": direct,
            "farmer_advantage_x": farmer / direct if direct else float("inf")}


def pig_plan(fert_available: int, target_level: int = 10) -> dict:
    """Fully fed pig: each level L costs 3 feeds × L Fertilizer and waits 16 h × L × 25%."""
    fert = hours = 0.0; level = 1; rows = []
    while level < target_level and fert + 3 * level <= fert_available:
        fert += 3 * level; hours += 16 * level * 0.25; level += 1
        rows.append({"level": level, "size": PIG_SIZE[level], "hours_after_launch": hours, "fert_used": fert})
    return {"reaches_level": level, "size": PIG_SIZE[level], "fert_used": fert, "hours": hours, "steps": rows}


def coop_daily(fund_usd: float, tended_fertility: float = 18_235, fertility: int = 6, spend_rate: float = 0.03,
               deed_share: float = 0.30) -> dict:
    """Co-op spends 3% of its fund a day; 30% of each buy goes to tended deeds by Fertility, 70% to truffles."""
    buy = fund_usd * spend_rate
    return {"coop_buy_usd_per_day": buy, "to_truffles_usd": buy * (1 - deed_share), "to_deeds_usd": buy * deed_share,
            "per_deed_usd_per_day": buy * deed_share * fertility / tended_fertility,
            "per_deed_after_claim_fee": buy * deed_share * fertility / tended_fertility * 0.9}


def exit_breakeven(paid_eth: float, crop_value_eth: float, sell_tax_pct: float = SELL_TAX) -> float:
    """Price multiple vs your Farmer entry needed to get `paid_eth` back out, net of the sell tax."""
    return paid_eth / (crop_value_eth * (1 - FARMER_FEE) * (1 - sell_tax_pct / 100))
