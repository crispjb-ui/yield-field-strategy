# Handoff (2026-11-11)

Everything about this position lives in this repository. A new Claude session
(any subscription) can resume from here with no other context.

## Read in this order
1. `docs/05_OWNER_THESIS.md` — the owner's thesis, the operating rules in force, dated updates.
2. `docs/01_VERIFIED_FACTS.md` — fact ledger with sources and confidence grades.
3. `docs/06_OCH_DEVLOG_2026-11-09.md` — Onchain Heroes holdings and the burn-event plan.
4. `docs/02_STRATEGY_FRAMEWORK.md`, `docs/03_AUTOMATION_PLAN.md`, `docs/04_OPEN_QUESTIONS.md`.
5. `config/mechanics.yaml` — every game number, with `null` where the docs redact it.
6. `docs/source/` — verbatim snapshots of the official docs (30 Oct and 3 Nov pages).

## Position
- 3 Rare Founding Deeds #537, #660, #661 (Fertility 6), basis 0.1 ETH each, staked with Fert Decks, wallet `0x139e79b0d01148712528d56625a2a59f676e3952`.
- $8,000 earmarked: $6,000 farming/`$YIELD`, $2,000 ETH reserve untouched before 2026-12-15.
- OCH: 41 Genesis Heroes, 2 Ringbearers, 1 mythic + 9 legendary weapons, others (Abstract; burn event late Nov).

## Running tooling
```bash
pip install -r requirements.txt && pytest
python -m yf.cli fertrate     # network Fert rate + throttle projection
python -m yf.cli deeds        # the three deeds on-chain
python -m yf.cli market       # deed collection stats
```
`config/settings.example.yaml` already holds every address; `config/settings.yaml` is optional.

## Scheduled reminder
Claude scheduled task `trig_014BCKNZPVfFwhak8pAhRcAU` ("Yield Fields: claim Fertilizer reminder + status"), every even calendar day 02:47 UTC, push notification. **It belongs to the Claude account that created it. If the subscription or account changes, recreate it from `docs/03_AUTOMATION_PLAN.md` (prompt text is in the Status table) or use a phone alarm every 2 days.** Fert Decks stop at 9/9 (72 h).

## Next triggers
- Yield Fields farming / `$YIELD` launch ("next week" per 9 Nov devlog): fill `config/mechanics.yaml` from the un-redacted docs pages and the deployed Cornhub/pool contracts (`abi/abi_2.json`, `abi/abi_3.json`), run `seed_pack_ev()`, `farm_vs_buy()`, `plots_needed()` in `yf/roi.py`, then size the first ≤$1,500 tranche.
- OCH "Crossing the chasm" docs: model point ratios per asset before deciding heroes.
- Link a non-AGW wallet at play.onchainheroes.xyz before the event (free, deadline-driven).
