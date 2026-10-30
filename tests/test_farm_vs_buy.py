from yf.roi import farm_vs_buy

def test_farming_wins_only_if_ev_times_payout_beats_one_minus_tax():
    # EV 1.1x, Farmer 90%, dues 5% → 0.9405 $/ETH-equiv; direct with 5% tax → 0.95 → buy wins
    r = farm_vs_buy(1.0, 1.1, 90, 5, 1e-6, 5)
    assert r["farm_if"] is False and r["farming_advantage_pct"] < 0
    # EV 1.3x → 1.1115 → farming wins
    assert farm_vs_buy(1.0, 1.3, 90, 5, 1e-6, 5)["farm_if"] is True
