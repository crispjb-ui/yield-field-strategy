# Verified Facts Ledger

Last updated: 2026-10-30 (docs read directly; full text snapshot in `docs/source/`). Confidence scale: **A** = official source or ≥2
independent reports agree; **B** = single secondary report; **C** = unverified /
lookalike / third-party claim. Primary sources (yieldfields.fun, opensea.io,
x.com, blockscout) could not be fetched from the build session; everything
below came through search-engine summaries of those pages. Re-verify A/B items
against the docs directly before acting.

## From the official docs (grade A — read directly 2026-10-30, every page "Updated 30 Oct 2026")

Source pages: `https://yieldfields.fun/docs/<section>/<page>`. Docs state all numbers are subject to change with notice.

| Fact | Page |
|---|---|
| Stage One (live first): deed staking, Fert Deck, Fertilizer, export. Then farming + `$YIELD` + Farmers Co-op. Then deed rewards, Silo, burns. **No dates published.** | getting-started/whats-coming |
| **Fertility by tier: Common 5 (Meadow), Rare 6 (Frost), Epic 7 (Blight), Legendary 8 (Radiant), Mythic 9 (Astral).** Same Fertility within a tier. Mythic = 1.8× Common. Art is cosmetic. | deed-gameplay/founding-deeds |
| Fertility sets: Fert Deck output (now); Root Cellar share, claim-fee rebate share, Windfall share, one classified use (later) | founding-deeds |
| Deed contract `0x231142E88f523B0a4F46D2D79FAAB2cE1828E43a`, ERC-721C, 5% royalty to project treasury (not team) | reference/official-links-and-contracts |
| Staking: free (gas), many deeds per tx, stake+build in one step. Staked deed cannot be sold. **Unstaking destroys the structure.** Unstake blocked while game paused. | deed-gameplay/staking-and-the-fert-deck |
| Fert Deck: 0.01 ETH at launch (may change), fee stays in staking contract as Root Cellars. 1 structure per deed. Output scales with Fertility. **Storage = 3 days of production; deck stops when full.** Partial progress carries. | staking-and-the-fert-deck |
| **Fert output rate per Fertility point: NOT PUBLISHED.** | — |
| Fertilizer: each cuts 25% of total grow time, max 2 per crop (50%); one with <25% left ripens instantly; consumed on use; never expires; ERC-1155C, 5% royalty; export to wallet → trade on OpenSea → import to use. Export live at staking launch. | deed-gameplay/fertilizer |
| Root Cellar: per-deed ETH pot in the staking contract, funded by build fees now and a share of `$YIELD` taxes later; share by Fertility; **collected only by burning a staked deed**; no set amount. | deed-gameplay/the-root-cellar |
| Silo: `$YIELD` pot funded by a ███% claim fee on deed rewards; Windfall = tier-set share (███% each, redacted) of the Silo on burn; burns sequential; min-payout guard; **burn is permanent**. | deed-gameplay/the-silo-and-the-windfall |
| Seed packs (Bronze→Diamond), ETH prices redacted; same odds in every pack; 6 seed rarities with redacted odds and worth-multiples; Common worth < pack; **"splitting ETH across lots of small packs never beats 1 bigger pack"**; drand randomness; seeds tradeable. | farming-and-yield/seeds-and-crops |
| Farm plot: free fixed grid of slots per wallet, no expansions, no deed needed; grow ███–███ h; rarer = longer, bigger pack = faster; ripe crops never wilt. | farming-and-yield/growing-and-selling |
| Selling: Farmer pays ███% in `$YIELD` (executes a buy on the official pool, skips buy tax, lower dues); Broker pays ███% in ETH **from Cornhub pack-sale ETH**. Farmer→sell-`$YIELD` nets less than Broker. | growing-and-selling |
| `$YIELD`: ERC-20, fixed supply (redacted), 0% team, one official Uniswap v4 pool (URC-5, copycat pools blocked), buy/sell tax redacted with hard-coded caps, dynamic sell tax during heavy net selling, decaying launch buy tax. Taxes → Farmers Co-op + Root Cellars + small team cut. | farming-and-yield/yield |
| Farmers Co-op: funded by Co-op Dues on every crop sale + tax share + future Fert Deck boost fees; seeded with ████ on farming day 1; rules unpublished; "some of it may never come back out". | the-farmers-co-op/* |
| Team revenue: share of mint + small cut of regular taxes only. | reference/fees-and-risks |
| **Governance: team multisig, changes immediate, no timelock; contracts upgradeable incl. deed staking ("updates apply to staked deeds too"); external audit planned, not done; team manages the LP and "can add, remove or rebalance it".** Staking contract cannot move a staked deed. | fees-and-risks |
| Classified: truffles ("something in the soil"), the volume-incentive mechanism, an extra deed reward stream, Fert Deck boosts, new structures. | classified, flywheels |
| Official: `yieldfields.fun`, `@YieldFields_RH`, `discord.gg/onchainheroes`. Everything else is a scam per the docs. Earlier "weather / weekly leaderboard" claims came from lookalike sites and are **not in the docs**. | official-links-and-contracts |

## Live API checks (2026-10-30)

| Fact | Source |
|---|---|
| RPC `eth_chainId` = 4663; deed contract `name()` = "Yield Field Deeds", `totalSupply()` = 3333 | `rpc.mainnet.chain.robinhood.com` via `yf/rpc.py` |
| OpenSea chain slug = `robinhood`; collection `safelist_status: verified`; fees: 1.0% OpenSea + 5.0% creator → **6% total exit fee** (earlier 7.5% assumption corrected) | `api.opensea.io/api/v2/collections/yield-field-deeds` |
| Stats: floor 0.875 ETH, 1,208 owners, 1,341 sales / 1,386 ETH total; 24h 39 sales / 38.8 ETH; 7d 171 sales / 174 ETH | `/collections/yield-field-deeds/stats` (no API key needed) |
| Blockscout explorer returns a Cloudflare challenge to scripts | — |

## Project (secondary sources, pre-docs)

| Fact | Conf | Source |
|---|---|---|
| Yield Fields is an on-chain farming game on Robinhood Chain; players plant seeds and harvest `$YIELD` | A | [X post](https://x.com/ice_bearcute/status/2100065855073927661), [BlockchainGamerBiz](https://www.blockchaingamer.biz/news/43058/yield-fields-sells-8-million-nfts-30-seconds/) |
| Official X account: `@YieldFields_RH`; official site: `yieldfields.fun` | A | [X](https://x.com/yieldfields_rh), [web3raider](https://www.web3raider.com/news/yield-fields-deeds-mint-sold-out-robinhood-chain-oct-2026) |
| 3,333 "Founding Deeds", randomized rarity and metadata; each deed = ownership of a plot of land in-game | A | [Official X](https://x.com/YieldFields_RH/status/2099575499001663715), [OpenSea](https://opensea.io/collection/yield-field-deeds) |
| Anyone can farm without a deed; deed holders have a **separate loop that generates resources through gameplay** | A | Official X (above), BlockchainGamerBiz |
| First deed-holder resource is **Fertilizer**, produced via **"Fert Decks"**, which non-deed farmers need | B | [BlockchainGamerBiz](https://www.blockchaingamer.biz/news/43058/yield-fields-sells-8-million-nfts-30-seconds/) |
| Project site mentions an on-chain treasury, a weekly leaderboard, and dynamic weather | B | [TokenPost](https://www.tokenpost.com/news/technology/42960) |
| Whitelist: 850 WL spots earned via an Onchain Heroes "corn" leaderboard campaign | B | [Droply](https://droply.digital/project/yield-fields) |

## Mint

| Fact | Conf | Source |
|---|---|---|
| Public mint 2026-10-13, Dutch auction, 1 ETH → 0.069 ETH over 24 h, mint cap 5 per wallet | A | BlockchainGamerBiz, web3raider |
| Sold out in ~30 seconds; final clearing price **0.999688 ETH** | A | BlockchainGamerBiz, web3raider, official X |
| Over-payers "claim the difference" at `yieldfields.fun/mint` | B | Official X (via web3raider) |
| ~$8.3M gross is an *estimate* (3,332 ETH × spot); disputed by some outlets | A | BlockchainGamerBiz, crypto.news |
| 1,440 holding wallets, avg 2.3 deeds each (one snapshot); OpenSea showed 1,221 owners at another snapshot | B | BlockchainGamerBiz, TokenPost |

## Secondary market (OpenSea, point-in-time, do not treat as current)

| Fact | Conf | Source |
|---|---|---|
| OpenSea slug `yield-field-deeds`, chain Robinhood, **5% creator fee** | A | [OpenSea](https://opensea.io/collection/yield-field-deeds) |
| Trait categories: Background, Biome, Decor, Fertility, Landmark, Special, Special Count, Terrain, **Tier** | A | OpenSea trait filters (via search) |
| Snapshot 2026-10-28: floor ≈ $2,015, top offer ≈ $1,864, 24 h volume ≈ $33k, total volume ≈ $3.3M | B | OpenSea (via search) |
| Other snapshots: floor $2,957 / top offer $2,814; page titles showing 0.879 ETH floor and 1.219 ETH (offers page) | C (unknown dates) | OpenSea page titles |
| **Tier supply** (owner screenshot of OpenSea trait filter, 2026-10-30): Mythic 111, Legendary 222, Epic 555, Rare 888, Common 1,557 (sums to 3,333) | A | OpenSea trait panel |
| **Rare-tier floor 0.94 ETH** (listings 0.94–0.99 across Snow and Green biomes), owner screenshot 2026-10-30 | A | OpenSea, Tier=Rare filter |
| **Sales tape, ~22 h window ending 2026-10-30:** 39 sales, 38.8 ETH, mean 0.996, median 0.95 ETH; bimodal: a 0.79–0.99 band and a 1.15–1.23 band (10 of 39 prints ≥1.14), one outlier at 2.20 WETH | A | OpenSea activity (Sale, Mint filter) |
| **Collection header 2026-10-30:** floor 0.875 ETH, top offer 0.806 WETH, 24h volume 38.84 ETH, total volume 1,386.18 ETH, 222 listed (6.7%), 1,208 owners (36.2%); OpenSea footer showed ETH ≈ $2,223 | A | OpenSea header (owner screenshot) |
| **Biome == Tier, 1:1.** Mythic=Cosmic (purple/pink), Legendary=Sunset (orange), Epic=Swamp (purple/green), Rare=Snow, Common=Grassland | A | Tier-filtered item grids |
| **Tier floors / 7-day clearing bands (ETH):** Mythic 2.66 / 2.10–3.40 · Legendary 1.60 / 1.42–1.77 · Epic 1.18 / 1.03–1.17 · Rare 0.96 / 0.88–0.99 (one print 1.23) · Common 0.875 / 0.786–0.90 | A | Tier-filtered activity panels |
| The 1.15–1.23 band in the unfiltered tape is **Epic**, not Rare | A | Epic activity panel |
| What Tier / Fertility / any trait does in-game | **UNKNOWN** | — |

## Token

| Fact | Conf | Source |
|---|---|---|
| `$YIELD` not confirmed live; no contract address, supply, emissions, or sinks published in any indexed source | A (absence) | all searches |
| CryptoRank lists the project as "Potential" (pre-token) | B | [CryptoRank](https://cryptorank.io/price/yield-fields) |

## Chain

| Fact | Conf | Source |
|---|---|---|
| Robinhood Chain mainnet chain ID **4663**, testnet 46630; Arbitrum Orbit; gas in ETH | A | [TrustSwap](https://trustswap.com/robinhood/network-details), [OrbitFlare](https://orbitflare.com/products/robinhood-chain-rpcs), [ArchLiquid](https://www.archliquid.com/blog/robinhood-chain-network-configuration) |
| Public RPC `https://rpc.mainnet.chain.robinhood.com` | B | OrbitFlare |
| Explorer `robinhoodchain.blockscout.com` (Chainstack lists `robinscan.io` — conflict, unverified) | B | TrustSwap / Chainstack |

## Lookalikes and unaffiliated projects (do NOT interact)

| Item | Note |
|---|---|
| `yielfields-rh.com` ("Yield Fields — Web3 Farm Game") | Misspelled domain, uses `$YIELD` branding, says "wallet mode opens ~10 min after launch while we fund the treasury". Not confirmed official. Treat as phishing until proven otherwise. |
| `yieldfieldstrategy.xyz` / `$YFS` | Self-declared unaffiliated "strategy" token with 5% buy/sell tax that buys deeds. Not the project. |
| `rh.farm` / "Yield Farm" / `$CROP` | Different game (tiers Golden Acre / Prize Plot / Fertile / Common; weather 1.5×/0.5×). Not Yield Fields. |
| GitHub `identity-md-launches/launch-1626-yield-fields-deed` (`YFD` ERC-20) | Random token-generator repo; no link to project. |
| `yieldfields.medium.com` (BSC "YieldFields") | 2021 BSC DeFi farm, unrelated. |

## Owner position (resolved 2026-10-30)

Three **Rare (Frost, Fertility 6)** deeds minted at **0.1 ETH each via whitelist** (owner statement). Public Dutch auction cleared at 0.999688 ETH; WL price was a
separate tier (coverage noted WL pricing was "not yet clear"). Total basis
0.3 ETH. At the 0.96 ETH Rare floor net of 6% fees: ~2.71 ETH exit value, ~+800%.
All three are **Tier = Rare, Biome = Snow**. Token IDs still unrecorded (Q24).
