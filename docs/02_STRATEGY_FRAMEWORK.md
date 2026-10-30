# Strategy Framework

Scope: 3 deeds held + $8,000 deployable. Horizon: unstated (Q25).
Everything below is conditional on `config/mechanics.yaml` being filled from
the docs. Where a rule depends on an unknown, the unknown is named.

## 1. Game summary (what is verifiable today)

- Two loops. **Free loop:** anyone plants seeds and harvests `$YIELD`.
  **Deed loop:** 3,333 deed holders run a separate loop that produces resources
  (first: Fertilizer via "Fert Decks") that free-loop farmers need.
- Deeds therefore sit on the *supply* side of an input the whole player base
  consumes. Their value is a function of (a) number of active free farmers,
  (b) how much Fertilizer each farmer wants per cycle, (c) Fertilizer price
  in `$YIELD`, (d) `$YIELD` price in ETH, minus (e) any upkeep.
  Items (a)–(e) are all unknown numerically (Q4–Q9, Q15–Q18).
- `$YIELD` is not confirmed live. Until it is, there is no seed market to
  deploy into and nothing to exit into except ETH via deed sales.
- Deed market depth (owner screenshot 2026-10-30): ~39 sales / ~39 ETH in
  22 h, median 0.95 ETH. An earlier $33k/24h snapshot (Oct 28) understated it.
  Three deeds are <8% of a day's volume; exits are not the constraint.
- 5% creator royalty on OpenSea plus marketplace fee: round-trip friction on a
  deed is ≥7.5% before spread.

## 2. The one question that decides the whole plan

**Is deed output demand-driven or emission-driven?**

| If the docs say… | Then deeds are… | Core play |
|---|---|---|
| Fertilizer only has value because free farmers buy it (open market, no floor price) | A bet on player count | Sell into hype peaks; do not add deeds; farm the free loop with `$YIELD` reinvestment only if seed ROI > 0 after sinks |
| Fertilizer / deed output pays a fixed `$YIELD` drip from the treasury or emissions | A yield instrument with a known coupon | Compute payback period in days at current `$YIELD`/ETH; buy deeds only if payback < your horizon with a ≥2× safety margin on token price |
| Deed output is required to plant higher-tier seeds (gate) | Scarce input with inelastic demand | Hold; rent or sell output at the gate price; strongest hold case |

Record the answer in `mechanics.yaml: fert.effect / fert.market_type`.

## 3. Decision rules for the $8,000

Default rule set, applied in order. Each step requires the prior step's gate.

**R0 — Deploy nothing until:** (i) docs read and Q1–Q19 answered, (ii) `$YIELD`
contract confirmed on official X **and** Blockscout, (iii) DEX pool depth and
LP lock status known (Q18). Rationale: all three are absent today and each is
a total-loss vector on its own.

**R1 — Reserve.** Keep 25% ($2,000) in ETH on Robinhood Chain untouched: gas
for the deed loop, and dry powder for a capitulation floor.

**R2 — Seeds before deeds.** With `$YIELD` live, run the ROI model
(`python -m yf.cli roi`). Deploy to seeds only if the modelled payback at the
*current* `$YIELD` price, after burn/sinks and with a 50% token-price haircut,
is under 14 days. Start with ≤$1,500; scale weekly only on realized (not
modelled) harvests. Emission games front-load returns; late entrants fund
early exits. Realized payback is the only signal.

**R3 — Deeds only on a coupon.** Buy additional deeds only under row 2 or 3 of
§2 and only if realized deed-loop income on your *existing* three deeds, over
≥7 days, annualizes to >100% on the floor price in ETH terms. Cap at 2 extra
deeds (~$4,000 at a ~$2,000 floor) so that total deed exposure stays
sellable within ~2 days of volume.

**R4 — Never chase the floor up.** No deed purchase above 1.0 ETH (the public
clearing price); above that you are paying more than the Dutch auction's
first-second buyers, with the mint hype already spent.

**R5 — Harvest-to-ETH schedule.** Convert a fixed share of every harvest to
ETH on the day of harvest. Default 50%, raised to 75% once initial capital is
recovered. Emission tokens in NFT games have historically trended to zero in
ETH terms; the compounding case has to be proven by realized data, not assumed.

## 4. Deed-loop operations (once mechanics known)

- If output requires an action per cycle (Q4), the automation's job is to
  never miss a cycle: compute the cycle schedule from the on-chain state,
  alert before expiry, and (phase 2) submit the claim transaction from a
  hot wallet holding only gas.
- If Fertilizer is sold on an open market (Q5), the edge is pricing: post
  asks at the top of the recent clearing band, undercut only when inventory
  ages past one cycle. Track the Fert price in `$YIELD` and in ETH; sell
  inventory faster when the ETH price of Fert is falling.
- Weather (Q11) if deterministic per week: schedule planting into high-
  multiplier weeks and hold inputs through low ones.
- Leaderboard (Q12): only worth optimizing if reward pool ÷ participants >
  marginal cost of the extra actions. Evaluate after one weekly cycle.

## 5. Exit plan (all assets)

### 5.1 Posture (basis 0.1 ETH/deed via whitelist; 3× Rare = Snow biome)
Basis 0.3 ETH. Rare floor 0.96 → net exit 3 × 0.96 × 0.925 ≈ 2.66 ETH (~+790%).
Fee-adjusted breakeven 0.108 ETH. 24h volume 38.84 ETH (header): three deeds
are ~7% of a day; exits are not a constraint.

**Anomaly resolved.** The 1.15–1.23 prints are Epic. Rares clear 0.95–0.99.
So list at **0.99–1.00**, the top of the Rare band, not 1.15; a Rare at 1.15
competes with Epic floor at 1.18 and will not fill.

**Market-implied tier ladder (floor ÷ Common floor):**

| Tier | Supply | Scarcity vs Common | Price ratio |
|---|---|---|---|
| Common | 1,557 | 1.0× | 1.00 |
| Rare | 888 | 1.75× | 1.10 |
| Epic | 555 | 2.8× | 1.35 |
| Legendary | 222 | 7.0× | 1.83 |
| Mythic | 111 | 14.0× | 3.04 |

Premiums are strongly sub-linear in scarcity. The market is pricing Tier as a
*mild* utility multiplier plus a collector premium at the top. The docs'
actual output multiplier per tier (Q2) is the trade: run
`tier_relative_value()` in `yf/roi.py` once `multiplier` is filled. A tier
whose stated-utility ratio exceeds its price ratio by ≥20% is the buy; one
below is the sell. This relative-value trade does not depend on `$YIELD`
being live, so it is the only thing the $8k can legitimately target today —
**after** the multipliers are read, not before.

**Upgrade check.** Selling all 3 Rares buys 1 Legendary (2.66 net ÷ 1.60)
with 1.06 ETH left over. Worth it only if one Legendary out-produces three
Rares, i.e. Legendary multiplier ≥ 3× Rare's. Compute with `swap_breakeven()`.
Default: no.

**Rules.**
- Sell 1 of 3 at the first liquidity event (token launch day, or Rare floor
  ≥1.2 ETH). List at 0.99–1.00; relist daily at the top of the band. Never
  list below the Rare floor.
- Hold the other two, no stop-loss; 0.2 ETH of basis at risk.
- Do not buy Rares at the floor. Blended basis would go 0.10 → 0.31 ETH.
- Deed proceeds become the ETH reserve (R1); seed tranche from cash.

### 5.2 Trigger-based exits for deeds
| Trigger | Action |
|---|---|
| Token launch day | Expect peak attention. List 1 deed at ≥1.3× floor the morning of; cancel if unfilled in 48 h. |
| Floor crosses 1.5 ETH | Sell down to 1 deed regardless of narrative. |
| 24h volume < $10k for 5 consecutive days | Liquidity is leaving; accept best offer on 1 deed while offers still exist. |
| Deed-loop income over 14 days < gas + upkeep | The loop is net negative; sell all but the single best-tier deed. |
| Any of: LP unlocked by team, treasury multisig changes, unverified contract upgrade | Sell all deeds and token at market. |

Sell via **accept best offer** rather than listing when the spread is <10%;
listings in thin markets get sniped on bad news.

### 5.3 Token exit
- `$YIELD` is sold per R5 on a schedule, not on signals.
- Hard rule: never hold more than 7 days of harvest unsold unless staking
  with a verified lock yields more than the observed 7-day price decay.
- Exit venue is the DEX pool; size each sell at ≤2% of pool depth to cap
  slippage, spread across the day.

### 5.4 Full exit
Done when: ETH realized ≥ (initial basis + $8,000 deployed) × 1.5, **or** any
row of the kill table in 5.2 fires. Remaining deeds after that are a free
option; hold them.

## 6. Risk register

| Risk | Likelihood (today) | Mitigation |
|---|---|---|
| `$YIELD` never launches or launches with a thin, unlocked pool | Unknown; token unconfirmed | R0 |
| Fert demand smaller than deed supply (3,333 producers, unknown consumers) | Flagged by coverage | §2 row 1 play |
| Phishing via lookalikes (`yielfields-rh.com`, `$YFS`) | High — already indexed | Only act on addresses from official X + explorer |
| Copycat games fragment attention | Reported 2026-10-28 | Faster exit schedule, R5 |
| Thin secondary liquidity | Confirmed (~$33k/24h) | Position cap in R3, offer-based exits |
| Unverified game contract source on explorer | One report | Do not deploy until source verified or audited |
| Multi-wallet / bot farmers compressing free-loop yield | Typical | Measure realized harvest daily; stop scaling on decay |

## 7. What I would challenge in the stated plan

1. "Buying seeds to farm `$YIELD`" is not available today: the token is not
   confirmed live. The $8k has no deployable target yet; time spent on
   tooling and docs review has higher expected value than any purchase.
2. Three "rare" deeds: "rare" is not a confirmed Tier value. If the Tier
   trait carries a multiplier, the exact tier of each token ID is the single
   most valuable fact to establish for both hold and sale pricing.
3. Deed-heavy allocation concentrates on the supply side of an input whose
   demand is unproven. The free loop plus a small deed book is the
   lower-variance structure until Fert demand is observed on-chain.
