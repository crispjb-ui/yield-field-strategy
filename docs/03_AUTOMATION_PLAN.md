# Automation Plan

Principle: read-only first, signing last. No private key touches this repo.

## Phase 0 — Unblock (owner action, today)
Allow these hosts in the cloud environment's network settings (Limited level,
Allowed domains): `yieldfields.fun`, `opensea.io`, `api.opensea.io`,
`robinhoodchain.blockscout.com`, `rpc.mainnet.chain.robinhood.com`,
`x.com`, `api.coingecko.com`. Then re-run the docs read and fill
`config/mechanics.yaml`.

## Phase 1 — Observe (built in this repo, runs today where hosts allow)
| Module | Does | Needs |
|---|---|---|
| `yf/opensea.py` | Collection stats, listings, best offers, events for `yield-field-deeds`; per-token trait lookup | OpenSea API key, chain slug (Q: `/api/v2/chains`) |
| `yf/blockscout.py` | Contract ABI, token transfers, holder counts, tx list for a wallet | Deed/token addresses |
| `yf/rpc.py` | Raw JSON-RPC: `eth_call`, block number, balances; minimal ABI encoder for `balanceOf`/`ownerOf`/`tokenURI` | RPC URL |
| `yf/ledger.py` | Positions, cost basis, mark-to-floor P&L in ETH and USD | `data/ledger.csv` |
| `yf/roi.py` | Seed-vs-deed payback model from `mechanics.yaml`; refuses to run on nulls | Filled mechanics |
| `yf/cli.py` | `market`, `positions`, `roi`, `watch` (poll + threshold alerts, JSONL snapshots) | — |

Scheduling: a Claude Code Remote scheduled task (fresh session, every 4–6 h)
runs `python -m yf.cli watch --once` and reports deviations. Set up after
Phase 0.

## Phase 2 — Model (after docs are read)
1. Encode every mechanic in `mechanics.yaml` with the docs URL.
2. Extend `roi.py` with weather states and leaderboard EV.
3. Build a Fert price tracker if there is an open market (read the market
   contract's events via Blockscout; derive clearing price per cycle).
4. Backtest the §3 rules of the strategy against the first two weeks of
   on-chain data before scaling capital.

## Phase 3 — Act (only if deed loop needs per-cycle actions)
1. Dedicated hot wallet holding gas only; deeds stay in the cold wallet and
   are **delegated** if the game supports delegation (Q21); otherwise the
   hot wallet holds the deeds and nothing else.
2. A signer service outside this repo (local machine or a locked-down VM)
   with: cycle scheduler, dry-run simulation via `eth_call` before every
   send, max-gas cap, daily tx-count cap, and a kill switch file.
3. Fert selling: post asks per §4 of the strategy; never market-sell.
4. Harvest-to-ETH: per R5, swap a fixed share through the verified DEX
   router with slippage ≤1%; abort if pool depth < 50× order size.

## Phase 4 — Exit automation
Alert-only. The kill-table triggers in strategy §5.2 fire notifications; the
human executes sells. Automated selling of NFTs into a thin book is a way to
donate to snipers.

## Not building
- Multi-wallet farming bots: not until per-wallet caps (Q10) are known, and
  only if the terms of service permit it.
- Anything that stores keys, seed phrases, or signs from this environment.
