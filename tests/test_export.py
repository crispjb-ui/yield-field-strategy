from yf.roi import export_policy, exporter_speed, network_speed

def test_speed_curves_match_docs_chart():
    assert exporter_speed(0.0) == 1.0 and exporter_speed(0.25) == 1.0
    assert abs(exporter_speed(0.30) - 0.9) < 1e-9 and abs(exporter_speed(0.35) - 0.8) < 1e-9
    assert abs(exporter_speed(0.40) - 0.7) < 1e-9 and exporter_speed(0.50) == 0.5 and exporter_speed(0.9) == 0.5
    assert network_speed(0) == 1.0 and network_speed(7) == 1.0
    assert abs(network_speed(8.5) - 0.85) < 1e-9 and abs(network_speed(10) - 0.7) < 1e-9
    assert abs(network_speed(12) - 0.6) < 1e-9 and network_speed(14) == 0.5 and network_speed(30) == 0.5

def test_owner_three_rares_policy():
    rows = {r["export_frac"]: r for r in export_policy(9.0)}
    assert rows[0.25]["exported"] == 2.25 and rows[0.25]["kept"] == 6.75 and rows[0.25]["produced"] == 9.0
    assert rows[0.50]["produced"] == 4.5 and rows[0.50]["kept"] == 0.0
    assert rows[0.25]["exported"] + rows[0.25]["kept"] > rows[0.50]["exported"] + rows[0.50]["kept"]
