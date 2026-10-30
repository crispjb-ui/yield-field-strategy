# Open Questions — answer from yieldfields.fun/docs before deploying capital

Each answer goes into `config/mechanics.yaml` (parameter name in brackets) and
into `docs/01_VERIFIED_FACTS.md` with the docs URL.

## A. Deeds (your 3 + any purchase)
1. What are the Tier values and their supply counts? Which Tier are token IDs ___, ___, ___? `[deed.tiers]`
2. What does Tier change numerically: resource output rate, plot count, Fert Deck size, multiplier? `[deed.tier_multiplier]`
3. What do Fertility, Landmark, Special, Special Count, Biome, Terrain do? Which are cosmetic? `[deed.trait_effects]`
4. Is deed output (Fertilizer / Fert Decks) a passive drip, or does it require actions (gas, time, inputs)? `[deed.output_per_cycle, deed.cycle_hours, deed.action_required]`
5. Can deed output be sold on an in-game market or only consumed? Is there a built-in price or an open order book? `[fert.sellable, fert.market_type]`
6. Do deeds have any upkeep, decay, tax, or re-activation cost? `[deed.upkeep]`
7. Is deed output claimable in `$YIELD` directly, or only in resources? `[deed.pays_yield]`

## B. Seeds / farming (free loop)
8. Seed types, cost (in what asset), grow time, harvest size in `$YIELD`. `[seeds[]]`
9. Does Fertilizer multiply harvest, shorten time, or gate higher-tier seeds? By how much? `[fert.effect, fert.magnitude]`
10. Per-wallet caps on plots, plantings, or daily harvests? Does that make multi-wallet relevant? `[farm.plot_cap, farm.daily_cap]`
11. Weather: what are the states, their probabilities, their multipliers, and how is the week's weather set? `[weather]`
12. Leaderboard: scoring formula, reward pool size and source, payout cadence. `[leaderboard]`
13. Energy / cooldown / stamina mechanic? `[farm.energy]`

## C. `$YIELD` token
14. Contract address (confirm on official X + Blockscout). Total/max supply. `[token.address, token.max_supply]`
15. Emission schedule: per-block, per-harvest, halving, or treasury-funded? Does emission depend on number of players (fixed pool split) or is it per-player (inflationary)? `[token.emission_model]`
16. Sinks: what burns or locks `$YIELD` (seeds, upgrades, Fert, fees)? What fraction of seed spend is burned vs recycled to the treasury? `[token.sinks]`
17. Treasury: size, source (mint proceeds?), what it funds, who controls it. `[treasury]`
18. Liquidity: which DEX, initial pool depth, LP locked or not, team/insider allocation and vesting. `[token.liquidity]`
19. Any transfer tax or anti-whale rule? `[token.tax]`

## D. Market / exit
20. Which marketplaces list the deeds (OpenSea only?), and is there a royalty-free venue? (5% creator fee confirmed on OpenSea.)
21. Is there an in-game deed rental or delegation? (Changes whether holding vs selling is binary.)
22. Does the team have a published roadmap with dated milestones (token launch date, season end)?

## E. Owner inputs
23. Exact cost basis per deed in ETH and the ETH/USD at purchase (see discrepancy in `01_VERIFIED_FACTS.md`).
24. The three token IDs.
25. Target hold horizon and the drawdown you will tolerate on the $8k (defines the stop rules in §5 of the strategy).
