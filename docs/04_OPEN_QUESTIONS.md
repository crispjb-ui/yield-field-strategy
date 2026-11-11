# Open Questions

Docs read 2026-10-30. Resolved items moved to `01_VERIFIED_FACTS.md`. What remains is
either redacted (███) until its stage goes live, or an owner input.

## Redacted in the docs — becomes observable at each stage
| # | Unknown | Stage | Where it will appear | mechanics.yaml key |
|---|---|---|---|---|
| 3 | Fertilizer clearing price in ETH | Staking launch (speculative), farming day 1 (real) | OpenSea item sales | `fert.price_eth` |
| 4 | ~~Staking address~~ known. Fert claims are off-chain (in-app, authenticated); no operator role in the ABI. Automation of claims requires the game session cookie, not a key | — | — |
| 5 | ~~Pack prices, odds, worth~~ testnet defaults known (mirror); confirm from Cornhub contract at launch | Farming launch | `packPrices()` | `seeds.*` |
| 6 | ~~Grow times; slots~~ known: 1–12 h formula; 25 slots per wallet | — | — | — |
| 7 | Farmer/Market fee: 10% testnet default; mainnet Farmer fee said to be lower | Farming launch | `farmerFeeBps()`, `marketFeeBps()` | `farm.*` |
| 8 | `$YIELD` supply, taxes, contract, pool depth | Token launch | yield page, official-links | `token.*` |
| 9 | ~~Claim fee, Windfall~~ 10% fee 50/50; Windfall = F×10% (Rare 60%) | — | — | — |
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

## New unknowns (2026-11-11)
| # | Unknown | Why it matters |
|---|---|---|
| 17 | Launch seed size and daily release; claim limit | Sets tonight's budget B for the first 30 days, i.e. whether cycling is +EV at all |
| 18 | Truffle Pig price | Fixed cost per wallet before any truffle |
| 19 | Mainnet Farmer fee (docs: lower than Market) and normal buy tax | `farmer_vs_direct()` breakeven |
| 20 | Pool ETH reserve at launch | How much can go through the Farmer per clip under 3% slippage |
| 21 | Farmer open date | Whether day-1 harvests can be sold for $YIELD or must be held |
| 22 | Deed reward pool funding | Size of the deed $YIELD stream; Silo fill rate |
