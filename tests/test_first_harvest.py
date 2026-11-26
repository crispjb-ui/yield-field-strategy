from datetime import datetime, timezone
from yf.roi import seed_release, truffle_day_ev, TRUFFLE_SEED
from yf.poolwatch import minutes_to_next_settlement

def test_seed_schedule_sums_and_front_weights():
    assert abs(sum(seed_release(d) for d in range(1, 31)) - TRUFFLE_SEED) < 1e-3
    assert seed_release(1) > seed_release(2) > seed_release(30) > 0 and seed_release(31) == 0
    assert 640_000 < seed_release(1) < 650_000

def test_truffle_day_ev_breakeven():
    r = truffle_day_ev(3.25, 690.0, 2.5e-8 * 58.7, day=1)       # tiny share of a crowded day
    assert 0.4 < r["share_pct"] < 0.5 and 2500 < r["expected_tokens"] < 3200
    assert r["breakeven_mcap_eth"] > 5000                        # needs a multi-thousand-ETH cap to cover the fee
    quiet = truffle_day_ev(1.0, 30.0, 1e-6, day=5)
    assert quiet["expected_tokens"] > 15000 and quiet["breakeven_mcap_eth"] < 600

def test_settlement_is_1400_utc():
    assert abs(minutes_to_next_settlement(datetime(2026, 11, 28, 14, 30, tzinfo=timezone.utc)) - 23.5 * 60) < 1e-6
    assert abs(minutes_to_next_settlement(datetime(2026, 11, 29, 13, 15, tzinfo=timezone.utc)) - 45) < 1e-6
