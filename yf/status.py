"""Build STATUS.md and append JSONL snapshots. Runs in GitHub Actions (no secrets needed)."""
from __future__ import annotations
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

from . import config, fertrate
from .abi import Contract
from .rpc import Rpc, selector, enc_uint

ROOT = config.ROOT
SNAP = ROOT / "data" / "snapshots"
KNOWN_ADDRESSES = {
    "0x231142e88f523b0a4f46d2d79faab2ce1828e43a",  # deeds
    "0x0acfcd1483686fcd94dabea03714321d0e05fc8d",  # staking
    "0xd9d6d0557f3479e801a967eb693ebe1ada6e5317",  # items
}
OWNER = "0x139e79b0d01148712528d56625a2a59f676e3952"
DEEDS = [537, 660, 661]


def _get(url, **kw):
    r = requests.get(url, timeout=25, headers={"accept": "application/json", "user-agent": "yf-status/1.0"}, **kw)
    r.raise_for_status()
    return r


def _append(name: str, obj: dict):
    SNAP.mkdir(parents=True, exist_ok=True)
    obj = dict(obj, ts=datetime.now(timezone.utc).isoformat(timespec="seconds"))
    with open(SNAP / f"{name}.jsonl", "a") as f:
        f.write(json.dumps(obj, default=str) + "\n")


def section_fert() -> tuple[dict, list[str]]:
    fr = fertrate.fetch()
    s = fertrate.summarize(fr)
    m = fertrate.milestones(fr["supply"], s["network_output_per_day"])
    _append("fert-rate", fr)
    alerts = []
    if s["network_rate"] < 1.0:
        alerts.append(f"Network Fert rate is {s['network_rate']:.0%}")
    return {**s, "milestones": m}, alerts


def section_deeds(cfg) -> tuple[dict, list[str]]:
    rpc = Rpc(cfg["chain"]["rpc_url"])
    S = Contract(rpc, cfg["contracts"]["deed_staking"], "stakeAndBuild")
    rows, alerts = [], []
    for t in DEEDS:
        own, fert, struct, flag = S.call("deedOf", t)
        rv = int(rpc.eth_call(S.address, selector("redeemValue(uint256[])") + enc_uint(32) + enc_uint(1) + enc_uint(t)), 16) / 1e18
        rows.append({"id": t, "staker": own, "fertility": fert, "structure": struct, "root_cellar_eth": rv})
        if own.lower() != OWNER:
            alerts.append(f"Deed #{t} is no longer staked by the owner wallet (staker={own})")
        if struct != 1:
            alerts.append(f"Deed #{t} has no Fert Deck (structure={struct})")
    g = {"backing_eth": S.call("backing") / 1e18, "jackpot": S.call("jackpot"), "reward_pool": S.call("rewardPool"),
         "paused": S.call("paused"), "yield_token": S.call("yieldToken"), "wallet_eth": rpc.balance_eth(OWNER)}
    if g["paused"]:
        alerts.append("Staking contract is PAUSED")
    if g["yield_token"] != "0x" + "0" * 40:
        alerts.append(f"$YIELD token set on staking contract: {g['yield_token']}")
    _append("deeds", {"deeds": rows, **g})
    return {"deeds": rows, **g}, alerts


def section_markets() -> tuple[dict, list[str]]:
    out = {}
    for slug in ("yield-field-deeds", "yield-fields-items", "genesishero-abstract", "och-ringbearer"):
        try:
            d = _get(f"https://api.opensea.io/api/v2/collections/{slug}/stats").json()
            t = d["total"]; day = next((i for i in d["intervals"] if i["interval"] == "one_day"), {})
            out[slug] = {"floor": t.get("floor_price"), "symbol": t.get("floor_price_symbol"),
                         "sales_24h": day.get("sales"), "volume_24h": day.get("volume"), "owners": t.get("num_owners")}
        except Exception as e:
            out[slug] = {"error": str(e)[:80]}
    _append("markets", out)
    return out, []


def section_docs() -> tuple[dict, list[str]]:
    alerts, out = [], {}
    state_path = ROOT / "data" / "docs_state.json"
    prev = json.loads(state_path.read_text()) if state_path.exists() else {}
    cur = {}
    for page in ("reference/official-links-and-contracts", "reference/patch-notes", "farming-and-yield/yield",
                 "farming-and-yield/seeds-and-crops"):
        try:
            html = _get(f"https://yieldfields.fun/docs/{page}").text
            text = re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>|<style.*?</style>", "", html, flags=re.S))
            text = re.sub(r"\s+", " ", text)
            h = hashlib.sha256(text.encode()).hexdigest()[:16]
            addrs = set(a.lower() for a in re.findall(r"0x[0-9a-fA-F]{40}", text))
            cur[page] = {"hash": h, "addresses": sorted(addrs)}
            if page in prev and prev[page]["hash"] != h:
                alerts.append(f"Docs page changed: {page}")
            new = addrs - KNOWN_ADDRESSES
            if new:
                alerts.append(f"New contract address on {page}: {', '.join(sorted(new))}")
            m = re.search(r"Updated (\d{1,2} \w+ \d{4})", text)
            cur[page]["updated"] = m.group(1) if m else None
        except Exception as e:
            cur[page] = {"error": str(e)[:80]}
    state_path.write_text(json.dumps(cur, indent=1))
    out["pages"] = cur
    return out, alerts


def build(cfg) -> tuple[str, list[str]]:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    alerts: list[str] = []
    parts = [f"# Yield Fields status\n\n_Auto-generated {now} by `.github/workflows/monitor.yml`. Read-only. Do not edit by hand._\n"]
    try:
        f, a = section_fert(); alerts += a
        ms = f["milestones"]
        parts.append(f"""## Fertilizer network
| Circulation | Days of output | Network rate | Output/day | Staked Fertility |
|---|---|---|---|---|
| {f['circulation']:,} | {f['days_in_circulation']:.2f} | {f['network_rate']:.0%} | {f['network_output_per_day']:,.0f} | {f['staked_fertility']:,.0f} |

Projected (nothing consumed): slowdown starts in {ms['to_7d_slowdown_start']} d, 70% in {ms['to_10d_70pct']} d, 50% floor in {ms['to_14d_50pct']} d.
""")
    except Exception as e:
        parts.append(f"## Fertilizer network\nERROR: {e}\n"); alerts.append(f"fert-rate fetch failed: {e}")
    try:
        d, a = section_deeds(cfg); alerts += a
        rows = "\n".join(f"| #{r['id']} | {r['fertility']} | {'Fert Deck' if r['structure']==1 else r['structure']} | {'owner' if r['staker'].lower()==OWNER else r['staker']} | {r['root_cellar_eth']:.5f} |" for r in d["deeds"])
        parts.append(f"""## Deeds (#537, #660, #661)
| Deed | Fertility | Structure | Staker | Root Cellar ETH |
|---|---|---|---|---|
{rows}

Staking: paused={d['paused']} · backing {d['backing_eth']:.2f} ETH · jackpot {d['jackpot']} · rewardPool {d['reward_pool']} · yieldToken {d['yield_token']} · owner wallet {d['wallet_eth']:.4f} ETH
""")
    except Exception as e:
        parts.append(f"## Deeds\nERROR: {e}\n"); alerts.append(f"deeds read failed: {e}")
    try:
        m, a = section_markets(); alerts += a
        rows = "\n".join(f"| {k} | {v.get('floor')} {v.get('symbol','')} | {v.get('sales_24h')} | {v.get('volume_24h')} |" if "error" not in v else f"| {k} | error | | |" for k, v in m.items())
        parts.append(f"""## Markets (OpenSea)
| Collection | Floor | 24h sales | 24h volume |
|---|---|---|---|
{rows}
""")
    except Exception as e:
        parts.append(f"## Markets\nERROR: {e}\n")
    try:
        dd, a = section_docs(); alerts += a
        rows = "\n".join(f"| {k} | {v.get('updated')} | {len(v.get('addresses', []))} |" if "error" not in v else f"| {k} | error | |" for k, v in dd["pages"].items())
        parts.append(f"""## Docs watch
| Page | "Updated" | Addresses on page |
|---|---|---|
{rows}
""")
    except Exception as e:
        parts.append(f"## Docs watch\nERROR: {e}\n")
    parts.insert(1, "## Alerts\n" + ("\n".join(f"- **{x}**" for x in alerts) if alerts else "- none") + "\n")
    return "\n".join(parts), alerts


def main():
    cfg = config.load_settings()
    md, alerts = build(cfg)
    (ROOT / "STATUS.md").write_text(md)
    (ROOT / "data" / "alerts.json").write_text(json.dumps({"ts": datetime.now(timezone.utc).isoformat(), "alerts": alerts}, indent=1))
    print(md)
    print(f"\n{len(alerts)} alert(s)", file=sys.stderr)


if __name__ == "__main__":
    main()
