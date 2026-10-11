# Option scores by raid (draft, 2026-10-10)

Draft figures. They are the nine cells of Table 2 in the paper (`drafts/2026-10-10-draft.md`) and are produced by `capabilities/economic-research/model.xlsx` (see its `Table 2` sheet for where each number comes from) and, independently, by `capabilities/economic-research/reference-optimizer.py`. Every number rests on placeholder assumptions and is a draft until verified.

## Protection score by option and raid

Protection score = damage-weighted share of threats defeated.

| Option | Raid A (ballistic-heavy) | Raid B (cruise-heavy) | Raid C (drone saturation) | Spend |
|---|---:|---:|---:|---:|
| 8 Patriot batteries with 576 MSE only | 91.6% | 88.5% | 49.0% | $5.6B |
| Current Guam plan (Aegis + existing THAAD) | 67.5% | 53.3% | 42.5% | $3.1B to $4.1B |
| Optimal mix, up to 8 Patriot batteries | 97.3% | 94.9% | 59.0% | $7.6B to $8.0B |

## What each option buys

| Option | Raid A | Raid B | Raid C |
|---|---|---|---|
| 8 Patriot batteries with 576 MSE only | 8 batteries, 576 MSE (same purchase in every raid) | same | same |
| Current Guam plan | 48 THAAD, 46 SM-3 IIA, 50 SM-6 ($4,120M) | 48 THAAD, 96 SM-6 ($3,138M) | 48 THAAD, 96 SM-6 ($3,138M) |
| Optimal mix | 8 batteries, 322 CRI, 257 MSE, 96 SM-6 ($8,000M) | 8 batteries, 615 CRI, 1 SM-2, 95 SM-6 ($8,000M) | 8 batteries, 98 CRI, 218 MSE, 48 THAAD, 96 SM-6 ($7,617M) |

The Aegis Guam system ($1.9B) is included in the current plan and optimal-mix spend. Options 2 and 3 are re-optimized for each raid; the Patriot-only option is one fixed purchase. Different mixes can tie on protection, so compare the scores and spend rather than the exact quantities. PAC-3 CRI is marked "not confirmed for Guam" in Table 1.

## Protection per dollar (most bang for the buck)

Protection points per $B of spend (protection % divided by spend in $B), from the same nine cells:

| Option | Raid A | Raid B | Raid C |
|---|---:|---:|---:|
| 8 Patriot batteries with 576 MSE only | 16.3 | 15.7 | 8.7 |
| Current Guam plan | 16.4 | 17.0 | 13.5 |
| Optimal mix, up to 8 Patriot batteries | 12.2 | 11.9 | 7.7 |

Best protection (%) the unrestricted model can reach at each budget, per raid (Option 3 with the budget changed; spend can be slightly below the budget). Option 1 sits at $5.6B; the row marked * is the budget closest to it.

| Budget | Raid A | Raid B | Raid C |
|---|---:|---:|---:|
| $2.0B | 55.5 | 41.7 | 28.4 |
| $3.0B | 70.3 | 57.3 | 43.5 |
| $4.0B | 82.5 | 72.9 | 47.5 |
| $5.0B | 90.8 | 86.6 | 51.3 |
| $5.6B* | 91.6 | 89.6 | 54.0 |
| $6.0B | 91.7 | 90.3 | 55.1 |
| $7.0B | 95.2 | 91.4 | 58.8 |
| $8.0B | 97.3 | 94.9 | 59.0 |

The `Table 2` sheet in `model.xlsx` holds the same figures with points per $B and the extra points per extra $B between budgets. These come from the reference optimizer, not from Excel Solver.

## Assumptions
- Prices and system costs: Table 1 of the paper, using midpoints where Table 1 gives a range (SM-6 $6.55M, SM-2 $2.05M). Patriot battery $0.4B without missiles; Aegis Guam $1.9B; THAAD battery already paid for. Costs are not confirmed against primary sources.
- Kill probability: 50% for one interceptor against a threat it can engage, rising as 1 - 0.5^n for n interceptors per threat. Placeholder.
- Which threats each interceptor can engage: Table 1. Patriot (MSE, CRI) cannot engage drones.
- Raid sizes (ballistic / cruise / aircraft / drones): A 40 / 30 / 10 / 50; B 15 / 80 / 20 / 60; C 10 / 30 / 10 / 300. Placeholders.
- Damage weights per leaked threat: 10 / 5 / 4 / 1. Placeholders.
- Sites: 16, threats spread evenly across sites. Aegis and THAAD interceptors can defend all 16; each Patriot battery protects up to 2 sites; up to 8 batteries; Patriot interceptors defend only the sites their batteries cover.
- Limits: $8,000M interceptor and system budget; 96 Mk 41 cells; THAAD battery holds 48; production cap non-binding (2,000 per type).

## Provenance and one check
- Each cell: set `OPTION`, `ACTIVE_RAID` and `BUDGET` = 8,000 in `capabilities/economic-research/model.xlsx`, solve, read `PROTECTION` (Model!B65). The `Table 2` sheet lists the steps and the reference value for each cell.
- Independent check: `python capabilities/economic-research/reference-optimizer.py` reproduces the nine reference solutions; Excel formulas evaluate each of them to the same protection and spend.
- Check against the paper's Table 2: eight of nine cells match after rounding. The Patriot-only option in the cruise-heavy raid is 88.5% (88.497), which rounds to 88, not 89.
