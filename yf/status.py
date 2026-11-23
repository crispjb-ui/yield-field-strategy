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
from . import probe as probe_mod

ROOT = config.ROOT
SNAP = ROOT / "data" / "snapshots"
KNOWN_ADDRESSES = {
    "0x231142e88f523b0a4f46d2d79faab2ce1828e43a",  # deeds
    "0x0acfcd1483686fcd94dabea03714321d0e05fc8d",  # staking
    "0xd9d6d0557f3479e801a967eb693ebe1ada6e5317",  # items
    "0x8c1e23bc90f88ddc8cba7256798acbd745072524",  # cornhub (game mainnet config, 2026-11-23)
}
ALL_DOC_PAGES = (
    "reference/official-links-and-contracts", "reference/patch-notes", "reference/fees-and-risks", "reference/faq",
    "reference/glossary", "getting-started/about-yield-fields", "getting-started/quick-start",
    "getting-started/whats-coming", "deed-gameplay/founding-deeds", "deed-gameplay/staking-and-the-fert-deck",
    "deed-gameplay/fertilizer", "deed-gameplay/the-root-cellar", "deed-gameplay/the-silo-and-the-windfall",
    "farming-and-yield/seeds-and-crops", "farming-and-yield/growing-and-selling", "farming-and-yield/yield",
    "farming-and-yield/classified", "the-farmers-co-op/how-the-farmers-co-op-works", "the-farmers-co-op/flywheels")
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
    for page in ALL_DOC_PAGES:
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
    new_all = set()
    for v in cur.values():
        new_all |= set(v.get("addresses", [])) - KNOWN_ADDRESSES
    out["new_addresses"] = sorted(new_all)
    return out, alerts


def section_new_contracts(cfg, addrs: list[str]) -> tuple[str, list[str]]:
    if not addrs:
        return "", []
    rpc = Rpc(cfg["chain"]["rpc_url"])
    lines, alerts, found = ["## Newly published contracts"], [], []
    for a in addrs:
        try:
            r = probe_mod.probe(rpc, a)
        except Exception as e:
            r = {"kind": "error", "address": a, "error": str(e)[:80]}
        found.append(r)
        lines.append(f"### {r['kind']} `{a}`")
        lines.append("```json\n" + json.dumps(r, indent=1, default=str) + "\n```")
        if r["kind"] == "cornhub":
            ek = probe_mod.rake_from_cornhub(r)
            lines.append(f"Loop economics at live fees: Market rake {ek['market_rake_pct']:.2f}% per cycle; Farmer beats a direct buy while buy tax > {ek['farmer_breakeven_buy_tax_pct']:.2f}%. Truffle Pig {r['truffle_pig_eth']} ETH. Float {r['float_eth']} ETH.")
            alerts.append(f"CORNHUB LIVE at {a}: farmer fee {r['farmer_fee_pct']}%, market fee {r['market_fee_pct']}%, pig {r['truffle_pig_eth']} ETH")
        if r["kind"] == "yield_pool":
            alerts.append(f"$YIELD POOL LIVE at {a}: buy tax {r['buy_fee_pct']}%, sell tax {r['sell_fee_pct']}% (max {r['max_sell_fee_pct']}%), ETH reserve {r['eth_reserve']:.3f}")
    _append("contracts", {"contracts": found})
    return "\n".join(lines) + "\n", alerts


def section_cornhub(cfg) -> tuple[str, list[str]]:
    from . import cornhub
    rpc = Rpc(cfg["chain"]["rpc_url"], timeout=40)
    c = probe_mod.probe(rpc, cornhub.MAINNET)
    sales = cornhub.scan(rpc, ROOT / "data" / "cornhub_state.json")
    _append("cornhub", {"fees": {k: c.get(k) for k in ("farmer_fee_pct", "market_fee_pct", "pack_fee_pct", "truffle_pig_eth", "paused")},
                        **{k: sales[k] for k in ("balance_eth", "total_paid_eth", "purchases", "unique_buyers", "diamond_share_pct")}})
    alerts = []
    if c.get("kind") == "cornhub":
        if c.get("paused"):
            alerts.append("CornHub is PAUSED")
        if c.get("truffle_pig_eth"):
            alerts.append(f"Truffle Pig on sale: {c['truffle_pig_eth']} ETH")
        if sales["total_paid_eth"] - sales["balance_eth"] > 1:
            alerts.append(f"CornHub balance {sales['balance_eth']:.1f} ETH is below pack sales {sales['total_paid_eth']:.1f} ETH (selling has started or ETH was withdrawn)")
    rows = "\n".join(f"| {k} | {v['packs']:,} | {v['eth']:,.2f} |" for k, v in sales["by_pack"].items())
    md = f"""## CornHub `{cornhub.MAINNET}`
Fees: Farmer {c.get('farmer_fee_pct')}% · Market {c.get('market_fee_pct')}% · pack {c.get('pack_fee_pct')}% · Truffle Pig {c.get('truffle_pig_eth')} ETH · paused={c.get('paused')}

Pack sales: **{sales['total_paid_eth']:,.1f} ETH** from {sales['unique_buyers']:,} wallets in {sales['purchases']:,} purchases · contract balance {sales['balance_eth']:,.1f} ETH · Diamond {sales['diamond_share_pct']:.0f}% · top-10 wallets {sales['top10_share_pct']:.0f}%

| Pack | Packs | ETH |
|---|---|---|
{rows}
"""
    return md, alerts


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
        ch, a = section_cornhub(cfg); alerts += a
        parts.append(ch)
    except Exception as e:
        parts.append(f"## CornHub\nERROR: {e}\n")
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
        try:
            nc, a = section_new_contracts(cfg, dd.get("new_addresses", [])); alerts += a
            if nc:
                parts.append(nc)
        except Exception as e:
            parts.append(f"## Newly published contracts\nERROR: {e}\n")
    except Exception as e:
        parts.append(f"## Docs watch\nERROR: {e}\n")
    parts.insert(1, "## Alerts\n" + ("\n".join(f"- **{x}**" for x in alerts) if alerts else "- none") + "\n")
    return "\n".join(parts), alerts


def _alert_key(a: str) -> str:
    """Condition identity, so a persisting condition does not re-alert every run."""
    if a.startswith("Network Fert rate is"):
        return "network_rate_below_100"
    if a.startswith("CornHub balance"):
        return "cornhub_balance_below_sales"
    if a.startswith("Truffle Pig on sale"):
        return "pig_on_sale"
    if a.startswith("CORNHUB LIVE"):
        return "cornhub_live"
    if a.startswith("$YIELD POOL LIVE"):
        return "yield_pool_live"
    if a.startswith("New contract address"):
        return a
    if a.startswith("Docs page changed"):
        return a   # a new change is a new key only if the page hash moved again (docs_state handles that)
    return a


def main():
    cfg = config.load_settings()
    md, alerts = build(cfg)
    (ROOT / "STATUS.md").write_text(md)
    path = ROOT / "data" / "alerts.json"
    prev = json.loads(path.read_text()) if path.exists() else {}
    prev_keys = set(prev.get("active_keys", []))
    keys = {_alert_key(a): a for a in alerts}
    # docs changes are one-shot: they only appear in `alerts` on the run that saw the hash move
    new = [a for k, a in keys.items() if k not in prev_keys or k.startswith("Docs page changed")]
    cleared = sorted(k for k in prev_keys if k not in keys and not k.startswith("Docs page changed"))
    active_keys = sorted(k for k in keys if not k.startswith("Docs page changed"))
    path.write_text(json.dumps({"ts": datetime.now(timezone.utc).isoformat(), "alerts": alerts,
                                "new_alerts": new, "cleared": cleared, "active_keys": active_keys}, indent=1))
    print(md)
    print(f"\n{len(alerts)} alert(s), {len(new)} new, {len(cleared)} cleared", file=sys.stderr)


if __name__ == "__main__":
    main()
