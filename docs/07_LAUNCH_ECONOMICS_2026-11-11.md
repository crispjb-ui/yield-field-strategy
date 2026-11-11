# Launch economics, from the un-redacted mirror (2026-11-11)

Source: `yf-unredacted.vercel.app` (third party; snapshot in `docs/source/yf-unredacted-mirror-2026-11-11.txt`).
Grading: game *structure* is **A** where I confirmed the strings in the live bundle (Truffle Pig, 1-in-20,
Motherlode payout text, Spoiling/Spoiled, "Opening soon", grow-factor table `[120,116,108,104,100]`);
*numbers* (pack prices, odds, worth multiples, 10% fees, 90% launch tax, $250k mcap) are **B**: testnet
defaults that the mainnet Cornhub and pool contracts will set at launch. Recompute everything from
`packPrices()`, `vegetablePrices()`, `farmerFeeBps()`, `marketFeeBps()`, `buyFeeBps()` on launch day.

## The numbers (defaults)
| Item | Value |
|---|---|
| Packs (ETH) | Bronze 0.005 · Silver 0.01 · Gold 0.05 · Platinum 0.1 · Diamond 0.25 |
| Seed odds (all tiers) | Common 45% · Uncommon 31% · Rare 15% · Epic 6% · Legendary 2.5% · Mythic 0.5% |
| Crop worth (× pack) | 0.5 · 1 · 1.6 · 2 · 3 · 5 → **E[worth] = 0.995** |
| Sale fee (Co-op Dues) | 10% Market (ETH, from pack float) · 10% Farmer ($YIELD, tax-free pool buy). Docs say Farmer's will be lower on mainnet |
| Grow time | worth×10 × tier factor ÷ 500 h. Diamond: 1 / 2 / 3.2 / 4 / 6 / 10 h; odds-weighted avg ≈ 2 h |
| Plot | 25 slots per wallet, free, no deed |
| Truffles | Truffle Pig required (one per wallet, ETH, price unknown); 1-in-20 per harvest of crops planted after the Pig; weight = crop ETH value; harvest within 48 h of ripe |
| Nightly payout | seed release (30-day launch seed) + 5% of refill above it; 5% to Motherlode; split by weight; ≤5% of pool per truffle |
| Fees → | Buyback vault → buys $YIELD → Truffle Pool. Pack ETH stays in the Cornhub as the Market's float |
| $YIELD launch (team "leaning") | ~$250k starting mcap; ~90% buy tax decaying over ~24 h; taxes live in an in-house pool, not the token |
| Deed rewards | release lock, half every 8 h; 10% claim fee (5% back to stakers, 5% Silo); no back pay |
| Windfall | min(F×10%, 100%): Rare **60%**, Mythic 90%; sequential race, first burn takes its share of the whole Silo |
| Exports (owner, F=18) | 3/day free (ceil 18/8), hard limit 4/day; rolling 24 h |

## What this does to the thesis

**1. The ETH loop is a 10.45% rake, by construction.** Pack → crop → sale returns 0.995 × 0.90 = 0.8955 per ETH.
Cycling 2.7 ETH twelve times (one Diamond day) spends ~19 ETH on packs, pays ~2.0 ETH of rake and leaves 0.72.
Nothing about tier changes this: EV per ETH is the same for Bronze and Diamond.

**2. Fertilizer is nearly worthless to a $6k farmer.** 25 Diamond slots at ~2 h turn over ~300 harvests/day = 75 ETH/day
of packs. $6k is 2.7 ETH. Slots never bind; Fert only buys speed, and speed only burns rake faster. Fert matters to
(a) whales above ~75 ETH/day, (b) Bronze/Silver spammers, (c) **the first 30 minutes of launch day**, when a
Diamond Common with 2 Fert ripens in 30 min instead of 60 and reaches the Farmer before the pool reprices.
Your stockpile (~130 units) covers that. Buy none. This also caps Fert demand: deed income from Fert sales is small
by design, which the 6 USDG price already reflects.

**3. Truffles are a pro-rata emission on pack spend.** Expected weight per harvest = 0.05 × crop value, so your expected
share of tonight's budget ≈ your pack ETH today ÷ everyone's pack ETH today (given Pigs and 48-h harvests).
Tier and speed do not change it. The only question each day is `B × 0.95 × share × price > rake`, and the Truffles
tab shows B ("Pays out today") and W ("Weight today") live. `truffle_cycle_ev()` answers it. For the first 30 days B
is the launch seed (size unpublished); after day 30 it is 5%/day of a refill fed by the rake itself, i.e. farmers
collectively get back a fraction of their own fees. **The +EV window, if there is one, is the 30-day seed.**

**4. The Farmer is the cheap door to $YIELD only while the buy tax exceeds 10.45%.** Farmer route yields 0.8955 ETH of
$YIELD per ETH of packs, tax-free. Direct pool buy yields (1 − tax). With a 90% launch tax decaying over 24 h the
Farmer wins for most of day 1; after that it depends on the normal buy tax (unpublished; hard-coded cap). `farmer_vs_direct()`.
Caveat: **the Farmer opens on its own switch with no stated date.** If it is closed on day 1, harvest anyway (crops
never wilt for selling) and hold crops in the Bag until it opens; truffle rolls happen at harvest, not sale.

**5. Pool depth is the constraint on the thesis, not slots or Fert.** At a $250k mcap the official pool's ETH side is
small. A Farmer sale "moves the $YIELD price"; the game warns above 3% slippage. $6k routed through the Farmer in one
go would move a $250k pool by a large fraction. Sell to the Farmer in clips sized to the slippage warning, over hours.
Early clips get the launch price; that, not throughput, is what day-1 speed buys.

**6. Windfall race.** A Rare burned first takes 60% of the Silo; a Mythic burned second takes 90% of the remaining 40%
(= 36%). Timing beats tier. The Silo fills at 5% of every deed-reward claim, so it is usually thin; the trade is to watch
`jackpot()` and burn one Rare only when 0.6 × Silo × price + Root Cellar > 0.94 × floor. Automated in the monitor
once $YIELD is set.

**7. The Market can run dry.** Market sales are paid from the pack float. Heavy selling to the Market after a buying
wave can hit "The Market is short on ETH". Exit timing matters; do not assume instant ETH liquidity for crops.

## Launch-day playbook (owner thesis: accumulate $YIELD)
1. **Before:** ETH on Robinhood Chain for packs + Pig + gas; Fert claimed and in the Bag; USDG unnecessary.
2. **T+0:** buy the Truffle Pig first (price unknown; buy if < ~5% of tranche). Then tranche 1: **6 Platinum packs
   (0.6 ETH ≈ $1,330)**, not Diamond: same EV per ETH, 2.5× the truffle rolls and 2.5× the Farmer clips, lower variance,
   and no single 1.25 ETH Heartbeet sale moving the pool. Plant all, 2 Fert on each.
3. **First harvests (≈30–60 min):** if the Farmer is open, sell in clips below the 3% slippage warning. If closed,
   hold crops in the Bag. Record B, W, $YIELD price, pool reserves (`abi/abi_3.json`: `ethReserve`, `spotPrice`).
4. **Decide tranche 2 only on data:** run `truffle_cycle_ev()` with the live B and W, and `farmer_vs_direct()` with the
   live buy tax. Cycle while both say yes; stop cycling the moment the truffle EV drops below the rake, and switch to
   holding crops / direct buys if the tax has decayed below 10.45%.
5. **Day 2–30:** the seed carries payouts; re-run the EV check daily at ~22:00 UTC when W is nearly final. Claim truffle
   payouts in one tx when gas is quiet. Harvest every ripe crop within 48 h.
6. **Day 30+:** payouts come only from refills. Expect the cycle EV to go negative; stop cycling unless the tab says otherwise.
7. **Never:** buy Fert; sell to the Market just to re-buy packs when truffle EV is negative; put the $2,000 reserve in.
