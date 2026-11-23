# CornHub is live: on-chain facts and what they change (2026-11-23)

## Official docs: what changed since 20 Nov
Only the two Farmers Co-op pages (both "Updated 20 Nov 2026"); the other 17 are unchanged.
- The Co-op "each day spends some of what it collected buying `$YIELD` for farmers and deed holders".
- Its buys go three ways: **farmers, most of it, through truffles; deed holders, a share as "Co-op Rewards" for
  staked deeds; the rest burned, gone for good.**
- Flywheels page un-redacts the deed line: "a share of every daily `$YIELD` buy, as Co-op Rewards for staked deeds".
- Still redacted: Farmer/Broker payout %, `$YIELD` supply and taxes, claim fee, Windfall %, Co-op day-1 seed, the
  Classified (truffle) page. Contracts page and patch notes unchanged (no CornHub or `$YIELD` address listed).

## CornHub on mainnet (grade A: read from chain 2026-11-23 15:08 UTC)
Address `0x8C1e23Bc90F88DdC8CBA7256798aCbD745072524`, taken from the mainnet config inside the official game
client (yieldfields.fun). **It is not yet on the official links page**; compare it with the address your wallet
shows when you buy, and with that page once it is listed.

| Item | Value |
|---|---|
| Farmer fee (`farmerFeeBps`) | **6%** |
| Market/Broker fee (`marketFeeBps`) | **8%** |
| Pack fee | 0% |
| Pack prices | 0.005 / 0.01 / 0.05 / 0.1 / 0.25 ETH (match the docs) |
| Truffle Pig fee | reads 0 → not on sale yet (or free; unverified) |
| Owner | `0x93f0…dbae` (same as staking and items) |
| First sale | 2026-11-20 19:56 UTC |
| **Packs sold** | **496.1 ETH**, 1,760 purchases, **502 wallets** |
| By tier (ETH) | Diamond 357.3 (72%) · Platinum 68.5 · Gold 41.7 · Silver 19.1 · Bronze 9.5 |
| By day (ETH) | 20 Nov 117 · 21 Nov 233 · 22 Nov 110 · 23 Nov 36 (partial) |
| Concentration | top 10 wallets 27% (largest 19 ETH); median buyer 0.13 ETH |
| Contract balance | 496.1 ETH = every wei paid; nothing withdrawn |
| Owner wallet `0x139e…3952` | no purchases yet |

## What it changes
1. **The loop is cheaper than assumed.** Market exit returns 0.995 × 0.92 = 0.915 per ETH (rake 8.46%, was 10.45%).
   Farmer puts 0.935 per ETH into the swap; it beats a direct buy whenever the buy tax is above 6.5%.
   Worst-case exit on a 3.25 ETH plot ≈ 0.28 ETH.
2. **The buying is pre-committed and front-loaded.** ~464 ETH of crop value (after the Farmer fee) is waiting to be
   harvested. The rumoured starting cap is ~$250k ≈ 140 ETH. Illustration on a constant-product pool of that depth
   (pool unverified), price multiple vs launch after each rarity ripens with 2 Fert:

   | Share of presale sold to the Farmer | Commons ~0.5 h | Uncommons ~1 h | Rares ~1.6 h | Epics ~2 h | All ~5 h |
   |---|---|---|---|---|---|
   | 100% | 3.1× | 7.7× | 12.8× | 15.8× | 18.5× |
   | 50% | 1.9× | 3.6× | 5.2× | 6.2× | 7.0× |
   | 25% | 1.4× | 2.1× | 2.7× | 3.0× | 3.3× |

   Without Fert every time doubles. Either way the presale's buying is ~90% spent within 2–4 h of launch, and
   outside buyers still face the launch tax for ~a day. **The first run, if it happens, is hours long, not days.**
3. **72% Diamond is a speed bet.** A Diamond Common with 2 Fert ripens in 30.0 min, Platinum 31.2, Gold 32.4; with
   no Fert, 60. When ~100 ETH of Commons ripen in the same minutes, the first sales take most of the move.
4. **Your 3.25–3.4 ETH is 0.65% of the presale.** Your own price impact is negligible; your entry price is set by
   where you are in the queue. Fert puts you in the first cohort; clicking speed decides the rest. Scripts will be
   ahead of any manual seller.
5. **Deeds get a third `$YIELD` stream** (Co-op Rewards from daily buybacks) and `$YIELD` gets a burn.

## Plan changes
- **Launch plot: 13 Diamond (3.25 ETH)**, not the Platinum mix, **if** the Farmer is open at launch. Reason: first
  harvest 72 s earlier per crop, 13 crops to plant and fertilize instead of 25, same expected value. Cost: ±18%
  on value and a 51% chance of no day-1 Truffle. If the Farmer is not confirmed open at launch, speed is worth
  nothing: 20 Platinum + 5 Gold (2.25 ETH) and hold the rest.
- **Exit: add a clock.** `poolwatch` now also fires "sell 50%" at T+3 h if the multiple is ≥1.2 and nothing is
  sold: by then the pre-committed buying is spent. Set `launch_ts` in `data/poolwatch_state.json` on the day.
- **Buy timing unchanged**: nothing rewards buying early; 500 ETH already sits in a contract with an owner
  `withdraw`. But launch may come with short notice, so **prove the USDC → ETH → Robinhood Chain path now** with
  ~0.02 ETH and one Bronze pack, and convert the plot's ETH the moment a launch time is announced.
- Check the shop for the Truffle Pig: the contract fee reads 0, meaning not on sale yet or free.
