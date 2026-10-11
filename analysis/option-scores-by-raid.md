# Option scores by raid (draft, 2026-10-10)

Draft figures produced by Claude Code from a scratch optimizer script that is not in this repo. They are not outputs of `capabilities/economic-research/model.xlsx`, whose inputs and formula differ. Every number below rests on placeholder assumptions and is a draft until verified.

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
| Optimal mix | 8 batteries, 566 CRI, 13 THAAD, 96 SM-6 ($7,988M) | 8 batteries, 615 CRI, 1 SM-2, 95 SM-6 ($8,000M) | 8 batteries, 349 CRI, 48 THAAD, 96 SM-6 ($7,630M) |

The Aegis Guam system ($1.9B) is included in the current plan and optimal-mix spend. Options 2 and 3 are re-optimized for each raid; the Patriot-only option is one fixed purchase.

## Assumptions
- Prices and system costs: Table 1 as printed in the 2026-10-09 paper PDF, using midpoints where Table 1 gives a range (SM-6 $6.55M, SM-2 $2.05M). Patriot battery $0.4B without missiles; Aegis Guam $1.9B; THAAD battery already paid for. Costs are not confirmed against primary sources.
- Kill probability: 50% for one interceptor against a threat it can engage, rising as 1 - 0.5^n for n interceptors per threat. Placeholder.
- Which threats each interceptor can engage: Table 1. Patriot (MSE, CRI) cannot engage drones.
- Raid sizes (ballistic / cruise / aircraft / drones): A 40 / 30 / 10 / 50; B 15 / 80 / 20 / 60; C 10 / 30 / 10 / 300. Placeholders.
- Damage weights per leaked threat: 10 / 5 / 4 / 1. Placeholders.
- Sites: 16, threats spread evenly across sites. Aegis and THAAD interceptors can defend all 16; each Patriot battery protects up to 2 sites; up to 8 batteries; Patriot interceptors defend only the sites their batteries cover.
- Limits: $8,000M interceptor and system budget; 96 Mk 41 cells; THAAD battery holds 48; at most 500 of any interceptor type per threat class.
