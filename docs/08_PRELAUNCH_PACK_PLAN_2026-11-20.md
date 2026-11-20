# Pre-launch pack plan (2026-11-20)

Owner report: the Cornhub (pack shop) opens 2026-11-21; farming starts "sometime next week". Not yet in the
official docs or on the contracts page at the time of writing (grade C until the address is published; the
monitor alerts and reads the contract automatically when it is). ETH = $1,752 → farming bucket $6,000 = 3.43 ETH,
reserve $2,000 = 1.14 ETH.

## What pre-buying does and does not buy
- Pack price is fixed and odds are identical every day. A pack bought on day 1 of the shop is the same pack as one
  bought an hour before launch. **Buying early has no edge by itself.**
- The only thing pre-buying buys is **being planted at T+0**: seeds already ripped and in the Bag, no shop
  transaction or drand wait while the launch-day servers are loaded.
- A plot has 25 slots. Pack 26 cannot be planted until a slot frees (≥30 min with 2 Fert). **Pre-buying more
  than 25 packs has zero speed benefit.** "As many packs as possible" is the wrong objective; the right one is
  "the ETH I want working at T+0, in ≤25 packs".
- Cost of buying early: ETH sits in the Cornhub contract for a week (owner has a `withdraw(to, amount)`
  function; audits were still pending on 9 Nov), seeds live off-chain in the game Bag, and the selling fees,
  Truffle Pig price, launch-seed size, Farmer opening time and launch-tax curve are all still unannounced.
  Each of those can change how much should go in.
- Conclusion: **buy the T+0 plot ~24 h before the announced launch time, not tomorrow.** Tomorrow is for reading
  the contract and testing the flow.

## Mix comparison (`pack_mix()` in `yf/roi.py`, 2 Fert per crop, 10% fee assumed)
| Mix | ETH | USD | ±1σ on value | P(no Truffle) | Fert | Hours to clear | Market-exit loss if thesis fails |
|---|---|---|---|---|---|---|---|
| 13 Diamond | 3.25 | 5,693 | 17.8% | 51% | 26 | ~1 (tail 5.0) | 0.34 ETH |
| 8 Diamond + 14 Platinum | 3.40 | 5,956 | 15.1% | 32% | 44 | ~1 (tail 5.2) | 0.36 ETH |
| 34 Platinum | 3.40 | 5,956 | 11.0% | 17.5% | 68 | ~1.4 | 0.36 ETH |
| 68 Gold | 3.40 | 5,956 | 7.8% | 3.1% | 136 | ~2.9 | 0.36 ETH |
| **20 Platinum + 5 Gold** | **2.25** | **3,942** | 13.1% | 27.7% | 50 | ~1.0 | **0.24 ETH** |
| 25 Gold | 1.25 | 2,190 | 12.8% | 27.7% | 50 | ~1.1 | 0.13 ETH |

Expected value per ETH is identical in every row (0.995 before fees). Tier only changes variance, Truffle-roll
count, Fert use and time. Diamond is fastest per ETH but at this budget half the time you find no Truffle on
day 1 and one Common-heavy draw costs 18%. Gold needs three plot cycles and most of the Fert stockpile.
Platinum is the balance point.

## Plan
**Tomorrow (shop opens) — spend ≤0.01 ETH**
1. Wait for the Cornhub address on the official links page (monitor raises `CORNHUB LIVE` with fees, pack
   prices, Pig price, float). Verify the address character by character before signing.
2. Buy 1 Bronze pack (0.005 ETH), rip it, open "Verify the draw". Confirms wallet, shop, rip and Bag work.
3. Note the Truffle Pig price. Buy it if ≤0.1 ETH (≈3% of the farming bucket): without it there are no
   Truffles, and it must be owned before planting. Above that, wait for the launch-seed size.
4. Send me a screenshot of the shop and Pig screens and any announcement text. If there is an early-buyer
   incentive, a per-wallet cap, a price schedule or reward packs, the plan changes and I re-run it.

**T−24 h (launch time announced, fees published)**
5. Re-run `python -m yf.cli probe <cornhub>`; check `rake_from_cornhub`. Go if Market rake ≤ ~12% and the
   Farmer is confirmed for launch or shortly after.
6. Buy and rip the T+0 plot: **20 Platinum + 5 Gold = 2.25 ETH (66% of the bucket)**. Keep 1.18 ETH of the
   bucket and the whole 1.14 ETH reserve liquid. Have ≥50 Fertilizer in the Bag (stop exporting at T−3 days if
   the Bag is below 60).

**T+0**
7. Plant all 25, 2 Fert each, immediately. Commons ripen in ~31–32 min.
8. Harvest as they ripen. Farmer open → sell in clips under the 3% slippage warning. Farmer closed → hold crops
   in the Bag (they never wilt for selling); Truffle rolls already happened at harvest.
9. **Wave 2 (the remaining 1.18 ETH) is decided on live data, 1–3 h in:** `truffle_cycle_ev()` with "Pays out
   today" and "Weight today" from the Truffles tab, `farmer_vs_direct()` with the live buy tax, and the pool's
   ETH reserve. Deploy if both say yes; otherwise hold it for day 2+, when Truffle weight per ETH is usually
   better because day 1 is the most crowded night.

**Do not**
- Buy more than 25 packs ahead; buy days ahead; touch the reserve; sell to the Market just to rebuy packs unless
  the Truffle EV check is positive.

## Why 66% and not 100% at T+0
The owner's thesis (earliest Farmer sales buy the cheapest `$YIELD`) argues for everything at T+0. Against it:
the Farmer runs on its own switch with no stated opening time, the fee is unpublished, the pool at a ~$250k
start is thin enough that 3.4 ETH of Farmer sales in one hour moves it materially, and day-1 Truffle weight
will be the highest of the month. A worst-case Market exit on 2.25 ETH costs ~0.24 ETH (~$410). That is an
acceptable price for being in at T+0; 0.36 ETH on the whole bucket buys nothing extra, because the last third
can follow within the hour once the tabs show real numbers.

## Addendum: stacking high-rarity seeds for the T+0 plot (asked 2026-11-20)
Simulated in `scripts/sim_plant_order.py` (4,000 draws, 25 slots, 2 Fert each, whole bucket pre-ripped).

| 34 Platinum, plant order | Value-weighted mean hours to harvest | % of value harvested by 1 h | by 2 h | All done |
|---|---|---|---|---|
| Highest rarity first | 1.52 | 10% | 79% | 3.0 h |
| Random | 1.57 | 17% | 72% | 3.3 h |
| Shortest first | 1.68 | 23% | 57% | 3.6 h |

- Grow time is proportional to worth, so every rarity in a tier earns the same value per slot-hour. A plot of
  Mythics is not a better plot; it is the same value arriving later in one lump.
- Cherry-picking does not remove the low seeds. They cannot be sold or exported; they still have to be planted.
  Total value is set by packs bought, not by which 25 go first.
- Rare-or-better is 24% of pulls: 25 such seeds needs ~105 packs (10.5 ETH in Platinum). The bucket buys 34.
- Order moves the average by ~3–10 minutes. Highest-first finishes sooner overall; shortest-first gets more value
  to the Farmer in the first hour. Neither is material.
- Real uses of order: longest crops before going offline (fewer check-ins, inside the 48 h Truffle window), short
  crops while active; and Fert goes furthest on long crops if Fert is ever scarce.
- Only reason to hold more than 25 pre-ripped: commit the whole bucket to day 1 regardless of live data and avoid
  needing the shop under launch load. Then: 34 Platinum, plant highest first. Cost: the wave-2 option on 1.18 ETH.

## Addendum: funds are in USDC (owner, 2026-11-20)
- Sizing stands: at ETH $1,752 the $6,000 bucket is 3.43 ETH; T+0 plot 20 Platinum + 5 Gold = 2.25 ETH ≈ $3,940.
  Re-price in USD on the day: packs are priced in ETH, so the USD cost moves with ETH.
- **Convert just in time, in three steps, and leave everything else in USDC:**
  1. Tomorrow: ~0.12 ETH on Robinhood Chain (test pack 0.005 + Truffle Pig cap 0.1 + gas). This doubles as the
     test of the conversion and bridge path.
  2. T−24 h: 2.25 ETH for the T+0 plot (+0.01 gas).
  3. Wave 2: convert up to 1.18 ETH only when the live checks say go.
- The $2,000 reserve stays in USDC, not ETH (supersedes "reserve as ETH on Robinhood Chain"): no ETH price
  exposure on money that is not meant to be deployed before 2026-12-15.
- Official Robinhood Chain bridge only. Bridge time is unverified here; step 1 measures it. Do not leave step 2
  to launch morning.
