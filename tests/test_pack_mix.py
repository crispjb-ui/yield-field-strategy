from yf.roi import pack_mix

def test_mix_core_numbers():
    m = pack_mix({"Platinum": 20, "Gold": 5})
    assert m["packs"] == 25 and abs(m["cost_eth"] - 2.25) < 1e-9
    assert abs(m["expected_crop_value_eth"] - 2.25 * 0.995) < 1e-9
    assert abs(m["p_no_truffle"] - 0.95 ** 25) < 1e-12 and m["fert_needed"] == 50
    assert 0.2 < m["worst_case_market_exit_loss_eth"] < 0.25

def test_variance_falls_with_more_smaller_packs():
    assert pack_mix({"Diamond": 8})["sd_pct"] > pack_mix({"Platinum": 20})["sd_pct"] > pack_mix({"Gold": 40})["sd_pct"]
