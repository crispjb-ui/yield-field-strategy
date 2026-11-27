# Launch runbook (written Wed 2026-11-25; updated Thu 26 Nov with the official "First Harvest" thread)

## UPDATE Fri 27 Nov: launch docs are out → see `12_LAUNCH_DOCS_2026-11-27.md` (it supersedes the notes below where they differ)
Key changes: Farmer open from minute one; Truffle Pig 0.01 ETH **on sale now**; Pig Levels (Fertilizer-fed, up to 3×);
Co-op spends only 3%/day (70% truffles / 30% tended deeds); sell tax 3% → 20%; launch buy tax 90% → 2% over 6 h;
any seed tends a deed; **not available to US persons per the docs**.

## Official announcement, @YieldFields_RH, 26 Nov (owner screenshots; grade A)
| Fact | Value |
|---|---|
| **Launch** | **Sat 28 Nov, 14:00 UTC** (9:00 Eastern, 8:00 Central, 6:00 Pacific) |
| Truffle Pool seed | 10M `$YIELD` = 10% of supply → **total supply 100M**. Paid daily for 30 days, front-weighted ("biggest rewards first"); after day 30, Co-op buys refill it |
| Truffle chance | **1 in 10 per crop** (was 1 in 20). Truffle Pig required before planting. Harvest within 48 h of ripening. Heavier Truffles from more valuable crops |
| Truffle payouts | **daily at 14:00 UTC** (not 00:00). First payout Sun 29 Nov 14:00 UTC |
| Farmers Co-op | **$500k in ETH, $250k of it on day 1.** Buys `$YIELD` every day, **starting 6 h after launch (Sat 20:00 UTC)**. Buys feed the Truffle Pool and Co-op Rewards. Exact split "in the docs tomorrow" |
| Docs | **Launch docs go live Fri 27 Nov, 14:00 UTC** (9:00 ET), "final numbers" |
| Co-op buying style | "Every day, in steady buys"; `$YIELD` trading taxes go "most of them to the Co-op" |
| First daily settlement | Sun 29 Nov, 14:00 UTC |
| **Co-op Rewards for deeds** | Stake the deed (no Fert Deck needed). **Each seed planted on your own plot tends 1 staked deed for 7 days.** Only tended deeds get that day's rewards; claim daily; rarer deeds get more |

What it changes:
1. **Your deeds only earn Co-op Rewards while tended.** 3 deeds need 3 plantings every 7 days. The launch planting
   covers 28 Nov → 5 Dec; plant 3 more seeds by Sat 5 Dec (whether a Bronze seed is enough: check Friday's docs).
2. **A known buyer arrives at T+6 h.** $250k is ~147 ETH, against ~682 ETH of presale crop value. The gap with no
   committed buying is roughly T+4 h to T+6 h. The ladder already sells half at T+3 h and lets the rest ride into
   the Co-op's buying; unchanged. How fast the Co-op spends is unpublished.
3. **First new-supply event is T+24 h** (Sun 14:00 UTC), when day-1 Truffle rewards (~645k `$YIELD` on a linear
   reading of the chart) are paid. The "45 min before settlement" rule now points at Sun 13:15 UTC.
4. **Truffles are a small bonus on day 1.** With ~682 ETH of crops harvested, 8 Diamond is 0.29% of the weight:
   ~1,800 tokens expected (43% chance of none). That is ~$4 at a $250k cap, ~$45 at $2.5M, ~$180 at $10M. Day-1
   Truffles only cover the sale fee above a ~$15M cap. They get interesting on **quiet later days**: 1 ETH of
   crops on a day when the network harvests 30 ETH would earn ~17,700 tokens, break-even at a ~$0.8M cap.
   The Pig is therefore an option on later-day farming: buy at ≤0.1 ETH.

## Saturday timeline in UTC
| Time | Event |
|---|---|
| 13:00 | Claim decks, Fert in Bag, Pig owned, wallet gas, game open |
| **14:00** | **Launch. Plant all, fertilize Commons first** |
| 14:30 | Diamond Commons ripe → harvest, sell to Farmer |
| 15:00 | Uncommons ripe |
| 15:36 / 16:00 | Rares / Epics ripe |
| 17:00 | T+3 h: ladder time rule; Legendaries ripe |
| 19:00 | Mythics ripe |
| 20:00 | Co-op begins buying |
| Sun 13:15 | Pre-settlement rule |
| Sun 14:00 | First Truffle payout; claim |
| Sat 5 Dec 14:00 | Deeds need re-tending by now |


Owner report: **full docs Friday 27 Nov, game live Saturday 28 Nov.** Launch hour not yet known.
State today: wallet `0x139e…3952` holds 3.0034 ETH on Robinhood Chain, no packs bought, ~120 Fertilizer,
3 Rare decks at 50% network speed. CornHub: 652.7 ETH of packs sold to 566 wallets, 74% Diamond; Farmer fee 6%,
Market fee 8%; Truffle Pig not on sale.

## Why the main buy moves to Friday
On Monday the case for buying early was readiness: the bridge was untested and launch could come at short notice.
Both are now resolved (ETH is bridged; docs land a full day before launch). Friday's docs should answer the
questions that set the size: is the Farmer open at launch, the buy/sell tax and launch-tax curve, `$YIELD` supply
and pool, Truffle Pig price, launch seed. Packs cost the same on Friday. So: test today, size and buy Friday.

## Owner decision (25 Nov): staggered buying
Owner chose to buy 5 Diamond today, a few on Thursday, and the rest before Saturday, instead of waiting for
Friday's docs. Accepted; the downside is bounded (Market exit ≈ −8.5%). Guard rails:
- Keep the **last 4 packs (1.0 ETH) unbought until Friday's docs are read**, so the size can still respond to the
  Farmer / tax news. Cap before docs: 9 Diamond (2.25 ETH).
- Wallet has 3.0034 ETH: 5 today leaves 1.75; 13 Diamond + Pig + gas needs a ~0.4–0.5 ETH top-up.
- Rip each batch the day it is bought and record the pulls (rarity counts) so the launch timing is known.
- `STATUS.md` shows the owner wallet's pack spend from chain.

## Seeds held (see `data/seeds.csv`)
**Holding 11 Diamond (2.75 ETH paid): 4 Ginger (Common), 6 Beet (Uncommon), 1 Eggplant (Epic) = 2.5 ETH crop value (−9.1% vs paid). Bag screenshot 27 Nov; 162 Fertilizer.**
With 2 Fert (22 total): 0.50 ETH ripe at 14:30 UTC, 1.50 ETH at 15:00, 0.50 ETH at 16:00. Farmer swap-in 2.35 ETH; Broker 2.30 ETH.
Exit break-even vs Farmer entry: 1.21× at a 3% sell tax, 1.46× at 20%. `poolwatch --cost-eth 2.75`.
27 Nov batch: 3 Beet. 26 Nov batch: 2 Ginger, 1 Beet.
25 Nov, 5 Diamond for 1.25 ETH → 2 Ginger (Common), 2 Beet (Uncommon), 1 Eggplant (Epic) = **1.25 ETH crop value**
(expected 1.244). With 2 Fert: 0.25 ETH ripe at 30 min, 0.50 ETH at 60 min, 0.50 ETH at 2 h. 10 Fert needed.

## Wednesday 25 Nov (today)
- [ ] Buy **1 Bronze pack** (0.005 ETH). Confirm the wallet shows contract `0x8C1e23Bc90F88DdC8CBA7256798aCbD745072524`. Rip it. Open "Verify the draw".
- [ ] Check the Bag for a Reward Pack. Look at the Truffle Pig screen.
- [ ] Claim Fertilizer.
- [ ] OCH: link a non-AGW wallet at play.onchainheroes.xyz if not done ("Crossing the chasm" was due late Nov).

## Thursday 26 Nov
- [ ] Claim Fertilizer. Keep ≥60 in the Bag from here on (26 needed for 13 Diamond, 50 for a full plot).
- [ ] If you want all 13 Diamond plus the Pig and gas: bridge ~0.4–0.5 ETH more (3.25 + Pig + ~0.05 gas).

## Friday 27 Nov — docs drop at 14:00 UTC / 9:00 ET (monitor is hourly; it opens an alert issue when any page changes)
- [ ] Tell Claude "docs are out" (or paste the alert). Claude re-reads all pages and the contracts, fills
      `config/mechanics.yaml`, re-runs `seed_pack_ev`, `farmer_vs_direct`, `roundtrip_breakeven`, the flow
      illustration with the real pool depth, and gives the final plot and ladder.
- [ ] Decision table:

  | Friday docs say | Launch plot |
  |---|---|
  | Farmer open at launch, buy tax well above 6.5% | 13 Diamond (or 11 with current ETH) |
  | Farmer opens later / not stated | 9 Diamond, hold the rest in ETH |
  | Fees raised, a pack cap, or a pool structure that breaks the thesis | re-plan before buying anything |

- [ ] Buy and rip the packs. Buy the Truffle Pig if on sale at ≤0.1 ETH (it must be owned before planting).
- [ ] Note the announced launch time in UTC; work out the hours to the first 00:00 UTC after it.

## Saturday 28 Nov — launch
**T−60 min**
- [ ] Claim all decks. Fertilizer in the Bag (import any you exported and need).
- [ ] Wallet connected, ≥0.03 ETH for gas, game open, seeds visible in the Bag.
- [ ] Start the watcher once the pool address is known (Claude can run it live in this session):
      `python -m yf.cli poolwatch --pool <POOL> --wallet 0x139e79b0d01148712528d56625a2a59f676e3952 --cost-eth <ETH spent on packs>`
      and set `launch_ts` in `data/poolwatch_state.json`.

**T+0**
- [ ] Plant every seed. 2 Fertilizer on each, immediately.

**T+30 min onward**
- [ ] Harvest as crops ripen (Diamond Common 30 min, Uncommon 60, Rare 96, Epic 120, Legendary 180, Mythic 300).
- [ ] Farmer open → sell each batch right away, in clips under the 3% slippage warning.
      Farmer closed → hold crops in the Bag; do not dump to the Market in a panic.
- [ ] Late crops (Legendary/Mythic): if the price has already run several-fold, sell those to the Market for ETH.

**Exit ladder** (multiple = (ETH realized + bag value now, net) ÷ ETH spent on packs)
| Trigger | Action |
|---|---|
| ≥ 2.0× | sell half |
| ≥ 3.5× | sell half of the rest |
| −30% from peak after ≥ 1.5× | sell down to a 15% keeper |
| T+3 h, nothing sold, ≥ 1.2× | sell half |
| Sun 13:15 UTC (45 min before the first Truffle payout), nothing sold, ≥ 1.2× | sell half |
| < 0.9× and never ≥ 1.5× | stop; no forced sale into a raised sell tax |

**After**
- [ ] Harvest everything within 48 h of ripening (Truffle rolls). Claim Truffle payouts after 14:00 UTC.
- [ ] Re-tend the deeds: plant ≥3 seeds every 7 days; claim Co-op Rewards daily.
- [ ] Deed rewards start at launch: check pending `$YIELD` on the three deeds; 10% claim fee.
- [ ] Revert the monitor cron to every 6 h after 5 Dec.

## Not doing
Buying deeds or Fertilizer; touching the USDC reserve; buying more than one plot of packs before launch.
