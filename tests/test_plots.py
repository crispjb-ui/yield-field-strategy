from yf.roi import plots_needed

def test_plots_needed_cases():
    assert plots_needed(6000, 20, 48)["plots_with_fert"] == 2
    assert plots_needed(6000, 20, 72)["plots_with_fert"] == 3
    assert plots_needed(6000, 20, 48)["plots_without_fert"] == 4
    assert plots_needed(6000, 110, 72)["plots_with_fert"] == 1
    assert plots_needed(6000, 220, 24)["fert_gap"] == 0
