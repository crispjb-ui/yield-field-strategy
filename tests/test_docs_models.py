import pytest
from yf.roi import seed_pack_ev, burn_vs_sell, fert_deed_yield, tier_relative_value, MissingMechanics
from yf import config

def test_tier_scores_from_docs_fertility():
    t = config.load_mechanics()["deed"]["tiers"]
    rv = tier_relative_value(t)
    scores = {k: v["score"] for k, v in rv.items()}
    assert scores["Rare"] > scores["Common"] > scores["Legendary"] > scores["Mythic"]
    assert abs(rv["Mythic"]["util_ratio"] - 1.8) < 1e-9
    assert rv["Rare"]["score"] > 1.08 and rv["Mythic"]["score"] < 0.6

def test_seed_ev_refuses_on_redacted():
    with pytest.raises(MissingMechanics):
        seed_pack_ev(0.1, config.load_mechanics()["seeds"]["rarities"], 80)

def test_seed_ev_math():
    r = {"Common": {"p": 0.6, "worth_x": 0.5}, "Rare": {"p": 0.4, "worth_x": 2.0}}
    ev = seed_pack_ev(1.0, r, payout_pct=80, dues_pct=10)   # E[x]=1.1 → 1.1*0.8*0.9=0.792
    assert abs(ev["ev_ratio"] - 0.792) < 1e-9 and ev["house_edge_pct"] > 20

def test_burn_vs_sell():
    r = burn_vs_sell(0.05, silo_yield=1_000_000, windfall_pct=0.5, yield_eth=1e-7, tier_floor_eth=0.96)
    assert abs(r["sell_value_eth"] - 0.9024) < 1e-9 and r["burn_if"] is False

def test_fert_deed_yield_scales_with_fertility():
    c = fert_deed_yield(10, 0.001, 0.875, fertility=5)
    r = fert_deed_yield(10, 0.001, 0.96, fertility=6)
    assert abs(r["units_per_day"] / c["units_per_day"] - 1.2) < 1e-9
    assert r["net_eth_per_day"] > c["net_eth_per_day"]
