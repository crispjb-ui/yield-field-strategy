import pytest
from yf.roi import seed_roi, deed_roi, allocate, MissingMechanics
from yf import config

def test_shipped_mechanics_are_null_and_model_refuses():
    mech = config.load_mechanics()
    with pytest.raises(MissingMechanics):
        seed_roi(mech)
    with pytest.raises(MissingMechanics):
        deed_roi(mech, floor_eth=0.88, yield_eth=0.0001)

def test_seed_roi_math_on_synthetic_numbers():
    mech = {"seeds": [{"name": "A", "cost_yield": 10, "grow_hours": 12, "harvest_yield": 15},
                      {"name": "B", "cost_yield": 100, "grow_hours": 24, "harvest_yield": 110}]}
    r = seed_roi(mech)
    assert r[0].name == "A"                      # 50%/cycle × 2 cycles/day = 100%/day
    assert abs(r[0].daily_roi_pct - 100) < 1e-9
    assert abs(r[0].payback_days - 1.0) < 1e-9
    assert abs(r[1].daily_roi_pct - 10) < 1e-9
    stressed = seed_roi(mech, price_haircut=0.5)
    assert stressed[1].net_per_cycle_yield < 0   # B is underwater after a 50% haircut

def test_deed_roi_math_on_synthetic_numbers():
    mech = {"deed": {"tiers": {"Rare": {"count": 1, "multiplier": 2.0}}, "owner_tier": "Rare",
                     "output_per_cycle": 5, "cycle_hours": 24, "action_required": True,
                     "upkeep_per_cycle": 1, "pays_yield_directly": False},
            "fert": {"price_yield": 3}}
    d = deed_roi(mech, floor_eth=1.0, yield_eth=0.001, gas_eth_per_claim=0.0005)
    assert d.output_per_day == 10 and d.gross_yield_per_day == 30 and d.net_yield_per_day == 29
    assert abs(d.net_eth_per_day - (0.029 - 0.0005)) < 1e-12
    assert d.payback_days_at_floor > 30

def test_allocate_rules():
    a = allocate(8000, floor_usd=2000)
    assert a["reserve_usd"] == 2000 and a["seed_tranche_usd"] == 1500
    assert a["extra_deeds"] == 2 and a["deed_spend_usd"] == 4000 and a["undeployed_usd"] == 500
    assert allocate(8000)["extra_deeds"] == 0
