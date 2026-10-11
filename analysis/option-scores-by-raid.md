# Option scores by raid (draft, 2026-10-10)

Draft figures. They are the nine cells of Table 2 in the paper (`drafts/2026-10-10-draft.md`) and are produced by `capabilities/economic-research/model.xlsx` (its `Table 2` sheet shows where each number comes from) and, independently, by `capabilities/economic-research/reference-optimizer.py`. Every number rests on placeholder assumptions and is a draft until verified.

## Protection score by option and raid

Protection score = damage-weighted share of threats defeated.

| Option | Raid A (ballistic-heavy) | Raid B (cruise-heavy) | Raid C (drone saturation) | Spend |
|---|---:|---:|---:|---:|
| 8 Patriot batteries with 576 MSE only | 91.6% | 88.6% | 49.1% | $5.6B |
| Current Guam plan (Aegis + existing THAAD) | 67.5% | 53.3% | 42.5% | $3.1B |
| Optimal mix, up to 8 Patriot batteries | 97.5% | 95.0% | 59.3% | $8.0B |

Rounded to whole percents, as in Table 2: Option 1 92 / 89 / 49; Option 2 68 / 53 / 43; Option 3 98 / 95 / 59 (Raid A is 97.51%, so it rounds to 98).

## What each option buys

| Option | Raid A | Raid B | Raid C |
|---|---|---|---|
| 8 Patriot batteries with 576 MSE only | 8 batteries, 576 MSE ($5,619M) | 8 batteries, 576 MSE ($5,619M) | 8 batteries, 576 MSE ($5,619M) |
| Current Guam plan (Aegis + existing THAAD) | 48 THAAD, 96 SM-6 ($3,138M) | 48 THAAD, 96 SM-6 ($3,138M) | 48 THAAD, 96 SM-6 ($3,138M) |
| Optimal mix, up to 8 Patriot batteries | 8 batteries, 613 CRI, 96 SM-6 ($7,997M) | 8 batteries, 615 CRI, 1 SM-2, 95 SM-6 ($8,000M) | 8 batteries, 613 CRI, 96 SM-6 ($7,997M) |

The Aegis Guam system ($1.9B) is included in the current plan and optimal-mix spend. Options 2 and 3 are re-optimized for each raid; the Patriot-only option is one fixed purchase. Where two loadouts tie on protection, the cheaper one is shown (for example SM-6 and SM-3 IIA engage the same threats in the model, so the current plan uses SM-6). PAC-3 CRI is marked "not confirmed for Guam" in Table 1; CRI and MSE engage the same threats in the model, so the optimal mix buys the cheaper CRI.

## Protection per dollar (most bang for the buck)

Protection points per $B of spend (protection % divided by spend in $B), from the same nine cells:

| Option | Raid A | Raid B | Raid C |
|---|---:|---:|---:|
| 8 Patriot batteries with 576 MSE only | 16.3 | 15.8 | 8.7 |
| Current Guam plan (Aegis + existing THAAD) | 21.5 | 17.0 | 13.5 |
| Optimal mix, up to 8 Patriot batteries | 12.2 | 11.9 | 7.4 |

Best protection (%) the unrestricted model can reach at each budget, per raid (Option 3 with the budget changed; spend can be slightly below the budget). The row marked * is the budget closest to Option 1's $5.6B.

| Budget | Raid A | Raid B | Raid C |
|---|---:|---:|---:|
| $2.0B | 55.5 | 41.7 | 28.4 |
| $3.0B | 70.4 | 57.3 | 43.5 |
| $4.0B | 82.5 | 72.9 | 47.5 |
| $5.0B | 90.9 | 86.6 | 51.3 |
| $5.6B* | 91.9 | 89.6 | 54.0 |
| $6.0B | 92.1 | 90.4 | 55.1 |
| $7.0B | 95.3 | 91.5 | 58.9 |
| $8.0B | 97.5 | 95.0 | 59.3 |

The `Table 2` sheet in `model.xlsx` holds the same figures with points per $B and the extra points per extra $B between budgets. They come from the reference optimizer, not from Excel Solver.

## Assumptions
- Prices and system costs: Table 1 of the paper, using midpoints where Table 1 gives a range (SM-6 $6.55M, SM-2 $2.05M). Patriot battery $0.4B without missiles; Aegis Guam $1.9B; THAAD battery already paid for. Costs are not confirmed against primary sources.
- Kill probability: 50% for one interceptor against a threat it can engage, rising as 1 - 0.5^n for n interceptors per threat. Placeholder.
- Which threats each interceptor can engage: Table 1. Patriot (MSE, CRI) cannot engage drones.
- Raid sizes (ballistic / cruise / aircraft / drones): A 40 / 30 / 10 / 50; B 15 / 80 / 20 / 60; C 10 / 30 / 10 / 300. Placeholders.
- Damage weights per leaked threat: 10 / 5 / 4 / 1. Placeholders.
- Sites: 16, threats spread evenly across sites. Aegis and THAAD interceptors can defend all 16; each Patriot battery protects up to 2 sites; up to 8 batteries; Patriot interceptors defend only the sites their batteries cover.
- Limits: $8,000M interceptor and system budget; 96 Mk 41 cells; THAAD battery holds 48; production cap non-binding (2,000 per type).

## Provenance
- Each cell: set `OPTION`, `ACTIVE_RAID` and `BUDGET` = 8,000 in `capabilities/economic-research/model.xlsx`, then read `PROTECTION` (Model!B65). The `Table 2` sheet lists the steps and the reference value for each cell; Excel formulas evaluate each reference solution to the same protection and spend.
- Reference values: `python capabilities/economic-research/reference-optimizer.py` runs an integer program and then an exact local search that breaks ties toward the cheaper loadout.
- Excel Solver (GRG Nonlinear), run on 2026-10-10 from the reference solutions, matched the reference values for Options 1 and 2. For Option 3 it finished one of three runs (Raid C, 0.1 point below the reference) and did not return within its time limit on the other two. From rough starting points it can stall (see the workbook's Scenarios sheet, MY SOLVER RUNS). The Option 3 mixes are the best found, not proven optimal.
- Rounding: Patriot-only in the cruise-heavy raid is 88.58%, which rounds to 89, not 88. An earlier reference result of 88.50% came from the integer program's piecewise approximation of the defeat curve and was slightly below the true best allocation.
