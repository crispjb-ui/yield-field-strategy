# $YIELD exit plan: accumulate at launch, sell the first run (2026-11-20)

Owner thesis: get as much `$YIELD` as possible as soon after launch as possible, hold through the first run-up,
sell before it dumps. Supersedes the "hold with no target" rule of 30 Oct. Everything about the pool below is
from the docs and the bundled ABI; the tax rates, launch-tax curve and pool depth are unpublished.

## What the mechanics say about this trade
1. **The first run is Farmer-driven.** Every Farmer sale is a tax-free pool buy. Open-market buyers pay the launch
   tax (team "leaning" ~90% decaying over ~24 h), so in the first hours almost all buying is farmers. The run
   lasts as long as pack ETH keeps flowing through the Farmer.
2. **The sell tax punishes the late exit.** "Once net selling passes a set level, the sell tax climbs to a hard
   cap, then eases back. Buys cancel out sells, and splitting a sale doesn't avoid it." You cannot sell *after*
   the turn cheaply. The exit has to happen into net buying, i.e. on the way up, by rule.
3. **Farmers who want ETH never touch the pool.** They use the Market. Pool sell pressure comes from three known
   sources, two of them on a clock:
   - Farmer-route holders taking profit (this trade; everyone running it);
   - **the first Truffle settlement at 00:00 UTC after launch**: the launch seed's first daily release reaches
     farmers as new, free `$YIELD`, claimable in one transaction;
   - deed rewards, released half every 8 h from launch.
   The first 00:00 UTC is the first moment a large amount of zero-cost `$YIELD` exists. Be de-risked before it.
4. **Launch-tax expiry (~24 h) cuts both ways**: speculators can finally buy (a possible second leg), and the
   Farmer's edge over a direct buy ends.
5. **Round trip cost.** In through the Farmer at ~10% fee, out through the sell tax:

   | Sell tax | Price multiple to beat having used the Market | to get the pack ETH back |
   |---|---|---|
   | 5% | 1.05× | 1.18× |
   | 10% | 1.11× | 1.24× |
   | 15% | 1.18× | 1.31× |
   | 25% (heavy selling) | 1.33× | 1.49× |

6. **Each harvested crop is an option.** It can go to the Farmer (buy `$YIELD` at the current price) or the Market
   (ETH at a fixed ~90%), and it never wilts for selling. Early crops → Farmer. Crops that ripen after the price
   has already run (Legendary and Mythic ripen at 3–5 h) → Market, or hold in the Bag. Do not buy the top with
   your slowest 10% of value.

## The ladder (encoded in `yf/poolwatch.py`, 37 tests)
Decision variable: **(ETH already realized + what the bag would fetch right now, net of tax and slippage) ÷ ETH
spent on packs.** The pool's own `quoteYieldForEth(balance)` gives the middle term exactly.

| Trigger | Action |
|---|---|
| Multiple ≥ 2.0 | Sell 50% of the bag. Principal is back. |
| Multiple ≥ 3.5 | Sell 50% of what is left. |
| Multiple falls 30% from its peak, after having been ≥ 1.5 | Sell down to a 15% moonbag. |
| 45 min before the first 00:00 UTC settlement, nothing sold yet, multiple ≥ 1.2 | Sell 50% of the bag. |
| Multiple < 0.9 and never reached 1.5 | Thesis failed. Stop adding. No forced sale into a raised sell tax; reassess when the tax has eased. |

Run on launch day (any machine with Python; read-only, no keys):
```bash
python -m yf.cli poolwatch --pool <POOL_ADDRESS> --wallet 0x139e79b0d01148712528d56625a2a59f676e3952 --cost-eth 3.40
```
It prints the multiple, both live taxes, a heavy-selling flag, and `ACTION:` lines every 20 s. After each sale,
update `stage` and `realized_eth` in `data/poolwatch_state.json`. Sells are manual, sized under the game's 3%
slippage warning.

## Limits of this plan
- "Before it dumps" is not observable in advance. The ladder accepts selling too early on half the bag in
  exchange for never round-tripping the whole position.
- If the Farmer is closed at launch there is no early accumulation and no edge; the conditional plot in
  `08_PRELAUNCH_PACK_PLAN` applies.
- Team controls the pool ("can add, remove or rebalance") with no timelock. No rule here protects against that.
- The 2.0 / 3.5 / 30% numbers are judgement, not derived. Change them in `Rules` if you want a different shape.
