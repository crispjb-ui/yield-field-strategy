# Launch runbook (written Wed 2026-11-25)

Owner report: **full docs Friday 27 Nov, game live Saturday 28 Nov.** Launch hour not yet known.
State today: wallet `0x139e…3952` holds 3.0034 ETH on Robinhood Chain, no packs bought, ~120 Fertilizer,
3 Rare decks at 50% network speed. CornHub: 652.7 ETH of packs sold to 566 wallets, 74% Diamond; Farmer fee 6%,
Market fee 8%; Truffle Pig not on sale.

## Why the main buy moves to Friday
On Monday the case for buying early was readiness: the bridge was untested and launch could come at short notice.
Both are now resolved (ETH is bridged; docs land a full day before launch). Friday's docs should answer the
questions that set the size: is the Farmer open at launch, the buy/sell tax and launch-tax curve, `$YIELD` supply
and pool, Truffle Pig price, launch seed. Packs cost the same on Friday. So: test today, size and buy Friday.

## Wednesday 25 Nov (today)
- [ ] Buy **1 Bronze pack** (0.005 ETH). Confirm the wallet shows contract `0x8C1e23Bc90F88DdC8CBA7256798aCbD745072524`. Rip it. Open "Verify the draw".
- [ ] Check the Bag for a Reward Pack. Look at the Truffle Pig screen.
- [ ] Claim Fertilizer.
- [ ] OCH: link a non-AGW wallet at play.onchainheroes.xyz if not done ("Crossing the chasm" was due late Nov).

## Thursday 26 Nov
- [ ] Claim Fertilizer. Keep ≥60 in the Bag from here on (26 needed for 13 Diamond, 50 for a full plot).
- [ ] If you want all 13 Diamond plus the Pig and gas: bridge ~0.4–0.5 ETH more (3.25 + Pig + ~0.05 gas).

## Friday 27 Nov — docs drop (monitor is hourly; it opens an alert issue when any page changes)
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
| 45 min before the first 00:00 UTC, nothing sold, ≥ 1.2× | sell half |
| < 0.9× and never ≥ 1.5× | stop; no forced sale into a raised sell tax |

**After**
- [ ] Harvest everything within 48 h of ripening (Truffle rolls). Claim Truffle payouts after 00:00 UTC.
- [ ] Deed rewards start at launch: check pending `$YIELD` on the three deeds; 10% claim fee.
- [ ] Revert the monitor cron to every 6 h after 5 Dec.

## Not doing
Buying deeds or Fertilizer; touching the USDC reserve; buying more than one plot of packs before launch.
