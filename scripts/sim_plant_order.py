"""Does planting the highest-rarity seeds first beat random or shortest-first? 25 slots, 2 Fert per crop."""
import heapq, random, statistics as st, sys
ODDS = [(0.45, 0.5), (0.31, 1.0), (0.15, 1.6), (0.06, 2.0), (0.025, 3.0), (0.005, 5.0)]
PRICE = {"Gold": 0.05, "Platinum": 0.1, "Diamond": 0.25}; FACTOR = {"Gold": 108, "Platinum": 104, "Diamond": 100}

def draw(n, rng):
    return rng.choices([w for _, w in ODDS], weights=[p for p, _ in ODDS], k=n)

def run(worths, tier, order, slots=25, fert=2):
    seeds = sorted(worths, reverse=(order == "highest")) if order != "random" else worths[:]
    grow = lambda w: w * 10 * FACTOR[tier] / 500 * (1 - 0.25 * fert)
    heap, done, q = [], [], list(seeds)
    for _ in range(min(slots, len(q))):
        w = q.pop(0); heapq.heappush(heap, (grow(w), w))
    while heap:
        t, w = heapq.heappop(heap); done.append((t, w * PRICE[tier]))
        if q:
            w2 = q.pop(0); heapq.heappush(heap, (t + grow(w2), w2))
    tot = sum(v for _, v in done)
    return {"total": tot, "vw_mean_h": sum(t * v for t, v in done) / tot, "first_h": done[0][0],
            "by1h": sum(v for t, v in done if t <= 1) / tot, "by2h": sum(v for t, v in done if t <= 2) / tot,
            "all_done_h": done[-1][0], "harvests_by2h": sum(1 for t, _ in done if t <= 2)}

rng = random.Random(7)
for tier, n in (("Platinum", 34), ("Gold", 68), ("Diamond", 13)):
    res = {o: [] for o in ("highest", "random", "shortest")}
    for _ in range(4000):
        w = draw(n, rng)
        for o in res:
            res[o].append(run(w, tier, o))
    print(f"\n{n} {tier} packs ({n*PRICE[tier]:.2f} ETH), 25 slots, 2 Fert each")
    print(f"{'order':<10}{'value-weighted mean h':>22}{'first harvest h':>17}{'% value by 1h':>15}{'% by 2h':>9}{'harvests by 2h':>16}{'all done h':>12}")
    for o, rs in res.items():
        m = lambda k: st.mean(r[k] for r in rs)
        print(f"{o:<10}{m('vw_mean_h'):>22.2f}{m('first_h'):>17.2f}{m('by1h')*100:>14.0f}%{m('by2h')*100:>8.0f}%{m('harvests_by2h'):>16.1f}{m('all_done_h'):>12.2f}")
# how many packs to own 25 Rare-or-better seeds?
import math
print("\nRare-or-better share of pulls:", sum(p for p, w in ODDS if w >= 1.6), "-> packs for 25 such seeds ≈", math.ceil(25 / sum(p for p, w in ODDS if w >= 1.6)))
