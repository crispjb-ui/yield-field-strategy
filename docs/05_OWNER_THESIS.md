# Owner Thesis and Operating Rules (set 2026-10-30)

## Thesis (owner)
1. `$YIELD` could be the most valuable asset in the game. Plan: put most of the
   $8k ETH into farming to accumulate it.
2. Future utility will make higher rarities worth their premium.
3. With a 0.1 ETH basis on 3 Rares, do not buy more deeds.

## Where the docs support it
- `$YIELD` is fixed supply, 0% team, one taxed pool; every Farmer sale is a pool
  buy that skips buy tax. Early farmers choosing the Farmer create structural
  buy pressure at launch. Sell tax rises on heavy net selling, which slows
  dumps. Fert Deck output, deed rewards, Windfall and a classified stream all
  pay deed holders in `$YIELD`-adjacent flows, so upside concentrates in the
  token if volume arrives.
- Fertility "sets your share almost everywhere a deed earns" and "more parts
  of the game may use Fertility as it grows" — rarity utility is designed to
  widen. The redacted Windfall % by tier is the one place it could be convex.
- Not buying deeds at 0.96 when basis is 0.10 is correct on any thesis.

## Launch window (owner point, 2026-10-30; docs confirm)
The docs say: "right after trading opens, buys pay a much higher tax that falls
steadily back to normal", and a Farmer sale "buys $YIELD for you on the official
pool and skips the buy tax". So at onset the direct route is penalised by
design and farming is the only untaxed entry. `farm_vs_buy()` with the launch
tax plugged in returns `farm_if = True` for the whole decay window regardless
of pack EV, unless Farmer % is very low. Consequences:
- **The launch window is the highest-value period to be farming.** Every
  harvest sold to the Farmer is a tax-free pool buy while open-market buyers
  pay the launch tax. Early harvests also execute before Co-op rewards and
  speculative flow reprice the pool.
- **Throughput in that window is the edge.** Slots are fixed; Fertilizer is
  the only lever (2 units = 50% grow time = 2× cycles per slot). The 3 decks'
  stockpile is therefore worth more used than sold on day 1. Revised Fert
  rule: reserve 2 units × slots × expected cycles for the launch window
  first; sell only the surplus.
- **Readiness checklist before farming day 1:** ETH bridged, wallet tested on
  the Cornhub, Fert imported to Bag, pack choice precomputed from the
  published odds the moment they post, claim cadence maintained so the decks
  never stop.
- Direct buying is a later-stage tool, only after the launch tax has decayed
  and only if `farm_vs_buy()` says so.

## What the chain adds (2026-11-04)
1. **The network throttle is inevitable and arrives in days.** Circulation
   counts claimed Fert including Bags (API: `supply = claimed − used`). With
   84.7% of Fertility staked and nothing consuming Fert, the network crosses
   7 days of output ~11 Nov, 70% ~15 Nov, and sits at the 50% floor from
   ~21 Nov until farming opens. Your 9/day becomes 4.5/day on that schedule
   whatever you do. Not claiming does not help: a stopped deck is worse than
   a half-speed one, and held Fert is never taken. **Keep claiming.**
2. **Stockpile is therefore bounded**, roughly 9/day × 7 + taper ≈ 120 units
   by 21 Nov, then 4.5/day. At 2 per crop that is ~60 fully-fertilized crops
   for launch week plus ~2 per day after. Enough for your own plot; not a
   trading inventory. The Fert-sale leg of deed income is small by design.
3. **No back pay.** Deed `$YIELD` rewards start at token launch. Being staked
   early earns only Fert. Nothing is lost by this, but there is no "accrued
   rewards" argument for holding through a dip before launch.
4. **Claim fee is 10%, split 50/50** between all staked deeds (by Fertility)
   and the Silo. Every claim you make subsidises other stakers and the burn
   pot; claim deed rewards in large, infrequent batches once live.
5. **Root Cellar today is 0.0086 ETH per Rare.** Burn value is 1% of the
   floor. Burning is irrelevant until `$YIELD` taxes flow.
6. **70% of the collection was minted at 0.1 ETH.** The floor at ~0.9 is set
   by holders sitting on 9×. 85% staked and a live Fert loop keeps them
   sticky, but any shock meets a wall of sellers with nothing to lose. This
   is the main reason not to add deeds and the main reason the "sell 1 at a
   liquidity event" rule stays.
7. **The classified layer is visible in the bundle.** Cornhub has
   `farmerFeeBps`, `marketFeeBps`, `packFeeBps`, `packPrices` and a
   **Truffle Pig** purchase; a buyback contract spends a daily bps of the
   Co-op pool buying `$YIELD` and routes it to a truffle pool; a vester pays
   truffle claims over time. The pool itself is an in-house AMM with a
   virtual ETH reserve and a `maxSellFeeBps`, which is how the dynamic sell
   tax and "the team manages the pool" are implemented. Implication for the
   thesis: the volume incentive is a daily `$YIELD` prize pool funded by
   fees and paid to active farmers, which rewards throughput and consistency
   over capital size. Your plan (farm hard in the launch window, use own
   Fert, Farmer not Broker) is aligned with it. Budget for a Truffle Pig on
   day 1 if its fee is small relative to the tranche.

## Fert market read (2026-11-04) and the claim-automation decision
**Price.** 4.25 USDG ≈ 0.0019 ETH per unit, down from ~0.01–0.02 ETH on the
first prints. Supply in circulation grows ~8,400/day against ~1,200 exported
in total; pre-farming demand is speculators only. Expect the price to keep
falling toward the 50%-floor regime. Do not anchor the deed valuation on it.

**What a Rare earns at this price.** 3/day × $4.25 × 0.94 = $12/day gross
production value, but only 0.75/day (25%) exports without slowing the deck
and 1.5/day is the hard cap. Sustainable ETH income ≈ $3/day per Rare
(≈50% annualised on a $2,130 deed at a price that is collapsing). The
Fert-sale leg is a rounding error against the thesis; it exists to price
your own Fert's opportunity cost, which is now ~$4 per unit.

**Optional trade, not recommended for the effort:** export the free 25%
band (2.25/day across 3 decks ≈ $9/day) while the price is >$4 and rebuy
cheaper before farming. Exporting does not add to circulation (claimed
units already count), so it has no network cost. Upside ≈ $150–200 over
three weeks. Default remains: keep everything for launch-window throughput.

**Claim automation: manual, with a reminder.** Reasons:
- Claims are off-chain, authenticated by a wallet-signed login (SIWE) and
  a session cookie, then `POST /api/play/deeds/claim`. No key is needed
  after login, but a browser bot that signs the login needs a key or a
  wallet extension; that is the only dangerous part and it is avoidable.
- Stakes are small: a missed claim window costs at most 3 units per deck
  per day ≈ $38/day today, falling with price and the network throttle.
  Twelve clicks a month cover it.
- Partial progress carries over, so claiming early loses nothing. Any
  time inside 72 h is equally good.
- If travel makes manual claiming unreliable: log in once in a normal
  browser, copy the session cookie, and run a 30-line script that calls
  the claim endpoint every 60 h until the cookie expires. The cookie can
  act in-game (claim, plant, use Fert) but cannot move on-chain assets,
  which always need a wallet signature. Build only on request.
1. **After the launch tax decays, farming is not necessarily the cheapest way to own `$YIELD`.**
   Farming route: pack ETH → random seed (Common < pack value) → Farmer pays
   ███% in `$YIELD` minus Co-op Dues. Direct route: buy on the pool and pay the
   buy tax. Farming wins only if `E[worth] × Farmer% × (1 − dues) > 1 − buy tax`.
   `farm_vs_buy()` decides this the day the numbers publish. If direct is
   cheaper, farming is a worse way to express the token thesis, with pack
   variance on top. Farming's extra claim is the classified layer (truffles,
   the volume incentive) which only farmers can access.
2. **The docs name volume as the unsolved problem** ("most onchain games never
   figured out how to incentivize it") and the answer is classified. The token
   thesis is a bet that the classified mechanism works. Unverifiable today.
3. **LP is team-managed and removable; contracts upgrade without timelock.** If
   the token is the thesis, these are the thesis's largest holes. Size to them.
4. **Rarity premium is already in the price.** Mythic trades at 3.04× Common
   for 1.8× stated utility. The market already pays for convex future utility.
   Owner's view and the market agree, so there is no edge in it, which is
   consistent with not buying.
5. **Throughput cap.** One free plot with fixed slots per wallet. $8k may not
   deploy in one cycle; it deploys as slots free up, so capital sits idle
   unless spread across wallets (every wallet gets a free plot per the docs;
   terms of service on multi-wallet are not published).

## Operating rules under the owner's thesis
| Rule | Setting |
|---|---|
| Allocation | 75% ($6,000) farming/`$YIELD`; 25% ($2,000) ETH reserve for gas, decks, and a capitulation buy of `$YIELD` if it dumps post-launch tax |
| Timing | Nothing until farming and `$YIELD` are live and odds, pack prices, Farmer %, dues and buy tax are published. Then run `seed_pack_ev()` and `farm_vs_buy()` the same day |
| Route | Launch window: farm, Farmer only (never Broker), largest pack only, 2 Fert per crop from own decks, run slots continuously. After the launch tax decays: re-run `farm_vs_buy()`; buy direct only if it wins by >10%, in ≤2%-of-pool clips |
| Tranches | First tranche ≤ $1,500 regardless of route; next tranche only after one full realized cycle matches the model within 20% |
| Hold rule | Hold `$YIELD` per thesis. Hard rule: once `$YIELD` holdings ≥ 2× ETH deployed, sell enough to recover deployed principal; the remainder rides with no target |
| Fert | Own-use first: reserve 2 × slots × planned launch-window cycles; sell only surplus into the day-1 spike |
| Deeds | Hold 3, stake all, no additions. Sell 1 only on a Rare floor ≥1.5 ETH or a kill trigger; thesis favours keeping all 3 for deed rewards in `$YIELD` |
| Kill (exit all `$YIELD` and unstake) | LP removed/rebalanced against holders; staking or token contract upgraded without notice; multisig change; exploit; `$YIELD` 7-day realized volume below what funds any rewards (judgement, logged) |

## What would change my recommendation to "wait"
Published numbers showing `farm_vs_buy` advantage > +20%, or a classified
reveal that pays farmers something deed holders and pool buyers cannot get.
