import json
from yf.fertrate import summarize, project, milestones

def test_summarize_live_snapshot_shape():
    fr = json.load(open("data/snapshots/fert-rate-2026-11-04.json"))
    s = summarize(fr)
    assert abs(s["network_output_per_day"] - 8373.5) < 1e-6
    assert abs(s["staked_fertility"] - 16747) < 1e-6
    assert s["network_rate"] == 1.0 and 0.4 < s["days_in_circulation"] < 0.5

def test_projection_reaches_floor_and_never_recovers_without_consumption():
    rows = project(3848, 8373.5, days=60)
    assert rows[5]["speed"] == 1.0 and rows[-1]["speed"] == 0.5
    m = milestones(3848, 8373.5)
    assert m["to_7d_slowdown_start"] == 7 and 9 <= m["to_10d_70pct"] <= 12 and 15 <= m["to_14d_50pct"] <= 20

def test_projection_with_consumption_can_hold_full_speed():
    rows = project(3848, 8373.5, days=30, consumption_per_day=8373.5)
    assert all(r["speed"] == 1.0 for r in rows)
