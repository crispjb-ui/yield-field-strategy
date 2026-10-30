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

## Where the docs cut against it (the challenge)
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
