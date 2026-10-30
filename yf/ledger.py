"""Positions ledger: cost basis and mark-to-floor P&L."""
from __future__ import annotations
import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Position:
    date: str
    asset: str
    token_id: str
    qty: float
    cost_eth: float
    eth_usd_at_cost: float
    venue: str = ""
    tier: str = ""
    notes: str = ""

    @property
    def cost_usd(self) -> float:
        return self.cost_eth * self.eth_usd_at_cost


def read_ledger(path: Path) -> list[Position]:
    out = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            out.append(Position(
                date=row["date"], asset=row["asset"], token_id=row.get("token_id", ""),
                qty=float(row["qty"]), cost_eth=float(row["cost_eth"]),
                eth_usd_at_cost=float(row.get("eth_usd_at_cost") or 0),
                venue=row.get("venue", ""), tier=row.get("tier", ""), notes=row.get("notes", "")))
    return out


def mark(positions: list[Position], floor_eth: float, eth_usd: float | None = None,
         royalty_pct: float = 5.0, market_fee_pct: float = 1.0) -> dict:
    """Mark deeds to floor net of exit fees. Fees: 5% creator (verified) +
    OpenSea fee 1.0% (verified from the collection API fees[] 2026-10-30)."""
    deeds = [p for p in positions if p.asset == "deed"]
    qty = sum(p.qty for p in deeds)
    cost = sum(p.cost_eth * p.qty for p in deeds)
    gross = qty * floor_eth
    net = gross * (1 - (royalty_pct + market_fee_pct) / 100)
    out = {
        "deeds": qty,
        "cost_eth": cost,
        "avg_cost_eth": cost / qty if qty else 0.0,
        "floor_eth": floor_eth,
        "gross_value_eth": gross,
        "net_exit_value_eth": net,
        "pnl_eth": net - cost,
        "pnl_pct": ((net - cost) / cost * 100) if cost else None,
        "breakeven_floor_eth": (cost / qty) / (1 - (royalty_pct + market_fee_pct) / 100) if qty else None,
    }
    if eth_usd:
        out["net_exit_value_usd"] = net * eth_usd
        out["pnl_usd"] = (net - cost) * eth_usd
    return out
