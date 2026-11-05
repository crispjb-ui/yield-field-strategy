from yf.roi import launch_fert_need

def test_gap_shrinks_with_pack_price():
    cheap = launch_fert_need(6000, 20, 120)
    dear = launch_fert_need(6000, 220, 120)
    assert cheap["packs"] == 300 and cheap["gap"] == 600 - 120 - 31.5
    assert dear["packs"] == 27 and dear["gap"] == 0

def test_slot_binding():
    r = launch_fert_need(6000, 50, 120, grow_hours=48)
    assert r["crops_possible_no_fert"] == 87 and r["crops_possible_with_fert"] == 175
    assert r["slots_bind_without_fert"] is True
