# Yield Fields — Strategy & Automation

Private working repo for a position in **Yield Fields** (Robinhood Chain farming game,
3,333 "Founding Deeds", `$YIELD` token) and the tooling around it.

Status (2026-10-30): primary sources (`yieldfields.fun/docs`, `opensea.io`,
`robinhoodchain.blockscout.com`, `x.com`) were **unreachable** from the build
session. Everything in `docs/` is split into *verified from secondary sources*
vs *unverified*. Nothing in the strategy assumes a game mechanic that has not
been read in the docs; those parameters live in `config/mechanics.yaml` as
`null` until filled.

| Path | What |
|---|---|
| `docs/01_VERIFIED_FACTS.md` | Fact ledger with sources and confidence |
| `docs/02_STRATEGY_FRAMEWORK.md` | Game summary, decision rules, $8k allocation, exit plan, risk register |
| `docs/03_AUTOMATION_PLAN.md` | Infrastructure build plan, phased |
| `docs/04_OPEN_QUESTIONS.md` | Exact questions the docs must answer before capital is deployed |
| `config/settings.example.yaml` | Chain / API / contract config (copy to `config/settings.yaml`) |
| `config/mechanics.yaml` | Game-mechanics parameters (all `null` until read from docs) |
| `yf/` | Python package: RPC, OpenSea, Blockscout clients; ledger; ROI model; CLI |
| `data/ledger.csv` | Your positions (cost basis, token ids) — create from `ledger.example.csv` |

## Quick start

```bash
pip install -r requirements.txt
cp config/settings.example.yaml config/settings.yaml   # fill contract addresses + API key
cp data/ledger.example.csv data/ledger.csv            # fill your 3 deeds
python -m yf.cli market        # OpenSea floor / best offer / 24h volume snapshot
python -m yf.cli positions     # mark-to-floor P&L for the ledger
python -m yf.cli roi           # seed-vs-deed ROI once mechanics.yaml is filled
python -m yf.cli watch         # loop: snapshot + alert on thresholds
pytest
```

## Rules this repo enforces on itself
1. No mechanic is modelled until it is quoted from `yieldfields.fun/docs` with a URL in `docs/01_VERIFIED_FACTS.md`.
2. No private key is ever stored here. Read-only tooling only; signing happens in a wallet you control.
3. Any token/contract address is confirmed on the official X account **and** the Blockscout explorer before it goes in `settings.yaml`.
