# Yield Fields — Strategy & Automation

Private working repo for a position in **Yield Fields** (Robinhood Chain farming game,
3,333 "Founding Deeds", `$YIELD` token) and the tooling around it.

Status (2026-10-30): official docs read in full (snapshot in `docs/source/`),
OpenSea API and Robinhood Chain RPC verified live. `config/mechanics.yaml`
holds every published number; `null` means the docs redact it until that
stage launches. Stage One (staking + Fert Deck) is the only live loop.

| Path | What |
|---|---|
| **`STATUS.md`** | **Live status page**, rebuilt every 6 h by GitHub Actions: Fert network, deeds, markets, docs watch, alerts |
| `.github/workflows/` | `monitor.yml` (6-hourly status + snapshots + alert issues) · `claim-reminder.yml` (every 2 days opens a "CLAIM FERTILIZER" issue) |
| `data/snapshots/*.jsonl` | Time series appended by the monitor (fert-rate, deeds, markets) |
| `docs/00_HANDOFF.md` | **Start here** in a new session: position, reading order, tooling, scheduled task, next triggers |
| `docs/01_VERIFIED_FACTS.md` | Fact ledger with sources and confidence |
| `docs/02_STRATEGY_FRAMEWORK.md` | Game summary, decision rules, $8k allocation, exit plan, risk register |
| `docs/03_AUTOMATION_PLAN.md` | Infrastructure build plan, phased |
| `docs/05_OWNER_THESIS.md` | Owner's token thesis, the docs-based challenge to it, and the operating rules in force |
| `docs/07_LAUNCH_ECONOMICS_2026-11-11.md` | Pack EV, rake, truffle payout math, Farmer-vs-direct, Windfall race, launch-day playbook |
| `docs/06_OCH_DEVLOG_2026-11-09.md` | OCH devlog analysis vs the owner's heroes / Ringbearers / weapons; actions |
| `docs/04_OPEN_QUESTIONS.md` | Exact questions the docs must answer before capital is deployed |
| `config/settings.example.yaml` | Chain / API / contract config (copy to `config/settings.yaml`) |
| `config/mechanics.yaml` | Game-mechanics parameters from the docs (`null` = redacted) |
| `docs/source/` | Verbatim text snapshot of the official docs, dated |
| `yf/` | Python package: RPC, OpenSea, Blockscout clients; ledger; ROI model; CLI |
| `data/ledger.csv` | Your positions (cost basis, token ids) — create from `ledger.example.csv` |

## Notifications
GitHub Issues are the notification channel, independent of any Claude subscription: watch this repository (Watch → Custom → Issues) and GitHub emails/pushes you each `claim` and `alert` issue.

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
