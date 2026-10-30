"""CLI: market | positions | roi | watch | allocate."""
from __future__ import annotations
import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

from . import config
from .ledger import read_ledger, mark
from .opensea import OpenSea
from .roi import MissingMechanics, seed_roi, deed_roi, allocate

ROOT = config.ROOT
SNAP_DIR = ROOT / "data" / "snapshots"


def eth_usd(cfg: dict) -> float | None:
    if cfg.get("pricing", {}).get("eth_usd_source") != "coingecko":
        return None
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price",
                         params={"ids": "ethereum", "vs_currencies": "usd"}, timeout=15)
        return float(r.json()["ethereum"]["usd"])
    except Exception:
        return None


def cmd_market(cfg, args):
    os_ = OpenSea(cfg["opensea"]["api_key"], cfg["opensea"]["collection_slug"])
    snap = os_.snapshot()
    snap["ts"] = datetime.now(timezone.utc).isoformat()
    snap["eth_usd"] = eth_usd(cfg)
    print(json.dumps(snap, indent=2))
    if args.save:
        SNAP_DIR.mkdir(parents=True, exist_ok=True)
        with open(SNAP_DIR / "market.jsonl", "a") as f:
            f.write(json.dumps(snap) + "\n")
    return snap


def cmd_positions(cfg, args):
    ledger = ROOT / "data" / ("ledger.csv" if (ROOT / "data" / "ledger.csv").exists()
                              else "ledger.example.csv")
    pos = read_ledger(ledger)
    floor = args.floor
    usd = args.eth_usd
    if floor is None:
        snap = OpenSea(cfg["opensea"]["api_key"], cfg["opensea"]["collection_slug"]).snapshot()
        floor = float(snap["floor_eth"] or 0)
        usd = usd or eth_usd(cfg)
    print(json.dumps(mark(pos, floor, usd), indent=2))


def cmd_roi(cfg, args):
    mech = config.load_mechanics()
    try:
        print("Seeds (sorted by daily ROI%):")
        for r in seed_roi(mech, fert_mult=args.fert_mult, price_haircut=args.haircut):
            print(f"  {r.name:<16} cost {r.cost_yield:>8.2f}  harvest {r.harvest_yield:>8.2f}  "
                  f"net/cycle {r.net_per_cycle_yield:>8.2f}  daily {r.daily_roi_pct:>7.2f}%  "
                  f"payback {r.payback_days if r.payback_days else '—'}d")
        d = deed_roi(mech, floor_eth=args.floor, yield_eth=args.yield_eth,
                     gas_eth_per_claim=args.gas)
        print("Deed loop:", json.dumps(d.__dict__, indent=2))
    except MissingMechanics as e:
        print(f"ROI model blocked: {e}", file=sys.stderr)
        sys.exit(2)


def cmd_allocate(cfg, args):
    print(json.dumps(allocate(args.budget, floor_usd=args.floor_usd), indent=2))


def cmd_watch(cfg, args):
    a = cfg["alerts"]
    while True:
        try:
            snap = cmd_market(cfg, argparse.Namespace(save=True))
            fl = snap.get("floor_eth")
            bo = snap.get("best_offer_eth")
            v = snap.get("volume_24h")
            alerts = []
            if fl is not None and fl < a["floor_below_eth"]:
                alerts.append(f"FLOOR BELOW {a['floor_below_eth']} ETH: {fl}")
            if fl is not None and fl > a["floor_above_eth"]:
                alerts.append(f"FLOOR ABOVE {a['floor_above_eth']} ETH: {fl}")
            if bo is not None and bo > a["best_offer_above_eth"]:
                alerts.append(f"BEST OFFER ABOVE {a['best_offer_above_eth']} ETH: {bo}")
            eu = snap.get("eth_usd")
            if v is not None and eu and v * eu < a["volume_24h_below_usd"]:
                alerts.append(f"24H VOLUME BELOW ${a['volume_24h_below_usd']}: ${v * eu:,.0f}")
            for line in alerts:
                print("ALERT:", line)
        except Exception as e:  # keep the loop alive
            print("watch error:", e, file=sys.stderr)
        if args.once:
            break
        time.sleep(a["poll_seconds"])


def main(argv=None):
    p = argparse.ArgumentParser(prog="yf")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("market"); s.add_argument("--save", action="store_true")
    s = sub.add_parser("positions"); s.add_argument("--floor", type=float); s.add_argument("--eth-usd", type=float)
    s = sub.add_parser("roi")
    s.add_argument("--floor", type=float, required=True, help="deed floor in ETH")
    s.add_argument("--yield-eth", type=float, help="$YIELD price in ETH")
    s.add_argument("--fert-mult", type=float, default=1.0)
    s.add_argument("--haircut", type=float, default=0.0)
    s.add_argument("--gas", type=float, default=0.0)
    s = sub.add_parser("allocate"); s.add_argument("--budget", type=float, default=8000); s.add_argument("--floor-usd", type=float)
    s = sub.add_parser("watch"); s.add_argument("--once", action="store_true")
    args = p.parse_args(argv)
    cfg = config.load_settings()
    {"market": cmd_market, "positions": cmd_positions, "roi": cmd_roi,
     "allocate": cmd_allocate, "watch": cmd_watch}[args.cmd](cfg, args)


if __name__ == "__main__":
    main()
