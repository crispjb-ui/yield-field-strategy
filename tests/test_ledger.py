from pathlib import Path
from yf.ledger import read_ledger, mark, Position

def test_example_ledger_loads():
    pos = read_ledger(Path("data/ledger.example.csv"))
    assert len(pos) == 3 and all(p.asset == "deed" for p in pos)

def test_mark_fees_and_breakeven():
    pos = [Position("d", "deed", "1", 1, 1.0, 0)] * 3
    m = mark(pos, floor_eth=0.88, royalty_pct=5, market_fee_pct=2.5)
    assert m["deeds"] == 3
    assert abs(m["gross_value_eth"] - 2.64) < 1e-9
    assert abs(m["net_exit_value_eth"] - 2.64 * 0.925) < 1e-9
    assert m["pnl_eth"] < 0
    assert abs(m["breakeven_floor_eth"] - 1 / 0.925) < 1e-9

def test_mark_low_basis_is_profitable():
    pos = [Position("d", "deed", "1", 1, 0.1, 0)] * 3
    m = mark(pos, floor_eth=0.88)
    assert m["pnl_eth"] > 0 and m["pnl_pct"] > 600
