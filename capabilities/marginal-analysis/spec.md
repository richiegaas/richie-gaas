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
| 'FIXED COSTS'   | $20,000| to operate entire farm | Case scenario, crop table|
| 'MAX FARMER COST'   | $24,998 | for 720 hours in the field in one season | Case scenario, crop table| descriptive context |
| 'FARMER RATE'   |50,000/1,440 | Case scenario, crop table|
| 'MAX TEMP WORKER COST'| $25,000| max 1,440 hours | Case scenario, crop table| descriptive context |
| 'TEMP WORKER RATE'| 25,000/1,440| Case scenario, crop table|
| 'TOM_MAX_BEDS | 20 | for Tomatoes | Case scenario, crop table|
| 'CAR_MAX_BEDS | 20 | for Carrots |Case scenario, crop table|
| 'MES_MAX_BEDS | 30 | for Mescluns | Case scenario, crop table |


## Structure
Sheet 1: Inputs
Sheet 2: Calculation: LABOR_HRS for (q) = q x HRS_PER_BED x 36 WEEKS x (1 + DIM_PCT)^q
Sheet 3: Optimization, number of beds (q) per crop is chosen. 64 is the max number beds allowed. Build one joint constrained optimization. The three crops are optimized jointly against the shared labor-hour and land constraints
Sheet 4: Number of Temporary Workers that should be hired
Sheet 4: Recommendation: how many Tomato, Carrot, and Mesclun beds should we have, and what is the total revenue, what is the total cost? 


## Calculation logic

  LABOR_HRS for (q) = q x HRS_PER_BED x 36 WEEKS x (1 + DIM_PCT)^q
  q is the number of beds. If there is 1 bed, q=1. If there are 5 beds, q=5.
  LABOR_HRS = hours spent per bed per week by crop
  Labor Costs for Farmer = $34.72 x Crop Hours worked per bed x Number of beds (q) 
  Labor Costs for 1 Temp Worker = $17.36 x Crop Hours worked per bed x Number of beds (q)
  Q must be a whole number
  Revenue = Crop Price x Number of beds (q), where price is fixed regardless of how many beds are planted.
  Farmer work hours have a 720 hour cap, and any hours above that get billed to temp worker(s) at $17.36/hr.
  Profit = Revenue - Total Costs. 
  Total Costs = $20,000 in Fixed Costs + Labor Costs for Farmer + Labor Costs for Temp Workers + Fertilizer costs
  Fertilizer Costs = TOM_FERT_COST x(q) + CAR_FERT_COST x (q) + MES_FERT_COST x (q)
  Fixed Costs = $20,000
  One tomato bed takes 1 x 2.50 x 36 x 1.10 = 99 hours exactly.
  Ten tomato beds take 10 x 2.50 x 36 x 1.10^10 = 2,334.37 hours.
  The optimal mix is 10 tomato / 20 carrot / 30 mesclun, and season profit is $42,762 within $5
  Standalone price-equals-marginal-cost crossings at 10, 10 and 6 beds, within one bed
  Hire as many temporary workers, maximum of up to 4 temporary workers. 


## Conventions
For hours, round to the nearest minute.
For USD, round to the nearest ten cents.


## Validation rules
Every calculated cell contains a formula.
No error cells.
Land on an integer under P = MC, or Price = Marginal Cost

## Outputs
Name of crop, and how many beds of that crop.
Total labor costs for Farmer
Total Revenue
Total Labor Costs for temp workers
In perfect competition, Total Profit.

## Audit findings

AUDIT # 3: Refined some more and addressed the following:


What "Fixed Costs" means now. Total Costs = Labor Costs for Farmer + Labor Costs for Temp Workers + Fixed Costs still uses the term "Fixed Costs," but nothing in this version defines it — the formula that used to define it got renamed to Additional Costs (see below). A builder would probably guess "Fixed Costs" is meant to be the 'EXPLICIT COSTS' input ($20,000).
Whether Additional Costs ever enters Profit. Additional Costs = TOM_FERT_COST x(q) + CAR_FERT_COST x(q) + MES_FERT_COST x(q) is defined but never referenced by Total Costs or Profit. As written, fertilizer cost drops out of the profit calculation entirely. A builder would almost certainly guess this is an oversight and fold it into Total Costs anyway.
The farmer's real hour cap. 'FARMER RATE' says "max 720 field hours," but Calculation logic says "Weekly labor-hour capacity constraint = 40 hours per week" — 40 hrs/wk × 36 weeks = 1,440 hours, not 720. A builder has to pick one. (Note: 1,440 exactly matches the temp worker's stated max, and 720 = half of 1,440 — which lines up suspiciously well with "only spends half her time in the field." A builder would likely guess the 40-hr/week line actually describes a full-time/temp-worker week, and the farmer's real cap is 20 hrs/week × 36 = 720.)
What "only spends half her time in the field" means numerically. No number is attached. A builder would guess "half of a standard 40-hour week," i.e., 20 hrs/week.
The q still missing from the two labor-cost formulas. Labor Costs for Farmer = 34.72 x HRS_PER_BED x 36 WEEKS and the temp-worker equivalent still have no q term, unlike LABOR_HRS for (q). A builder would still substitute in LABOR_HRS(q) x rate rather than build these literally.
The MAX FARMER COST ($50,000) mismatch. Her rate × her hour cap is 34.72 × 720 ≈ $25,000 — half of the stated $50,000. A builder would probably guess the $50,000 is her full (non-field-inclusive) pay and that only the ~$25,000 field-attributable portion matters here, then not use the $50,000 figure in any formula.
Whether MAX FARMER COST / MAX TEMP WORKER COST are hard budget ceilings the optimizer must respect, or just descriptive context (as before, no formula references them). A builder would likely treat them as unused, same as the earlier 'FIXED COSTS'/'EXPLICIT COSTS' input.
Sheet order vs. dependency order. "Recommendation" (Sheet 3) is listed before "Optimization" (Sheet 4), even though Sheet 3's numbers depend on Sheet 4's result. A builder would build Optimization first regardless of the stated numbering.
Whether "Total labor costs" (Outputs) is the same thing as "Labor Costs for Farmer" (Calculation logic). They're never explicitly equated. A builder would guess yes.
Rounding: "nearest 10 cent." Likely means nearest $0.10, but the prior draft used the phrase "10th cent" for the same convention, so a builder might second-guess whether a typo dropped the "th."
2. Undefined terms

Fixed Costs (used in the Total Costs formula, no longer defined anywhere) · Additional Costs (defined, but its relationship to Total Costs/Profit is unstated) · 'EXPLICIT COSTS' (never tied to any formula) · "half her time in the field" (no quantity) · MAX FARMER COST / MAX TEMP WORKER COST (never referenced by any formula) · "total price" (Sheet 3, still separate from "Total Revenue") · MC / Marginal Cost (Sheet 4 says "set MC=Price" but no MC formula is ever written) · field hours (unit on FARMER RATE)

3. Questions with answers missing from the document
Does "Fixed Costs" in the Total Costs formula refer to the 'EXPLICIT COSTS' input ($20,000)?
Should Additional Costs (fertilizer × q) be added into Total Costs / Profit, or is it intentionally excluded?
What is the farmer's actual season hour cap — 720 hours, or up to 1,440 via the 40-hr/week constraint?
Does the "40 hours per week" capacity constraint describe the farmer, a temp worker, or the combined labor pool?
Numerically, what does "only spends half her time in the field" mean?
Why is MAX FARMER COST ($50,000) roughly double what her rate × hour cap implies (~$25,000) — does the $50,000 include work outside this model?
Are MAX FARMER COST and MAX TEMP WORKER COST hard spending ceilings the optimizer must respect, or just descriptive context?
Is "Total labor costs" (Outputs) the same line item as "Labor Costs for Farmer" (Calculation logic)?
What is the actual Marginal Cost formula behind Sheet 4's MC = Price rule — labor only, or labor plus fertilizer; discrete difference or derivative?
Is "total price" (Sheet 3) the same as "Total Revenue" (Outputs)?




AUDIT # 2: Made better definitions and clarified some concerns:
The Fixed Costs contradiction. The Inputs table defines 'FIXED COSTS' as $20,000 for 64 beds total, but the Outputs section separately defines Fixed Costs = TOM_FERT_COST + CAR_FERT_COST + MES_FERT_COST (= $880 + $440 + $880 = $2,200). These are two different numbers for the same term. A builder would have to pick one — most likely the Outputs formula, since it's closer to where the number is actually consumed — and treat the $20,000 input row as unused.
Whether fertilizer cost scales with q. The Inputs table labels TOM_FERT_COST etc. as "USD per 1 bed," implying it should scale with quantity, but the Outputs formula sums the three crop constants once, with no q multiplier. A builder would guess fertilizer cost is being treated as a flat, per-season constant regardless of how many beds are planted (which is also why it landed under "Fixed Costs").
The missing q in the labor-cost formulas. Labor Costs for Farmer = 34.72 x HRS_PER_BED x 36 WEEKS has no q term at all — it doesn't grow with the number of beds, even though LABOR_HRS for (q) (defined one line earlier) explicitly does. A builder would almost certainly guess this is meant to be FARMER_RATE x LABOR_HRS(q) and silently substitute it in, rather than build the formula exactly as written.
How many temp workers, and when they kick in. Labor Costs for 1 Temp Worker is defined per worker, but nothing says how many temp workers are hired or what triggers hiring one. Given FARMER RATE ($34.72) is exactly double TEMP WORKER RATE ($17.36), and the weekly cap is 40 hrs/week × 36 weeks = 1,440 hours/season, a builder would probably guess: farmer covers hours up to the 40 hr/week cap, and any hours above that get billed to temp worker(s) at $17.36/hr. That mechanism is never stated.
FARMER COST and TEMP WORKER COST — are these used at all? The actual cost formulas run off FARMER RATE and TEMP WORKER RATE (a $/hour figure), not off FARMER COST ($50,000) or TEMP WORKER COST ($25,000). A builder would likely guess these two rows are just background context and leave them out of every formula. (Also, $50,000 ÷ 720 hours = $69.44/hr, not the stated $34.72/hr — the two farmer numbers don't reconcile with each other, which reinforces the guess that FARMER COST isn't actually wired into anything.)
Whether TOM_MAX_BEDS/CAR_MAX_BEDS/MES_MAX_BEDS cap the optimization. They sum to 70 beds, but 'FIXED COSTS' describes "64 beds total," a different number. A builder would have to guess whether 64 is a real land constraint that Sheet 2's MC = Price search must respect (on top of the per-crop caps), or just leftover context tied to the now-superseded $20,000 figure.
Whether the three crops are optimized independently or jointly. Sheet 2 says "q per crop is chosen, set MC=Price," which reads as three separate, unconstrained optimizations. But all three crops draw on the same farmer/temp labor pool and (possibly) the same 64-bed land cap. A builder would have to guess whether to run three independent P=MC solves and then check the shared constraints after the fact, or build one joint constrained optimization.
How to land on an integer q under P = MC. Since q must be a whole number, exact equality between price and marginal cost usually won't fall on an integer. A builder would likely guess "largest q where MC(q) ≤ Price," but that rule isn't stated.
Whether Marginal Cost includes fertilizer. Given fertilizer is bucketed as a flat Fixed Cost (see above), a builder would probably guess MC for the P=MC rule is derived purely from the labor-cost formula (via the (1+DIM_PCT)^q growth term), not from fertilizer.
Discrete vs. continuous marginal cost. Nothing says whether MC(q) is Cost(q) − Cost(q−1) or a calculus derivative of the exponential term. A builder would likely guess the discrete difference, since q is constrained to whole numbers.
Why "36 WEEKS" is hardcoded instead of referencing 'SEASON'. The 'SEASON' input is defined as 36 weeks, but the formulas write the literal 36 WEEKS rather than the named input. A builder would guess these are meant to be the same value and use SEASON in the actual build.
Rounding: "nearest 10th cent." Could mean nearest $0.10 or nearest $0.001 (a tenth of a cent). A builder would probably guess $0.001, reading "10th" as "one-tenth of a cent," but the phrasing supports either.
Sheet ordering. Sheet 2 (Optimization) is listed before Sheet 3 (the LABOR_HRS calculation it presumably depends on). A builder would guess the sheet numbers don't reflect a strict dependency order and build the calculation logic first regardless of sheet number.
"Total price" in Sheet 4. The Structure section asks for "what is the total price," but Outputs only defines "Total Revenue." A builder would guess these are meant to be the same thing.
2. Undefined terms

MC / Marginal Cost (as an actual formula, not just the P=MC rule) · field hours (unit on FARMER COST) · total price (Sheet 4, distinct from "Total Revenue") · "fixed costs are not changeable or neglected" (Purpose) · the "64 beds total" constraint (never tied to an explicit rule) · HRS_PER_BED (still a generic stand-in for the three crop-specific *_HRS inputs) · the DIM_PCT (TOM) / (CAR) / (MES) naming pattern (differs from the underscore-prefixed convention used everywhere else, e.g. TOM_PRICE) · how many temp workers exist / are hired

3. Questions with answers missing from the document
Which is correct: 'FIXED COSTS' = $20,000 for 64 beds, or Fixed Costs = TOM_FERT_COST + CAR_FERT_COST + MES_FERT_COST ($2,200)? Right now the document states both.
Does fertilizer cost scale with the number of beds planted (as its "per 1 bed" unit suggests), or is it a flat cost regardless of q (as the Outputs formula computes it)?
Should Labor Costs for Farmer and Labor Costs for 1 Temp Worker actually be functions of q (i.e., built from LABOR_HRS(q)), or are they genuinely meant to be flat, quantity-independent numbers as literally written?
How many temp workers can be hired, and what determines when a temp worker is used instead of the farmer — is it hours beyond the 40 hr/week cap?
Are FARMER COST ($50,000/720 hrs) and TEMP WORKER COST ($25,000/worker) used in any calculation, or are FARMER RATE/TEMP WORKER RATE the only ones actually wired into the model?
FARMER COST implies $69.44/hr (50,000 ÷ 720), but FARMER RATE is $34.72/hr — which is correct, and what does the other number represent?
Is there a real total-bed (land) constraint the optimization must respect, and is it 64 beds, or the sum of the per-crop max beds (70)?
Are TOM_MAX_BEDS, CAR_MAX_BEDS, and MES_MAX_BEDS hard caps on Sheet 2's optimization, overriding MC = Price if the unconstrained optimum would exceed them?
Are the three crops optimized independently, or jointly against the shared labor-hour and land constraints?
When MC = Price doesn't land on a whole number, what integer rule should be used — largest q with MC(q) ≤ Price, nearest q, something else?
Does Marginal Cost (for the P=MC rule) include fertilizer, or only labor?
Is Marginal Cost computed as a discrete step (Cost(q) − Cost(q−1)) or a derivative of the formula?
Should the formulas reference the 'SEASON' input, or is hardcoding "36 WEEKS" intentional?
Does "round to the nearest 10th cent" mean nearest $0.10 or nearest $0.001?
Is "total price" in Sheet 4 the same thing as "Total Revenue" in Outputs?



AUDIT # 1: After a first run of my spec description through Claude, here were the errors, concerns, and recommendations. I've adjusted the spec to accommodate Claude:
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
