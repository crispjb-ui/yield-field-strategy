"""$YIELD exit ladder. Decision variable: what the bag would fetch RIGHT NOW in ETH, net of sell tax and
slippage (pool.quoteYieldForEth(balance)), plus ETH already realized, divided by ETH spent on packs."""
from __future__ import annotations
import json
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class Rules:
    t1_multiple: float = 2.0        # sell half: principal back
    t2_multiple: float = 3.5        # sell half of what is left
    trail_drop: float = 0.30        # after the peak, a 30% fall in total multiple → cut to the moonbag
    trail_arm_multiple: float = 1.5 # trailing stop only arms once the position has been this far up
    moonbag_frac: float = 0.15      # of the original bag, kept with no target
    presettle_minutes: int = 45     # before the first 00:00 UTC Truffle settlement
    presettle_min_multiple: float = 1.2


@dataclass
class State:
    stage: int = 0                  # 0 none sold, 1 after T1, 2 after T2, 3 moonbag only
    peak_multiple: float = 0.0
    realized_eth: float = 0.0
    presettle_done: bool = False


def minutes_to_next_settlement(now: datetime | None = None) -> float:
    now = now or datetime.now(timezone.utc)
    nxt = (now.replace(hour=0, minute=0, second=0, microsecond=0)).timestamp() + 86400
    return (nxt - now.timestamp()) / 60


def decide(cost_eth: float, bag_exit_eth: float, st: State, r: Rules = Rules(),
           mins_to_settlement: float | None = None, first_settlement_pending: bool = True) -> dict:
    """Pure decision. Returns the multiple, the action (or None) and the reason."""
    m = (st.realized_eth + bag_exit_eth) / cost_eth if cost_eth else 0.0
    st.peak_multiple = max(st.peak_multiple, m)
    action = reason = None
    if st.stage < 3 and st.peak_multiple >= r.trail_arm_multiple and m <= st.peak_multiple * (1 - r.trail_drop):
        action, reason = "SELL DOWN TO MOONBAG", f"multiple {m:.2f} is {r.trail_drop:.0%} off the peak {st.peak_multiple:.2f}"
    elif st.stage == 0 and m >= r.t1_multiple:
        action, reason = "SELL 50% OF BAG", f"multiple {m:.2f} ≥ {r.t1_multiple}: principal back"
    elif st.stage == 1 and m >= r.t2_multiple:
        action, reason = "SELL 50% OF REMAINING", f"multiple {m:.2f} ≥ {r.t2_multiple}"
    elif (st.stage == 0 and first_settlement_pending and not st.presettle_done and mins_to_settlement is not None
          and mins_to_settlement <= r.presettle_minutes and m >= r.presettle_min_multiple):
        action, reason = "SELL 50% OF BAG", (f"{mins_to_settlement:.0f} min to the first Truffle settlement "
                                              f"(new $YIELD reaches farmers at 00:00 UTC) and multiple {m:.2f} > {r.presettle_min_multiple}")
    return {"multiple": m, "peak": st.peak_multiple, "action": action, "reason": reason, "stage": st.stage}


def roundtrip_breakeven(sell_tax_pct: float, farmer_fee_pct: float = 10.0, ev_x: float = 0.995) -> dict:
    """Price multiple vs your average Farmer entry needed to (a) beat having sold the crops to the Market,
    (b) get the pack ETH back."""
    keep = 1 - sell_tax_pct / 100
    into = ev_x * (1 - farmer_fee_pct / 100)
    return {"beat_market_multiple": 1 / keep, "recover_pack_eth_multiple": 1 / (into * keep)}


def watch(rpc, pool_addr: str, wallet: str, cost_eth: float, state_file: Path, interval: int = 20,
          launch_day_first_settlement: bool = True, once: bool = False):
    from .abi import Contract
    pool = Contract(rpc, pool_addr, "abi_3")
    token = Contract(rpc, pool.call("yieldToken"), "abi_5")
    st = State(**json.loads(state_file.read_text())) if state_file.exists() else State()
    base_sell = None
    while True:
        try:
            bal = token.call("balanceOf", wallet)
            exit_eth = pool.call("quoteYieldForEth", bal) / 1e18 if bal else 0.0
            sell, buy = pool.call("sellFeeBps") / 100, pool.call("buyFeeBps") / 100
            base_sell = sell if base_sell is None else min(base_sell, sell)
            d = decide(cost_eth, exit_eth, st, mins_to_settlement=minutes_to_next_settlement(),
                       first_settlement_pending=launch_day_first_settlement)
            line = (f"{datetime.now(timezone.utc):%H:%M:%S}Z bag {bal/1e18:,.0f} $YIELD → {exit_eth:.4f} ETH net | "
                    f"multiple {d['multiple']:.2f} (peak {d['peak']:.2f}) | buy tax {buy:.1f}% sell tax {sell:.1f}%"
                    f"{' HEAVY-SELLING TAX ON' if sell > base_sell else ''} | spot {pool.call('spotPrice')}")
            print(line, flush=True)
            if d["action"]:
                print(f"ACTION: {d['action']} — {d['reason']}", flush=True)
            state_file.write_text(json.dumps(asdict(st)))
        except Exception as e:
            print("watch error:", str(e)[:120], flush=True)
        if once:
            return
        time.sleep(interval)
