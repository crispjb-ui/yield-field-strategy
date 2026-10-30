# Strategy Framework

Rewritten 2026-10-30 after reading the official docs (`docs/source/`). Position:
3 Rare deeds (Frost, Fertility 6), basis 0.1 ETH each. Deployable: $8,000
(~3.6 ETH at the ~$2,223 ETH/USD OpenSea showed). Horizon: unstated.

## 1. The game, as the docs define it

Two loops, three stages, no dates.

- **Stage One (first):** deed holders stake, pay 0.01 ETH for a Fert Deck, and
  produce Fertilizer 24/7, scaled by Fertility (5–9). Storage holds 3 days;
  a full deck stops. Fertilizer exports as an ERC-1155 and trades on OpenSea.
- **Stage Two:** farming opens to everyone. Buy a seed pack in ETH, plant in a
  free fixed-slot plot, harvest, sell to the Farmer (`$YIELD`) or the Broker
  (ETH paid out of the pack-sale pool). Fertilizer cuts grow time 25% per
  unit, max 2 per crop.
- **Stage Three:** deed rewards in `$YIELD` split by Fertility, a claim fee
  that feeds the Silo, and burns that cash out a deed's Root Cellar (ETH) plus
  a Windfall (share of the Silo).

Structural reads that follow directly from the docs:

1. **Fertilizer is the deed's only Stage One income, and it is ETH-denominated
   on OpenSea.** Deed income path #1 does not depend on `$YIELD` existing.
2. **Fertilizer supply only grows.** 3,333 decks × 24/7 × never expires. Demand
   is bounded by farmers × plot slots × crops per day. Until farming opens
   there are no natural buyers, only speculators. Fert is a depreciating
   asset in expectation unless farmer count outruns 3,333 producers.
3. **Fertility is linear.** Rare makes 1.2× Common, Mythic 1.8×. The market
   prices Mythic at 3.04× Common. That gap is collector premium, not utility.
4. **The Broker is a closed loop.** Broker ETH comes from pack sales. Farming's
   ETH-only expected value is therefore ≤ (Broker % × E[worth multiple]) − 1
   per pack, and the docs say a Common seed is worth less than its pack.
   Until the redacted odds and multiples are published, farming EV in ETH is
   unknowable and plausibly negative; the upside case runs through `$YIELD`.
5. **Governance risk is explicit.** Multisig, no timelock, upgradeable staking
   contract that applies to staked deeds, team-managed LP it "can remove",
   audit planned not done. The docs are honest about this. Size accordingly.
6. **Burning is the exit of last resort, not the goal.** Root Cellar is funded
   by 0.01 ETH build fees (if all 3,333 build: 33 ETH total; a Rare's share by
   Fertility is 6/19,773 ≈ 0.01 ETH) until `$YIELD` taxes flow. The Windfall %
   by tier is redacted. A burn beats a sale only when
   `root_cellar + silo × windfall% × yield_eth > 0.94 × tier floor`
   (`burn_vs_sell()` in the model). Today that is 0.01 ETH vs ~0.90 ETH.

## 2. Tier relative value (docs Fertility ÷ market floor, 2026-10-30)

| Tier | Fertility | Floor ETH | Price ÷ Common | Utility ÷ Common | Score | Fertility per ETH |
|---|---|---|---|---|---|---|
| Common | 5 | 0.875 | 1.00 | 1.0 | 1.00 | 5.71 |
| **Rare** | 6 | 0.96 | 1.10 | 1.2 | **1.09** | **6.25** |
| Epic | 7 | 1.18 | 1.35 | 1.4 | 1.04 | 5.93 |
| Legendary | 8 | 1.60 | 1.83 | 1.6 | 0.88 | 5.00 |
| Mythic | 9 | 2.66 | 3.04 | 1.8 | 0.59 | 3.38 |

Rare is the most efficient tier to own for every Fertility-scaled reward the
docs list (Fert output, Root Cellar, claim rebate, deed rewards). You hold the
right tier. Caveat: if the redacted Windfall % is convex in tier (e.g. Mythic
takes 10× Common's share rather than 1.8×), the burn path could favour top
tiers. That is the only mechanism that could justify the Mythic premium; it is
unpublished. Do not pay for it in advance.

**Upgrade check:** 3 Rares sold net 2.71 ETH, buys 1 Legendary (1.60) + 1.11
ETH change, or 2 Epics (2.36) + 0.35 change. 3 Rares = Fertility 18; 1
Legendary = 8; 2 Epics = 14. Never swap up. Swapping *down* (3 Rares → 3
Commons + 0.08 ETH) loses Fertility 3 for 0.08 ETH; not worth the fees.

## 3. The plan

### 3.1 Do now (Stage One, cost ≈ 0.03 ETH + gas)
1. Bridge a small amount of ETH via the official Robinhood Chain bridge only.
2. Verify the staking contract address on the official-links page, character
   by character, then stake all 3 deeds and build 3 Fert Decks in one tx.
   Cost 0.03 ETH. Unstaking destroys the deck, so this is a one-way door
   until you intend to sell.
3. Claim every ≤60 h. A full deck is dead time. Record the first two claims to
   derive the output rate for Fertility 6 (open question 1), which converts
   every later decision into arithmetic.

### 3.2 Fertilizer policy
- **Before farming opens:** do not sell into speculative bids unless a bid
  exceeds the price you would accept for a unit on farming day 1 (set this
  once the output rate is known; placeholder: hold). Stockpile. The docs
  themselves say supply should be ready for day 1.
- **Farming day 1 to day 3:** this is the demand spike (every farmer starts at
  once with fresh packs). Sell most of the stockpile here. Keep 2 units per
  crop you plan to grow yourself for the first week.
- **Steady state:** sell weekly at the 24 h VWAP or better; do not hoard.
  Supply inflates forever; holding Fert is a bet that farmer count grows
  faster than 3,333 decks produce.
- Own-use beats buying: your 3 decks fund your own farming's Fert at zero
  marginal cost. Buy Fert never.

### 3.3 The $8,000 — superseded by `05_OWNER_THESIS.md` (owner elected the token thesis); the gating rules below still apply
- **R0 stands for seeds and `$YIELD`:** nothing is purchasable yet. Farming
  prices, odds and payout % are redacted. When published, run
  `seed_pack_ev()`; deploy only if the Broker-path EV ratio is ≥ 0.90 (ETH-only
  loop loses ≤10%) so the `$YIELD` path is upside, not rescue. Buy the largest
  pack affordable (docs: bigger packs are strictly better per ETH), never
  split into small packs. Throughput is capped by plot slots × grow time, so
  capital deploys in tranches, not at once; the first tranche is ≤ $1,500.
- **Deeds:** the only purchase with a quantifiable edge today is a Rare at
  ≤0.96 ETH (best Fertility per ETH). Two cases:
  - *Wait* (default): staking launch publishes the output rate within days of
    going live. With rate × any Fert price you can compute payback. Cost of
    waiting is a possible floor run-up on the staking announcement.
  - *Act now:* if you want more exposure before the number exists, cap it at
    2 Rares (≈1.92 ETH, ≈$4,270), at or below 0.96, and accept that you are
    buying on the docs' structure rather than a measured coupon. This raises
    blended basis from 0.10 to 0.44 ETH on five deeds.
  My recommendation is *wait*: the information arrives in days and is free.
- **Reserve:** 25% ($2,000) in ETH on Robinhood Chain, always.
- **Harvest-to-ETH:** sell 50% of every `$YIELD` receipt on receipt, through
  the Broker where possible (Farmer-then-sell nets less per the docs), sized
  ≤2% of pool depth per clip. Raise to 75% after capital is recovered.

### 3.4 Exit
- **Deeds.** Sell 1 of 3 at the first liquidity event: staking launch day or
  farming launch day, whichever produces a Rare floor ≥1.2 ETH first; else
  at farming launch regardless. List at the top of the Rare band (0.99–1.00
  today). Selling requires unstaking first (deck destroyed; 0.01 ETH to
  rebuild if you reverse). Hold the other two with no stop; 0.2 ETH basis at
  risk. Sell down to one at a Rare floor ≥1.5 ETH.
- **Fertilizer.** Per 3.2. Never carry more than ~2 weeks of production.
- **`$YIELD`.** Per 3.3 schedule. Never hold more than 7 days of receipts.
- **Burn.** Only when `burn_vs_sell()` is positive. Expect that to be never
  unless `$YIELD` taxes make Root Cellars large; re-check at each poll.
- **Kill table (sell everything at market):** LP removed or rebalanced
  against holders; staking contract upgraded without notice; multisig change;
  any exploit; Fert 24 h VWAP below gas cost of claiming for 14 days.

## 4. Risk register (docs-grounded)

| Risk | Evidence | Response |
|---|---|---|
| Upgradeable staking contract, no timelock, applies to staked deeds | fees-and-risks | Stake the free position only; add exposure after audit |
| Team-managed LP, removable | fees-and-risks | `$YIELD` sold on schedule; never a hold thesis |
| Fert oversupply (3,333 decks, no expiry) vs unknown farmer count | fertilizer, staking pages | Sell into day-1 spike; no hoarding |
| Farming ETH-EV negative by design (Broker paid from pack pool; Common < pack) | growing-and-selling, seeds | Gate on published odds; `seed_pack_ev()` ≥ 0.90 |
| Dynamic sell tax traps exits during drawdowns | yield page | Sell small and early; Broker path for ETH |
| Mythic/Legendary premium unsupported by linear Fertility | founding-deeds + market | Never swap up; hold Rare |
| Classified mechanics could reweight everything (truffles, volume incentive, extra deed stream) | classified, flywheels | Re-run the model at each reveal; no pre-positioning |
| Lookalike sites/tokens | official-links | Only the three official channels |

## 5. What I challenge in the original ask

1. "Seeds to farm `$YIELD`" is a Stage Two action with redacted economics and
   a Broker loop that is closed by construction. It is not where the edge is.
   The edge in Stage One is being an early, consistently-claiming Fert
   producer in the most efficient tier, and selling into the day-1 demand
   spike before supply overwhelms it.
2. The three Rares are already the optimal tier per the docs. The "upgrade"
   instinct toward Legendary/Mythic is the trade to avoid.
3. The $8k's highest-value use today is patience: the two numbers that decide
   everything (Fert output rate, pack EV) arrive free with each stage launch.
