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
