"""CornHub pack-sale tracker: incremental scan of PacksPurchased logs (public RPC has no archive state)."""
from __future__ import annotations
import json
from pathlib import Path
from .rpc import Rpc, _keccak

MAINNET = "0x8C1e23Bc90F88DdC8CBA7256798aCbD745072524"     # from the game's own mainnet config (bundle 2026-11-23)
PACKS = ["Bronze", "Silver", "Gold", "Platinum", "Diamond"]
TOPIC = "0x" + _keccak(b"PacksPurchased(address,uint8,uint32,uint256)").hex()
FIRST_SALE_SCAN_FROM = 113_501_675                         # before the first sale (2026-11-20 19:56 UTC)


def scan(rpc: Rpc, state_path: Path, addr: str = MAINNET) -> dict:
    st = json.loads(state_path.read_text()) if state_path.exists() else {
        "next_block": FIRST_SALE_SCAN_FROM, "purchases": 0, "packs": [0] * 5, "eth": [0.0] * 5, "buyers": {}}
    latest = rpc.block_number()
    b, step = st["next_block"], 500_000
    while b <= latest:
        e = min(b + step - 1, latest)
        try:
            logs = rpc.call("eth_getLogs", [{"address": addr, "topics": [TOPIC], "fromBlock": hex(b), "toBlock": hex(e)}])
        except Exception:
            if step <= 2000:
                raise
            step //= 4
            continue
        for l in logs:
            who = "0x" + l["topics"][1][-40:]; pid = int(l["topics"][2], 16); d = l["data"][2:]
            q, p = int(d[:64], 16), int(d[64:128], 16) / 1e18
            st["purchases"] += 1; st["packs"][pid] += q; st["eth"][pid] += p
            st["buyers"][who] = st["buyers"].get(who, 0.0) + p
        b = e + 1
    st["next_block"] = latest + 1
    state_path.write_text(json.dumps(st))
    total = sum(st["eth"])
    top = sorted(st["buyers"].values(), reverse=True)[:10]
    return {"address": addr, "balance_eth": rpc.balance_eth(addr), "total_paid_eth": total,
            "purchases": st["purchases"], "unique_buyers": len(st["buyers"]),
            "by_pack": {PACKS[i]: {"packs": st["packs"][i], "eth": round(st["eth"][i], 3)} for i in range(5)},
            "diamond_share_pct": st["eth"][4] / total * 100 if total else 0,
            "top10_share_pct": sum(top) / total * 100 if total else 0}


def farmer_flow_multiple(presale_eth: float, farmer_share: float, pool_depth_eth: float,
                         farmer_fee_pct: float = 6.0, ev_x: float = 0.995) -> dict:
    """Illustration: constant-product price multiple after the presale's crops are sold to the Farmer.
    pool_depth_eth is an ASSUMPTION until the pool is deployed."""
    flow = presale_eth * ev_x * (1 - farmer_fee_pct / 100) * farmer_share
    cum, out = 0.0, {}
    for label, share in (("commons ~0.5h", 0.226), ("uncommons ~1h", 0.312), ("rares ~1.6h", 0.241),
                         ("epics ~2h", 0.121), ("legendary ~3h", 0.075), ("mythic ~5h", 0.025)):
        cum += share * flow
        out[label] = (1 + cum / pool_depth_eth) ** 2
    return {"farmer_buy_flow_eth": flow, "price_multiple_after": out}
