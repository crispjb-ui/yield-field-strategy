# Open Questions

Docs read 2026-10-30. Resolved items moved to `01_VERIFIED_FACTS.md`. What remains is
either redacted (███) until its stage goes live, or an owner input.

## Redacted in the docs — becomes observable at each stage
| # | Unknown | Stage | Where it will appear | mechanics.yaml key |
|---|---|---|---|---|
| 3 | Fertilizer clearing price in ETH | Staking launch (speculative), farming day 1 (real) | OpenSea item sales | `fert.price_eth` |
| 4 | ~~Staking address~~ known. Fert claims are off-chain (in-app, authenticated); no operator role in the ABI. Automation of claims requires the game session cookie, not a key | — | — |
| 5 | Pack prices, seed odds, worth multiples | Farming launch | seeds-and-crops page | `seeds.*` |
| 6 | Grow-time range; slots per plot | Farming launch | growing-and-selling | `farm.*` |
| 7 | Farmer % / Broker % / Co-op Dues % | Farming launch | growing-and-selling, fees-and-risks | `farm.*` |
| 8 | `$YIELD` supply, taxes, contract, pool depth | Token launch | yield page, official-links | `token.*` |
| 9 | ~~Claim fee~~ 10% on-chain, split 50/50. Windfall % by tier still redacted (`jackpotCurve`=(0,1000); `quoteBurnForJackpot` quotes 0 while Silo is empty) | Deed-rewards stage | silo page | `silo.windfall_pct_by_tier` |
| 10 | Farmers Co-op rules, day-1 seed amount, "classified" volume mechanism, truffles | Farming launch | co-op pages, classified | — |
| 11 | Dates for any stage | — | `@YieldFields_RH` | `stage` |

## Owner inputs
| # | Input | Used for |
|---|---|---|
| 12 | ~~Token IDs~~ #537, #660, #661 (verified staked, Fertility 6) | — |
| 13 | ~~Wallet~~ `0x139e…3952` (from `deedOf`) | — |
| 14 | Hold horizon; max tolerable drawdown on the $8k | stop rules in strategy §3 |
| 15 | Whether a dedicated hot wallet for staking/claims is acceptable (see automation plan Phase 3) | automation scope |
| 16 | ETH/USD on 2026-10-13 | USD cost basis only |
