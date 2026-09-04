---
type: spec
capability: marginal-analysis
engagement: perfect-competition
date: 2026-08-26
status: built            # draft | built | audited
built_with: "Claude Code, from this file"
---

# <Capability> — model specification

## Purpose
This model will support the decision of how many crops to plant by type. This model must be able to answer how many beds of tomatoes, carrots, and mesclun should I plant to maximize profit and minimize costs of labor, assuming fixed costs are not changeable or neglected. 

## Inputs — the named contract
| Name | Value | Unit | Source |
|---|---|---|---|
| `TOM_PRICE`     | $8,800 | USD per 1 bed | Case scenario, crop table |
| `TOM_HRS`       | 2.5  | hours per week per 1 bed | Case scenario, crop table |
| `TOM_FERT_COST` | $880  | USD per 1 bed | Case scenario, crop table |
| `CAR_PRICE`     | $2094 | USD per 1 bed | Case scenario, crop table |
| `CAR_HRS`       | 0.833| hours per week per 1 bed | Case scenario, crop table |
| `CAR_FERT_COST` | 440  | USD per 1 bed | Case scenario, crop table |
| `MES_PRICE`     | $2700 | USD per 1 bed | Case scenario, crop table |
| `MES_HRS`       | 1.25 | hours per week per 1 bed | Case scenario, crop table |
| `MES_FERT_COST` | $880  | USD per 1 bed | Case scenario, crop table |
| 'DIM_PCT (TOM)  | 10% | per bed | Case scenario, crop table |
| 'DIM_PCT (CAR)  | 2.50% | per bed | Case scenario, crop table |
| 'DIM_PCT (MES)  | 1.25%| per bed| Case scenario, crop table|
| 'SEASON'        | 36 | Weeks | Case scenario, crop table |
| 'FIXED COSTS'   | $20,000| for 64 beds total | Case scenario, crop table|
| 'FARMER COST'   | $50,000| per 720 field hours | Case scenario, crop table|
| 'FARMER RATE'   | $34.72| per 1 hour | Case scenario, crop table|
| 'TEMP WORKER COST'| $25,000| per worker | Case scenario, crop table|
| 'TEMP WORKER RATE'| $17.36| per 1 hour | Case scenario, crop table|
| 'TOM_MAX_BEDS | 20 | for Tomatoes | Case scenario, crop table|
| 'CAR_MAX_BEDS | 20 | for Carrots |Case scenario, crop table|
| 'MES_MAX_BEDS | 30 | for Mescluns | Case scenario, crop table |


## Structure
Sheet 1: Inputs
Sheet 2: Optimization, q per crop is chosen, set MC=Price
Sheet 3: Calculation: LABOR_HRS for (q) = q x HRS_PER_BED x 36 WEEKS x (1 + DIM_PCT)^q
Sheet 4: Recommendation: how many Tomato, Carrot, and Mesclun beds should we have, and what is the total price, what is the total cost?

## Calculation logic

  LABOR_HRS for (q) = q x HRS_PER_BED x 36 WEEKS x (1 + DIM_PCT)^q
  PRICE (P) = Marginal Cost (MC)
  q is the number of beds. If there is 1 bed, q=1. If there are 5 beds, q=5.
  LABOR_HRS = hours spent per bed per week by crop
  Labor Costs for Farmer = 34.72 x HRS_PER_BED x 36 WEEKS
  Labor Costs for 1 Temp Worker = 17.36 x HRS_PER_BED x 36 WEEKS
  Weekly labor-hour capacity constraint = 40 hours per week
  Q must be a whole number
  Revenue = Crop Price x q, where price is fixed regardless of how many beds are planted.
  


## Conventions
For hours, round to the nearest minute.
For USD, round to the nearest 10th cent.


## Validation rules
Every calculated cell contains a formula.
No error cells.

## Outputs
Name of crop, and how many beds of that crop.
Total labor costs
Total Revenue
Total Labor Costs for temp workers
In perfect competition, Total Profit. Profit = Revenue - Total Costs. Total Costs = Labor Costs for Farmer + Labor Costs for Temp Workers + Fixed Costs
Fixed Costs = TOM_FERT_COST + CAR_FERT_COST + MES_FERT_COST

## Audit findings
After a first run of my spec description through Claude, here were the errors, concerns, and recommendations. I've adjusted the spec to accommodate Claude:
1. Places a builder would have to guess
WEEKS in LABOR_HRS(q) = q x HRS_PER_BED x WEEKS x (1 + DIM_PCT)^q — never appears in the Inputs table. A builder would invent a season length (12? 16? 52 weeks?).
A labor rate in USD/hour — nothing converts hours to dollars, yet "Total labor costs" is a required output and LABOR_HRS is in hours. A builder would invent a $/hr figure or, worse, silently treat hours as if they were dollars.
DIM_PCT's value and scope — named in the formula but has no row in the Inputs table, no source, and no statement of whether it's one shared constant or one per crop. A builder would pick an arbitrary small percentage.
How HRS_PER_BED maps to the three crop-specific inputs — the formula uses a generic name, but the Inputs table has TOM_HRS, CAR_HRS, MES_HRS. A builder would assume the formula runs three times, once per crop, substituting the matching *_HRS.
What counts as "Costs" in Profit = Revenue - Costs — only labor and fertilizer are modeled. A builder would assume those are the only two cost components (no seed, water, land, equipment).
The Revenue formula itself — never stated. A builder would assume Revenue = PRICE x q per crop, with price held constant regardless of volume (which happens to fit "perfect-competition" but is never said).
Any total-bed / land constraint — nothing caps how many beds exist in total. A builder would either assume unlimited land (each crop optimized independently until its own marginal cost exceeds its own price) or invent a total-bed cap to make "Optimization" solvable.
Any weekly labor-hour capacity constraint — no stated ceiling on how many hours/week are actually available. A builder might ignore this entirely or invent a cap.
The actual method in Sheet 4 "Optimization" — nothing says how the optimal q per crop is chosen (set MC = Price? grid search? calculus first-order condition?). This is the core decision logic and it's not specified.
How "marginal cost" in Sheet 3 is derived — discrete difference between Cost(q) and Cost(q-1), or a calculus derivative of the cost formula? Not stated.
Whether q must be a whole number — beds are presumably discrete, but nothing says so; a builder might allow fractional beds.
What "q = 1" means under Validation rules — is it a required test case (verify formulas behave sanely at q=1), a fixed assumption, or a stray leftover line? A builder would guess "test case."
What "round to the nearest hundredth in cents" means — read literally this could mean $0.01 or $0.0001 precision. A builder would probably guess $0.01.
What distinguishes Sheet 2 "Cost Structure" from Sheet 3 "Marginal-Cost schedules" — content boundary between the two sheets isn't defined.
2. Undefined terms

efficiency · harvest rate · DIM_PCT · WEEKS · HRS_PER_BED (as distinct from TOM_HRS/CAR_HRS/MES_HRS) · Cost Structure · Marginal-Cost schedules (as a computation, not just a sheet name) · perfect-competition (what it implies operationally for the formulas) · Optimization (method) · q (never explicitly stated to mean "beds planted of a given crop") · audited (as a status value — what criteria promote a spec from built to audited) · Costs (which line items)

3. Questions with answers missing from the document
What is WEEKS — one value shared across all three crops, or crop-specific?
What is the labor rate in USD per hour, to turn LABOR_HRS into a dollar figure?
What is DIM_PCT — a single number or per-crop, and where does its value come from?
Is there a total number of beds available across all three crops combined, or is land effectively unlimited?
Is there a weekly labor-hour ceiling (how many hours/week you actually have to work with)?
Besides fertilizer and labor, are there other cost line items that should count toward Costs?
What rule does Sheet 4 use to pick the optimal q per crop — set marginal cost equal to price, search for the profit-maximizing quantity, something else?
Is Revenue simply PRICE x q, with price fixed regardless of how many beds you plant?
Should q be restricted to whole numbers?
What does q = 1 mean under Validation rules?
"Efficiency" and "harvest rate" are named in the Purpose section but don't appear anywhere in Outputs — are those meant to be computed, or is Profit the only real objective?
What differentiates the content of Sheet 2 ("Cost Structure") from Sheet 3 ("Marginal-Cost schedules")?
Should marginal cost be computed as a discrete step (Cost(q) − Cost(q−1)) or as a continuous derivative of the cost formula?
