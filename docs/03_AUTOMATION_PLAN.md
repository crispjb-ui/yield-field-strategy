# Automation Plan

Principle: read-only first, signing last. No private key touches this repo.

## Phase 0 — Unblock (done 2026-10-30)
Docs, OpenSea API and the RPC are reachable through the session proxy.
Blockscout answers scripts with a Cloudflare challenge: all chain reads go
through `yf/rpc.py` (verified against the deed contract).

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
runs `python -m yf.cli watch --once` and reports deviations.

**Stage One specific (build next, before staking opens):**
1. **Claim-cadence monitor.** Storage caps at 72 h; a deck that is full earns
   nothing. Alert at 60 h since the last claim tx from the owner wallet
   (read via RPC: staking contract events once its address is published).
   Until then, a fixed 60 h scheduled reminder.
2. **Output-rate derivation.** From two consecutive claims, compute Fert units
   per day for Fertility 6 and write `deed.output_per_cycle`. This single
   number turns every deed-yield question into arithmetic.
3. **Fert market tape.** Once the items contract is published: poll OpenSea
   events for the Fertilizer token id, record each sale (price, qty, buyer),
   maintain a 24 h VWAP in ETH. Feeds `fert_deed_yield()`.
4. **Deed-floor by tier.** Extend `market` to pull best listings per Tier
   trait (needs API key) so the tier relative-value table updates itself.
5. **Burn-vs-sell.** Once staking contract ABI is known: read Root Cellar per
   deed and Silo balance; run `burn_vs_sell()` each poll; alert when it flips.

## Phase 2 — Model (after docs are read)
1. Encode every mechanic in `mechanics.yaml` with the docs URL.
2. Extend `roi.py` with weather states and leaderboard EV.
3. Build a Fert price tracker if there is an open market (read the market
   contract's events via Blockscout; derive clearing price per cycle).
4. Backtest the §3 rules of the strategy against the first two weeks of
   on-chain data before scaling capital.

## Phase 3 — Act (the deed loop DOES need per-cycle actions: a claim every ≤72 h)
1. Check the published staking ABI for an operator/claimer role. If one
   exists: deeds stay in the cold wallet, a hot wallet holding gas only
   claims. If none: a dedicated hot wallet holds the 3 deeds (staked, so the
   staking contract custodies them; the hot key can only claim, unstake,
   burn) and nothing else. Owner decides (open question 15). Manual claiming
   every 2.5 days is viable for 3 deeds; automation matters at scale.
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
