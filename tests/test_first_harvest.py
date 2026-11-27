from datetime import datetime, timezone
from yf.roi import seed_release, truffle_day_ev, TRUFFLE_SEED
from yf.poolwatch import minutes_to_next_settlement

def test_seed_schedule_sums_and_front_weights():
    assert abs(sum(seed_release(d) for d in range(1, 31)) - TRUFFLE_SEED) < 10_000
    assert seed_release(1) > seed_release(2) > seed_release(30) > 0 and seed_release(31) == 0
    assert seed_release(1) == 441_000 and abs(seed_release(30) - 226_000) < 1e-6

def test_truffle_day_ev_breakeven():
    r = truffle_day_ev(3.25, 690.0, 2.5e-8 * 58.7, day=1)       # tiny share of a crowded day
    assert 0.4 < r["share_pct"] < 0.5 and 1700 < r["expected_tokens"] < 2200
    assert r["breakeven_mcap_eth"] > 5000                        # needs a multi-thousand-ETH cap to cover the fee
    quiet = truffle_day_ev(1.0, 30.0, 1e-6, day=5)
    assert quiet["expected_tokens"] > 12000 and quiet["breakeven_mcap_eth"] < 700

def test_settlement_is_1400_utc():
    assert abs(minutes_to_next_settlement(datetime(2026, 11, 28, 14, 30, tzinfo=timezone.utc)) - 23.5 * 60) < 1e-6
    assert abs(minutes_to_next_settlement(datetime(2026, 11, 29, 13, 15, tzinfo=timezone.utc)) - 45) < 1e-6

from yf.roi import launch_buy_tax, farmer_edge, pig_plan, coop_daily, exit_breakeven

def test_launch_docs_models():
    assert launch_buy_tax(0) == 90 and launch_buy_tax(2) == 41 and launch_buy_tax(6) == 2 and launch_buy_tax(9) == 2
    assert farmer_edge(0.5)["farmer_advantage_x"] > 3.5 and farmer_edge(6)["farmer_advantage_x"] < 1
    p = pig_plan(135); assert p["reaches_level"] == 10 and p["fert_used"] == 135 and abs(p["hours"] - 180) < 1e-9
    p = pig_plan(110); assert p["reaches_level"] == 9 and p["fert_used"] == 108
    c = coop_daily(250_000); assert c["coop_buy_usd_per_day"] == 7500 and 0.7 < c["per_deed_usd_per_day"] < 0.8
    assert 1.24 < exit_breakeven(2.0, 1.75) < 1.26 and 1.5 < exit_breakeven(2.0, 1.75, 20) < 1.53
