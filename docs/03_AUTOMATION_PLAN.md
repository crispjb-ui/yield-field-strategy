# Automation Plan

Principle: read-only first, signing never from this repo. Updated 2026-11-04.

## Status
| Item | State |
|---|---|
| Network access | Docs, game API, OpenSea API, Robinhood RPC reachable via the session proxy. Blockscout and Sourcify blocked; all chain reads go through `yf/rpc.py` + `yf/abi.py` with ABIs extracted from the game bundle (`abi/`) |
| Claim reminder | **Live.** Scheduled task `trig_014BCKNZPVfFwhak8pAhRcAU`, "Yield Fields: claim Fertilizer reminder + status", cron `47 2 2-30/2 * *` UTC (every even calendar day at 02:47 UTC; 72 h worst case across a 31-day month end), fresh session, push notification. First run 2026-11-06 02:47 UTC, before the first claim deadline (~08:00 UTC). Each run: `fertrate --save`, `deeds`, both OpenSea stats, docs patch-notes/contracts diff. Read-only, no commits |
| Fert claims | Off-chain, behind the game's wallet-signed login. Not automatable without a key or a copied session cookie. Decision: manual (see `05_OWNER_THESIS.md`). Cookie-replay script available on request |

## Commands (all read-only)
| Command | Does |
|---|---|
| `python -m yf.cli fertrate [--save]` | `/api/fert-rate`: circulation, target, network rate, staked Fertility, projected 7/10/14-day milestones. Alerts when rate < 100% |
| `python -m yf.cli deeds` | `deedOf`/`redeemValue` for #537/#660/#661; staking `backing`, `jackpot`, `rewardPool`, `paused` |
| `python -m yf.cli market [--save]` | Deed collection floor / volumes (no key needed for stats) |
| `python -m yf.cli positions` | Fee-adjusted mark of the ledger (6% exit fee) |
| `python -m yf.cli roi --floor X` | Seed/deed ROI; refuses while mechanics are redacted |
| `python -m yf.cli watch [--once]` | Poll market + thresholds |

## Phase 2 — when farming / `$YIELD` launch (build on the day)
1. Fill `config/mechanics.yaml` from the un-redacted docs pages and from the
   deployed contracts (`abi/abi_2.json` Cornhub: `packPrices`, `farmerFeeBps`,
   `marketFeeBps`, `packFeeBps`, `trufflePigFee`; `abi/abi_3.json` pool:
   `buyFeeBps`, `sellFeeBps`, `maxSellFeeBps`, `ethReserve`,
   `virtualEthReserve`, `spotPrice`; `abi/abi_4.json` vester:
   `EMISSION_TOTAL`, `vestingRate`, `dailyCap`; `abi/abi_6.json` buyback:
   `DAILY_RATE_BPS`, `pool`, `trufflePool`).
2. Run `seed_pack_ev()` and `farm_vs_buy()` the same day; choose route per
   `05_OWNER_THESIS.md`.
3. Add `pool` and `coop` CLI commands: spot price, reserves, current sell
   tax, buyback spendable, truffle pool balance. Alert on `maxSellFeeBps`
   regime, LP reserve drops, owner/upgrade events (`Upgraded`,
   `OwnershipTransferred` on all proxies).
4. Fert market tape from OpenSea events for `yield-fields-items` once an API
   key is set; 24 h VWAP in USDG and ETH.
5. Burn-vs-sell each poll via `quoteBurnForJackpot` once `jackpot` > 0.

## Phase 3 — acting (only with explicit owner approval, never from this repo)
- Farming actions (buy packs, plant, fertilize, harvest, sell) are in-app
  API calls plus wallet signatures for purchases. A cookie-replay script can
  plant/fertilize/harvest without a key; purchases and sells need a
  signature. If launch-window throughput justifies it, run that script on
  the owner's own machine with the owner's browser session, not here.
- `$YIELD` sells per the thesis rules are manual, sized ≤2% of pool depth.

## Not building
- Key-holding bots. Multi-wallet farming (terms unpublished).
- Automated NFT selling into a thin book.
