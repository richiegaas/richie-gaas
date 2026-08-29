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
This model will support the decision of how many crops to plant by type. This model must be able to answer how many beds of tomatoes, carrots, and mesclun should I plant to maximize efficiency and harvest rate, and reduce and minimize costs of labor. 

## Inputs — the named contract
| Name | Value | Unit | Source |
|---|---|---|---|
| `TOM_PRICE`     | 8800 | USD per bed | Case scenario, crop table |
| `TOM_HRS`       | 2.5  | hours per week per bed | Case scenario, crop table |
| `TOM_FERT_COST` | 880  | USD per bed | Case scenario, crop table |
| `CAR_PRICE`     | 2094 | USD per bed | Case scenario, crop table |
| `CAR_HRS`       | 0.833| hours per week per bed | Case scenario, crop table |
| `CAR_FERT_COST` | 440  | USD per bed | Case scenario, crop table |
| `MES_PRICE`     | 2700 | USD per bed | Case scenario, crop table |
| `MES_HRS`       | 1.25 | hours per week per bed | Case scenario, crop table |
| `MES_FERT_COST` | 880  | USD per bed | Case scenario, crop table |


## Structure
Each sheet or region, and what it is for.

## Calculation logic
In named-range notation, never cell addresses:

  LABOR_HRS(q) = q x HRS_PER_BED x WEEKS x (1 + DIM_PCT)^q
  


## Conventions
For hours, round to the nearest minute.
For USD, round to the nearest hundredth in cents.

## Validation rules
Every calculated cell contains a formula.
No error cells.

## Outputs
By name of crop, and how many of each per bed.

## Audit findings
Added AFTER the build. For each check: what you checked, what you found, what
you did about it.
