---
type: spec
capability: marginal-analysis
engagement: perfect-competition
date: 2026-08-26
status: audited          # draft | built | audited
built_with: "Claude Code, from this file"
---

# Marginal analysis — model specification

## Purpose
This model supports the decision of how many beds of tomatoes, carrots, and
mesclun to plant to maximize profit, net of labor cost, assuming fixed costs
are not changeable or avoidable.

## Inputs — the named contract
| Name | Value | Unit | Source |
|---|---|---|---|
| `TOM_PRICE` | 8,800 | USD/bed | Case scenario, crop table |
| `TOM_HRS` | 2.5 | hours/week/bed | Case scenario, crop table |
| `TOM_FERT_COST` | 880 | USD/bed | Case scenario, crop table |
| `CAR_PRICE` | 2,094 | USD/bed | Case scenario, crop table |
| `CAR_HRS` | 2.5/3 (0.8333...) | hours/week/bed | Case scenario, crop table — the case prints 0.833 as a *display* value; the underlying figure is the exact fraction 2.5/3 |
| `CAR_FERT_COST` | 440 | USD/bed | Case scenario, crop table |
| `MES_PRICE` | 2,700 | USD/bed | Case scenario, crop table |
| `MES_HRS` | 1.25 | hours/week/bed | Case scenario, crop table |
| `MES_FERT_COST` | 880 | USD/bed | Case scenario, crop table |
| `TOM_DIM_PCT` | 10% | fraction/bed | Case scenario, crop table |
| `CAR_DIM_PCT` | 2.50% | fraction/bed | Case scenario, crop table |
| `MES_DIM_PCT` | 1.25% | fraction/bed | Case scenario, crop table |
| `WEEKS` | 36 | weeks | Case scenario ("SEASON") |
| `FIXED_COST` | 20,000 | USD/season | Case scenario ("FIXED COSTS", to operate entire farm) |
| `FARMER_HRS_CAP` | 720 | hours/season | Case scenario (farmer's field-hour cap before temp billing starts) |
| `MAX_FARMER_COST` | 24,998 | USD/season | Case scenario, descriptive context only — not used in any formula |
| `FARMER_RATE` | =50000/1440 (34.7222...) | USD/hour | Case scenario ("FARMER RATE") — the exact ratio, not the source table's rounded display figure ($34.72) |
| `WORKER_HRS_CAP` | 1,440 | hours/season/worker | Case scenario |
| `MAX_TEMP_WORKER_COST` | 25,000 | USD/season/worker | Case scenario, descriptive context only — not used in any formula |
| `TEMP_RATE` | =25000/1440 (17.3611...) | USD/hour | Case scenario ("TEMP WORKER RATE") — the exact ratio, not the source table's rounded display figure ($17.36) |
| `WORKER_MAX` | 4 | workers | Case scenario |
| `TOM_MAXBED` | 20 | beds | Case scenario, crop table |
| `CAR_MAXBED` | 20 | beds | Case scenario, crop table |
| `MES_MAXBED` | 30 | beds | Case scenario, crop table |
| `BEDS_TOTAL` | 64 | beds | Case scenario ("64 is the max number of beds allowed") |

## Structure
Three sheets, each described by what it must contain:
- **Model** — Inputs, Decision Variables, Per-Crop Labor Hours, a Q=1 Hand
  Check (build audit), Pooled Labor Billing, Roll-up (revenue/fertilizer/
  profit), Validation Rules, Outputs, Notes.
- **Standalone Diagnostics** — for each crop independently (its own private
  720-hour farmer allocation, ignoring the other two crops and the land
  cap): the per-bed labor-hours schedule, the farmer-first tiered cost
  schedule, and the marginal-cost-equals-price crossing.
- **Solver Model** — the embedded Excel Solver setup (objective, by-changing
  cells, all constraints) documented in plain language, the solution it
  finds, and the two-starting-point build-audit note.

## Calculation logic
In named-range notation, never cell addresses.

```
LABOR_HRS(crop)     = BEDS(crop) x HRS(crop) x WEEKS x (1 + DIM_PCT(crop)) ^ BEDS(crop)
                      [rounded to the nearest minute]
LABOR_HRS_TOTAL     = SUM over crop of LABOR_HRS(crop)

FARMER_HRS_USED     = MIN(LABOR_HRS_TOTAL, FARMER_HRS_CAP)
EXCESS_HRS          = MAX(0, LABOR_HRS_TOTAL - FARMER_HRS_CAP)
FARMER_COST         = FARMER_HRS_USED x FARMER_RATE       [rounded to the nearest USD 0.10]
TEMP_COST           = EXCESS_HRS x TEMP_RATE              [rounded to the nearest USD 0.10]
LABOR_COST          = FARMER_COST + TEMP_COST
N_WORKERS_NEEDED    = 0 if EXCESS_HRS = 0, else ROUNDUP(EXCESS_HRS / WORKER_HRS_CAP, 0)

CROP_REVENUE(crop)  = BEDS(crop) x PRICE(crop)             [price fixed regardless of q]
TOTAL_REVENUE       = SUM over crop of CROP_REVENUE(crop)
FERT_COST           = SUM over crop of (BEDS(crop) x FERT_COST(crop))
TOTAL_COST          = FIXED_COST + FERT_COST + LABOR_COST  [rounded to the nearest USD 0.10]
PROFIT              = TOTAL_REVENUE - TOTAL_COST           [rounded to the nearest USD 0.10]
```

All three crops' labor hours are pooled into one season total — this is
what the workbook actually does, and the only version of this formula that
belongs in this document. The farmer absorbs the first `FARMER_HRS_CAP`
(720) hours of the *pooled* total at `FARMER_RATE`; every hour beyond that —
regardless of which crop it came from — is billed at `TEMP_RATE`, up to a
hard capacity ceiling of `FARMER_HRS_CAP + WORKER_MAX x WORKER_HRS_CAP` =
6,480 hours. Farmer labor cost is therefore `FARMER_RATE x MIN(LABOR_HRS_TOTAL, 720)`,
never a per-bed quantity — "720 hours worked per bed" was a defect in an
earlier draft of this section (720 is a season total, not a per-bed figure)
and has been removed. There is no per-worker fixed fee — `MAX_FARMER_COST`
and `MAX_TEMP_WORKER_COST` are descriptive context only, confirmed unused in
any formula. `N_WORKERS_NEEDED` is an informational output (how many temp
workers that pooled excess implies), not a decision variable.

## Conventions
- Rounding is applied at **every** intermediate calculated cell, not only at
  the final output: hours round to the nearest minute; USD amounts round to
  the nearest USD 0.10.
- `FARMER_RATE` and `TEMP_RATE` are the unrounded ratios `50000/1440` and
  `25000/1440`, not the source table's rounded display figures ($34.72,
  $17.36) — this is the input that closed the remaining $6.67 gap between
  this workbook and the published profit figure. See Audit findings.
- `CAR_HRS` is the exact fraction `2.5/3`, not the source table's rounded
  display figure `0.833` — this is the input that closed the *original*
  profit check-figure gap. See Audit findings.
- Revenue does not erode with quantity; only labor hours inflate with `DIM_PCT`.
- Bed counts (`BEDS(crop)`) are integers.
- Whether all 64 beds must be planted, or beds may sit idle, is not stated in
  the source table; this spec assumes idle beds are allowed
  (`SUM of BEDS(crop) <= BEDS_TOTAL`, not `=`).

## Validation rules
Each rule below is computed live in the workbook (Model sheet) as its own
`TRUE`/`FALSE` cell, rolled up into one `ALL RULES PASS` cell.

| Rule | Tolerance | Catches |
|---|---|---|
| `SUM of BEDS(crop) <= BEDS_TOTAL` | exact (integer beds) | planting more beds than the 64-bed land cap allows |
| `BEDS(crop) <= MAXBED(crop)`, each crop | exact | exceeding a single crop's own per-bed cap (20/20/30) |
| `LABOR_HRS_TOTAL <= FARMER_HRS_CAP + WORKER_MAX x WORKER_HRS_CAP` | exact (6,480 hrs) | a labor plan that needs more hours than the farmer plus 4 temp workers can supply |
| `N_WORKERS_NEEDED <= WORKER_MAX` | exact | an allocation that implies hiring more than 4 temp workers |
| `BEDS(crop) = INT(BEDS(crop))`, each crop | exact | a fractional bed count leaking through |
| `TOTAL_REVENUE - FIXED_COST - FERT_COST - LABOR_COST = PROFIT` | within USD 0.005 | rounding drift between the rolled-up profit and its component parts |
| Q=1 hand check (4 sub-checks: 99 hrs at one tomato bed, 2,334.37 hrs at ten, $8,800 revenue at one bed, $3,437.50 farmer-rate labor cost at one bed) | exact | a formula that behaves correctly in aggregate but is wrong at the smallest, hand-verifiable case |
| Every calculated cell contains a formula | structural (build-time) | a pasted value silently replacing a live formula |
| No error cells | structural (build-time) | a broken reference, div/0, or #NAME? anywhere in the workbook |

Check figures (acceptance criteria, not build-time rules — verified against
the Model sheet and Standalone Diagnostics sheet after each build):
- One tomato bed takes `1 x 2.50 x 36 x 1.10 = 99` hours exactly.
- Ten tomato beds take `10 x 2.50 x 36 x 1.10^10 = 2,334.37` hours.
- Optimal mix: `BEDS_TOM = 10, BEDS_CAR = 20, BEDS_MES = 30`, season profit
  **$42,762, within $5**. Resolved — see Audit findings: the gap was two
  inputs (`CAR_HRS`, then `FARMER_RATE`/`TEMP_RATE`), not a modeling error.
- Standalone (single-crop, farmer-first-tiered, unconstrained by the shared
  labor pool or the other crops) price-equals-marginal-cost crossings at
  **10, 10, and 6 beds** (tomato, carrot, mesclun) — the first bed at which
  marginal cost exceeds price, reading each crop's own tiered schedule.

## Outputs
- `BEDS(crop)` and name, for each of tomatoes, carrots, mesclun.
- `N_WORKERS_NEEDED`.
- `FARMER_COST` (total labor cost for the farmer).
- `TEMP_COST` (total labor cost for temp workers).
- `TOTAL_REVENUE`.
- `PROFIT`.

## Audit findings
Three rounds of gap-finding against the *document* (2026-08-24 through
2026-09-05), followed by a build audit against the *workbook* (2026-09-24),
per the review on PR #3.

### Build audit (2026-09-24) — validation rules run against the workbook

The prior audit rounds read the specification and listed what a builder
would have to guess. This round runs the specification's own checks against
the file that already exists, per the review's instruction to audit the
build, not just the document.

1. **Q=1 hand check.** Set up as a standalone formula block on the Model
   sheet (not by changing the live decision cells): one tomato bed's
   `LABOR_HRS`, revenue, and farmer-rate labor cost, each computed by
   formula and compared against an independently hand-computed value. All
   four sub-checks read `TRUE`: 99.0000 hrs, 2,334.3667 hrs (ten beds),
   $8,800 revenue, $3,437.50 labor cost.
2. **Scan for pasted values.** Every cell in the workbook was classified as
   formula vs. numeric literal, and every literal cross-referenced against
   the workbook's own named ranges. Result: 342 formula cells; 108 numeric
   literals, of which 25 are the designated blue/yellow input and decision
   cells (expected) and the remaining 83 are either the `q` index column in
   the three Standalone Diagnostics tables (0..20 or 0..30, a row counter,
   not a calculated result), the deliberate hand-computed reference values
   in the Q=1 check's "Hand math" column, or the Solver Model sheet's prose
   documentation of the answer. No unexplained literal was found sitting
   where a formula should be.
3. **Two Solver starting points.** Excel's Evolutionary engine hangs under
   headless COM automation in this build environment — confirmed directly:
   `SolverOk`/`SolverAdd` return immediately, but `SolverSolve` does not
   return within several minutes, reproduced twice. Substituted a
   coordinate-ascent local search (Python, independent of the workbook's
   formulas) run from two extreme starting points, `(0, 0, 0)` and
   `(20, 20, 30)`; both converge to `10 / 20 / 30` at `$42,761.70`. This is
   a corroborating check, not the primary proof — full enumeration (below)
   already establishes global optimality over the entire feasible grid,
   which a two-start check cannot.
4. **Independent cross-check.** No access to the Farm Profit Lab reference
   tool from this environment. Substituted a from-scratch Python
   reimplementation of the model, typed directly from this document rather
   than copied from the workbook's formulas: `10 / 20 / 30` returns
   `$42,761.70`, matching the workbook's `PROFIT` cell to the cent.

### Resolved (2026-09-24) — the remaining $6.67, from PR #3's second review

After the `CAR_HRS` fix (below) reached the workbook, profit read $42,768.30
against a published $42,761.66 — a $6.67 gap. The reviewer traced it to the
same defect as the carrot hours, in two more places: `$34.72/hr` is a
rounded display of `50,000 / 1,440` = `$34.7222...`, and `$17.36/hr` is a
rounded display of `25,000 / 1,440` = `$17.3611...`. Verified independently:
deriving both rates as the exact ratios, with every other input, rate, and
rounding rule unchanged, gives **$42,761.70** with this workbook's
minute/dime rounding and **$42,761.66** with none — matching the published
figure to the cent. Re-ran the full enumeration with both corrections in
place: `10 / 20 / 30` remains the exact global optimum.

The same review also caught a regression: an intermediate edit to this
document's Calculation logic read `Labor Costs for Farmer = $34.72 x 720
hours worked per bed x Number of beds (q)` — not a quantity that exists,
since 720 is a season total, not a per-bed figure. The Calculation logic
section above has been rewritten to describe only the pooled, farmer-first
formula the workbook actually runs.

### Resolved (2026-09-07, from PR #3's first review)

- **The profit gap was `CAR_HRS`, not a rate or rounding choice.** Every
  rate/rounding variant tried in the prior audit round (rounded table rates
  $34.72/$17.36, unrounded `50000/1440`/`25000/1440`, `24998/720` for the
  farmer rate) landed $6–13 above the published $42,762, never inside the
  ±$5 band. The actual gap was `CAR_HRS`: the case prints `0.833` as a
  display value, but the underlying figure is the exact fraction `2.5/3`
  (0.8333...). Across twenty carrot beds compounded at 2.5% diminishing
  returns, that difference is about 0.39 labor-hours; at the blended
  farmer/temp rate it moves total cost by roughly $7. Verified
  independently by re-running the full enumeration: `10 / 20 / 30` remains
  the exact global optimum with the corrected `CAR_HRS`.
- **Standalone MC=Price crossings, resolved — with one correction to the
  reviewer's proposed rule.** The reviewer proposed applying the Model
  sheet's farmer-first tiered billing to each crop's own standalone
  schedule (each crop gets a private 720-hour farmer allocation, overflow
  at `TEMP_RATE`), reading the crossing off that single tiered schedule
  instead of the two separate all-farmer / all-temp columns. Verified
  independently: **the tiered rule only reproduces `10, 10, 6` if the
  crossing is read as the *first* bed where marginal cost exceeds price**
  (the standard introductory-economics stopping rule), **not the *last*
  bed satisfying `MC <= price`.** These two readings diverge here because
  the tiered schedule is not monotonic — once a crop's pooled hours pass
  720, the marginal hour gets *cheaper* (temp rate is half the farmer
  rate), so marginal cost can fall back under price after an earlier
  violation. Recomputing full standalone profit-maximization (which is the
  economically rigorous answer when marginal cost is non-monotonic, and is
  what "last bed with `MC <= price`" actually finds) gives `10, 20, 30` for
  the three crops — the *same* quantities as the real joint optimum, not
  `10, 10, 6` — because a rational planner facing unlimited standalone temp
  labor has no reason to stop once the marginal hour gets cheap again. The
  spec's check figure and the reviewer's narrative both anchor to the
  simpler, conventional "stop at the first unprofitable unit" rule, which
  *does* reproduce `10, 10, 6` exactly and is implemented as such in the
  Standalone Diagnostics sheet, including the marginal-cost drop the
  reviewer flagged (tomato bed 5 to bed 6: $7,660.86 down to $4,906.27, the
  moment the farmer's 720 hours run out and the marginal hour turns
  cheaper).

### AUDIT # 3
What "Fixed Costs" means now. Total Costs = Labor Costs for Farmer + Labor Costs for Temp Workers + Fixed Costs still uses the term "Fixed Costs," but nothing in this version defines it — the formula that used to define it got renamed to Additional Costs (see below). A builder would probably guess "Fixed Costs" is meant to be the 'EXPLICIT COSTS' input ($20,000).
Whether Additional Costs ever enters Profit. Additional Costs = TOM_FERT_COST x(q) + CAR_FERT_COST x(q) + MES_FERT_COST x(q) is defined but never referenced by Total Costs or Profit. As written, fertilizer cost drops out of the profit calculation entirely. A builder would almost certainly guess this is an oversight and fold it into Total Costs anyway.
The farmer's real hour cap. 'FARMER RATE' says "max 720 field hours," but Calculation logic says "Weekly labor-hour capacity constraint = 40 hours per week" — 40 hrs/wk × 36 weeks = 1,440 hours, not 720. A builder has to pick one.
What "only spends half her time in the field" means numerically. No number is attached.
The q still missing from the two labor-cost formulas.
The MAX FARMER COST ($50,000) mismatch.
Whether MAX FARMER COST / MAX TEMP WORKER COST are hard budget ceilings the optimizer must respect, or just descriptive context.
Sheet order vs. dependency order.
Whether "Total labor costs" (Outputs) is the same thing as "Labor Costs for Farmer" (Calculation logic).
Rounding: "nearest 10 cent" vs "10th cent."

### AUDIT # 2
The Fixed Costs contradiction between the Inputs table ($20,000) and an Outputs-section formula ($2,200).
Whether fertilizer cost scales with q.
The missing q in the labor-cost formulas.
How many temp workers, and when they kick in.
Whether FARMER COST/TEMP WORKER COST are used at all, versus FARMER RATE/TEMP WORKER RATE.
Whether TOM_MAX_BEDS/CAR_MAX_BEDS/MES_MAX_BEDS (sum 70) cap the optimization, versus the 64-bed land figure.
Whether the three crops are optimized independently or jointly.
How to land on an integer q under P = MC.
Whether Marginal Cost includes fertilizer.
Discrete vs. continuous marginal cost.
Why "36 WEEKS" is hardcoded instead of referencing 'SEASON'.
Rounding: "nearest 10th cent" — $0.10 or $0.001?
Sheet ordering vs. dependency order.
"Total price" (Sheet 4) vs "Total Revenue" (Outputs).

### AUDIT # 1
WEEKS never appears in the Inputs table.
No labor rate in USD/hour to turn LABOR_HRS into a dollar figure.
DIM_PCT's value and scope undefined.
How HRS_PER_BED maps to the three crop-specific inputs.
What counts as "Costs" in Profit = Revenue - Costs.
The Revenue formula itself never stated.
No total-bed / land constraint stated.
No weekly labor-hour capacity constraint stated.
The actual method in "Optimization" never specified.
How "marginal cost" is derived — discrete or continuous.
Whether q must be a whole number.
What "q = 1" means under Validation rules.
What "round to the nearest hundredth in cents" means.
What distinguishes "Cost Structure" from "Marginal-Cost schedules."
