from yf.roi import tier_relative_value, swap_breakeven
from yf import config

def test_shipped_tier_floors_and_ladder():
    t = config.load_mechanics()["deed"]["tiers"]
    rv = tier_relative_value(t)
    assert abs(rv["Rare"]["price_ratio"] - 0.96/0.875) < 1e-9
    assert rv["Mythic"]["scarcity_ratio"] > 14 and rv["Rare"]["util_ratio"] is None

def test_score_flags_cheap_tier():
    t = {"Common": {"count": 1557, "floor_eth": 0.875, "multiplier": 1.0},
         "Rare":   {"count": 888,  "floor_eth": 0.96,  "multiplier": 1.5}}
    rv = tier_relative_value(t)
    assert rv["Rare"]["score"] > 1.3

def test_swap_breakeven():
    r = swap_breakeven({"floor_eth": 0.96, "multiplier": 1}, {"floor_eth": 1.60}, 3)
    assert r["n_buy"] == 1 and abs(r["required_multiplier_ratio"] - 3.0) < 1e-9
