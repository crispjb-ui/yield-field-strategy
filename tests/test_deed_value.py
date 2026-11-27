from yf.roi import deed_coop_value

def test_deed_coop_value():
    r = deed_coop_value(500_000, 0.2)
    assert 32 < r["usd_to_this_deed"] < 34 and r["pct_of_deed_price"] < 3
    assert 17e6 < r["coop_inflow_needed_for_payback_usd"] < 19e6
    assert deed_coop_value(500_000, 0.2, fertility=9)["usd_to_this_deed"] > r["usd_to_this_deed"] * 1.49
