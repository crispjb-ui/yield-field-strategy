"""Read CornHub pack sales from chain: PacksPurchased logs → totals by pack, buyers, timeline."""
import json, sys, time
from collections import Counter, defaultdict
from yf.rpc import Rpc, _keccak
C = sys.argv[1] if len(sys.argv) > 1 else "0x8C1e23Bc90F88DdC8CBA7256798aCbD745072524"
WALLET = "0x139e79b0d01148712528d56625a2a59f676e3952"
PACKS = ["Bronze", "Silver", "Gold", "Platinum", "Diamond"]
r = Rpc("https://rpc.mainnet.chain.robinhood.com", timeout=40)
topic = "0x" + _keccak(b"PacksPurchased(address,uint8,uint32,uint256)").hex()
latest = r.block_number()
bal = r.balance_eth(C)
deploy = max(latest - int(sys.argv[2]) if len(sys.argv) > 2 else latest - 8_000_000, 0)   # scan window start (no archive state on the public RPC)
ts = lambda b: int(r.call("eth_getBlockByNumber", [hex(b), False])["timestamp"], 16)
logs, step, b = [], 500_000, deploy
while b <= latest:
    e = min(b + step - 1, latest)
    try:
        logs += r.call("eth_getLogs", [{"address": C, "topics": [topic], "fromBlock": hex(b), "toBlock": hex(e)}]); b = e + 1
    except Exception as ex:
        if step <= 2000: raise
        step //= 4
qty, paid, buyers, mine = Counter(), defaultdict(float), Counter(), []
for l in logs:
    who = "0x" + l["topics"][1][-40:]; pid = int(l["topics"][2], 16); d = l["data"][2:]
    q, p = int(d[:64], 16), int(d[64:128], 16) / 1e18
    qty[pid] += q; paid[pid] += p; buyers[who] += p
    if who.lower() == WALLET: mine.append((int(l["blockNumber"], 16), PACKS[pid], q, p))
t0, t1 = ts(deploy), ts(latest)
out = {"cornhub": C, "scan_from_block": deploy, "scan_from_utc": time.strftime("%Y-%m-%d %H:%M", time.gmtime(t0)),
       "as_of_utc": time.strftime("%Y-%m-%d %H:%M", time.gmtime(t1)), "contract_balance_eth": round(bal, 4),
       "purchases": len(logs), "unique_buyers": len(buyers), "total_paid_eth": round(sum(paid.values()), 4),
       "by_pack": {PACKS[i]: {"packs": qty[i], "eth": round(paid[i], 4)} for i in sorted(qty)},
       "top10_buyers_eth": [round(v, 3) for _, v in buyers.most_common(10)],
       "top10_share_pct": round(sum(v for _, v in buyers.most_common(10)) / max(sum(paid.values()), 1e-9) * 100, 1),
       "median_buyer_eth": round(sorted(buyers.values())[len(buyers) // 2], 4) if buyers else 0,
       "owner_wallet_purchases": mine}
if logs:
    first, last = ts(int(logs[0]["blockNumber"], 16)), ts(int(logs[-1]["blockNumber"], 16))
    out["first_sale_utc"] = time.strftime("%Y-%m-%d %H:%M", time.gmtime(first)); out["last_sale_utc"] = time.strftime("%Y-%m-%d %H:%M", time.gmtime(last))
    day = Counter()
    for l in logs:
        day[int(l["blockNumber"], 16)] += 0
    # per-day totals via block→time interpolation
    perday = defaultdict(float)
    for l in logs:
        bn = int(l["blockNumber"], 16); t = t0 + (t1 - t0) * (bn - deploy) / max(latest - deploy, 1)
        perday[time.strftime("%m-%d", time.gmtime(t))] += int(l["data"][2:][64:128], 16) / 1e18
    out["eth_per_day_approx"] = {k: round(v, 2) for k, v in sorted(perday.items())}
print(json.dumps(out, indent=1))
