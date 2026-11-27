from yf.poolwatch import decide, State, Rules, roundtrip_breakeven

def test_ladder_sequence():
    st = State()
    assert decide(3.4, 5.0, st)["action"] is None                       # 1.47x
    assert decide(3.4, 7.0, st)["action"] == "SELL 50% OF BAG"          # 2.06x
    st.stage, st.realized_eth = 1, 3.5                                   # sold half
    assert decide(3.4, 5.0, st)["action"] is None                       # (3.5+5)/3.4 = 2.5x
    assert decide(3.4, 8.5, st)["action"] == "SELL 50% OF REMAINING"    # 3.53x
    st.stage, st.realized_eth = 2, 7.75
    assert decide(3.4, 0.9, st)["action"] is None                       # 2.54x, still above 0.7 × 3.53 = 2.47
    assert decide(3.4, 0.5, st)["action"] == "SELL DOWN TO MOONBAG"     # 2.43x ≤ 2.47

def test_trailing_stop_arms_only_after_gain():
    st = State()
    decide(3.4, 3.0, st)                                                 # 0.88x, never armed
    assert decide(3.4, 1.5, st)["action"] is None
    st = State(); decide(3.4, 6.0, st)                                   # peak 1.76x, armed
    assert decide(3.4, 4.0, st)["action"] == "SELL DOWN TO MOONBAG"     # 1.18x ≤ 1.76*0.7

def test_presettlement_rule():
    st = State()
    assert decide(3.4, 4.5, st, mins_to_settlement=30)["action"] == "SELL 50% OF BAG"   # 1.32x
    st = State()
    assert decide(3.4, 3.6, st, mins_to_settlement=30)["action"] is None                # 1.06x < 1.2
    st = State()
    assert decide(3.4, 4.5, st, mins_to_settlement=300)["action"] is None

def test_breakeven():
    b = roundtrip_breakeven(3)
    assert abs(b["beat_market_multiple"] - 1/0.97) < 1e-9 and 1.09 < b["recover_pack_eth_multiple"] < 1.11
    assert 1.33 < roundtrip_breakeven(20)["recover_pack_eth_multiple"] < 1.35

def test_inflow_end_rule():
    st = State()
    assert decide(3.25, 4.5, st, hours_since_launch=1.0)["action"] is None             # 1.38x, too early
    assert decide(3.25, 4.5, st, hours_since_launch=3.2)["action"] == "SELL 50% OF BAG"
    st = State()
    assert decide(3.25, 3.4, st, hours_since_launch=3.2)["action"] is None             # 1.05x < 1.2
