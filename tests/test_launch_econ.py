from yf.roi import pack_cycle, cycling, truffle_cycle_ev, farmer_vs_direct, windfall_race, seed_pack_ev
from yf import config

def test_pack_ev_from_mirror_defaults():
    m = config.load_mechanics()["seeds"]
    ev = seed_pack_ev(0.25, m["rarities"], payout_pct=90)
    assert abs(ev["ev_crop_value_eth"] - 0.24875) < 1e-9 and abs(ev["ev_ratio"] - 0.8955) < 1e-9
    assert abs(pack_cycle(0.25)["rake_per_eth"] - 0.1045) < 1e-9

def test_cycling_burns_capital():
    c = cycling(2.7, 12)
    assert 0.7 < c["capital_left_eth"] < 0.75 and 18 < c["total_pack_spend_eth"] < 20

def test_truffle_ev_rule():
    # big budget, small network weight → worth it; tiny budget → not
    assert truffle_cycle_ev(100000, 1e-3, 5.0, 1.0)["worth_it"] is True
    assert truffle_cycle_ev(100, 1e-6, 50.0, 1.0)["worth_it"] is False

def test_farmer_vs_direct():
    assert farmer_vs_direct(90)["farmer_wins"] is True
    assert farmer_vs_direct(5)["farmer_wins"] is False
    assert abs(farmer_vs_direct(0)["breakeven_buy_tax_pct"] - 10.45) < 1e-9

def test_windfall_race_order_matters():
    a = windfall_race(10000, [9, 5, 8]); b = windfall_race(10000, [5, 9, 8])
    assert a[0]["wins"] == 9000 and b[0]["wins"] == 5000 and abs(b[1]["wins"] - 4500) < 1e-9
