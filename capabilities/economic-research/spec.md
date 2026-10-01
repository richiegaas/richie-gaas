---
type: spec
capability: economic-research
engagement: cost-exchange-ratio
date: 2026-09-30
status: draft            # draft | built | audited
built_with: "Claude Code — mechanical sections only; see 'Not included here'"
---

# Interceptor loadout allocation — research paper spec

Guam Defense System procurement, analyzed as a budget-allocation problem:
given a fixed procurement budget and a mix of threats (ballistic, cruise,
air-breathing, UAS), which interceptor types should the next dollar buy?

This supersedes the single-pairing cost-exchange framing of the prior
version of this spec. The underlying cost-exchange ratio survives as the
per-pairing metric the allocation is built on — it's now computed once per
interceptor-type/threat-type combination rather than once overall.

## Success criterion
The paper succeeds if a defense-appropriations staffer can use it to see
which interceptor type the next procurement dollar should buy, and why —
not just "more interceptors," but which type clears the highest
protection-per-dollar bar given the threats it's priced against.

## Framework: the course tools and what each one does
| Course tool | What it does in this paper |
|---|---|
| Equimarginal principle | Allocate the fixed procurement budget across interceptor types until the expected protection bought by the last dollar is equal across all of them |
| Marginal cost / cost-exchange ratio | The common currency comparing every interceptor-type / threat-type pairing: the defender's cost to stop one more threat of that type, divided by the attacker's cost to send one |
| Incentives / best response | A loadout that over-weights one threat type pushes a rational attacker toward whichever threat type is left thinnest-covered |
| Elasticity of supply | Interceptor output responds slowly to price (years-long lead times), so the "next dollar" question has a real near-term ceiling per type |
| Market structure | A few prime contractors and one buyer per interceptor line; cost-plus contracts weaken cost discipline |

## Core calculation
For each interceptor type `i` and each threat type `j` it can engage:

```
C_kill(i,j) = (n_ij x C_interceptor(i)) / P_k(i,j)
R(i,j)      = C_kill(i,j) / C_threat(j)
```

`n_ij` is interceptors of type `i` fired per threat of type `j` (often more
than one), `C_interceptor(i)` is that type's unit cost, and `P_k(i,j)` is
the probability that engagement kills the target. `R(i,j)` is the
cost-exchange ratio for that pairing — the same metric as a single
interceptor-vs-threat comparison, computed once per pairing instead of once
overall.

The loadout question: given a total procurement budget `B`, choose
quantities `q_i` of each interceptor type to maximize expected threats
averted (weighted by the threat mix Guam actually faces), subject to
`sum(q_i x C_interceptor(i)) <= B`. At an optimal loadout, the expected
protection bought by the next unit of every interceptor type in the mix is
equal — the equimarginal condition. If one type's marginal
protection-per-dollar is higher than another's, the budget should shift
toward it.

## Evidence plan
1. **Interceptor unit costs:** SM-3 IB and IIA, SM-6, THAAD, GBI, PAC-3 MSE.
   Sources: DoD budget justification books (MDA, Navy), CRS, CBO.
2. **Threat mix:** relative frequency/likelihood of ballistic, cruise,
   air-breathing, and UAS threats against Guam specifically. New to this
   framing, and likely the hardest number to source openly.
3. **Kill-probability estimates per pairing (`P_k(i,j)`):** which
   interceptor types are rated against which threat categories, and at
   what confidence. Flag every value as an estimate; state plainly where
   no open-source estimate exists.
4. **Threat missile cost estimates:** by category. Sources: CSIS Missile
   Threat, published analyst estimates, each labeled as an estimate.
5. **Budget figures:** total Guam Defense System procurement allocation by
   year, from MDA/Navy budget justification books.

## Required figure
A chart showing expected protection-per-dollar for each interceptor type
against its primary threat category. This is what makes the equimarginal
comparison visible: it should show at a glance whether the current loadout
is already roughly equalized at the margin, or tilted toward one type. A
grouped bar chart is the direct option; a scatter of cost-exchange ratio by
pairing is the fallback if protection-per-dollar proves too data-hungry to
support with open sources.

A second figure is optional: current vs. recommended loadout quantities by
interceptor type.

Figures go in `analysis/figures/`.

## Method rules
- Every cost and probability figure carries its source, year, and whether
  it's a government estimate, an analyst estimate, or assumed. Convert all
  costs to constant dollars in one base year.
- Where kill-probability or threat-mix data doesn't exist in open sources,
  say so explicitly rather than inventing a number — this is this
  framing's main data risk, flagged going in.
- Where estimates disagree, report the range and run the conclusion at
  both ends.

## AI log
Keep a dated table in `prompt-log.md`: prompt, what AI returned, what was
checked, what was kept or changed. Log every number AI suggested and the
primary source used to confirm or replace it.

## Acceptance tests
Check before submitting:
- [ ] Does the reader know which interceptor type the next dollar should
      buy, and why?
- [ ] Could the figure stand alone with its caption, and does the text use it?
- [ ] Is the recommendation still defensible if the least-certain
      kill-probability estimates are wrong in the unfavorable direction?
- [ ] Is the strongest objection — that threat mix and true `P_k` values
      can't be fully known — stated fairly and answered?
- [ ] Is every number traceable to a primary or government source, or
      explicitly labeled an estimate?

## Starting sources
Unit-cost and budget leads carry over unchanged from the prior framing.
New to this version: threat-mix and kill-probability sourcing, which
doesn't yet have a confirmed lead.

- [Breaking Defense — first ballistic intercept test from Guam](https://breakingdefense.com/2024/12/guam-missile-defenses-conduct-first-ever-ballistic-intercept/) — the system's parts (AN/TPY-6 radar, vertical launchers), the site cut from 22 to 16, and the salvo-size warning
- [Defense News — MDA's FY26 budget](https://www.defensenews.com/pentagon/2025/06/30/missile-defense-agencys-fy26-budget-targets-homeland-missile-defense/) — Guam command network and underlayer funding, plus Golden Dome
- [DoD FY2026 MDA military construction justification](https://comptroller.war.gov/Portals/45/Documents/defbudget/FY2026/budget_justification/pdfs/07_Military_Construction/10-Missile_Defense_Agency.pdf) and [FY2027 version](https://comptroller.war.gov/Portals/45/Documents/defbudget/FY2027/budget_justification/pdfs/07_Military_Construction/8-Missile_Defense_Agency.pdf) — primary source for Guam construction costs
- [CBO — Potential Costs of a National Missile Defense System](https://www.cbo.gov/publication/62422) — cost framing and interceptor cost ranges
- [Baird Maritime — pros and cons of "Fortress Guam"](https://www.bairdmaritime.com/security/weaponry/feature-weighing-the-pros-and-cons-of-fortress-guam-in-light-of-us-anti-ballistic-missile-tests) — an opposing view to use for the objection
- [The Defense Post — SM-3 Block IB production order (2026)](https://thedefensepost.com/2026/03/17/sm-3-block-ib/) — production and cost reporting
- Still to find: per-type kill-probability ratings against each threat
  category (likely the hardest to source openly), Guam-specific threat-mix
  estimates, MDA/Navy budget justification books, CSIS Missile Threat page
  on the DF-26.

## Not included here
Same discipline as the prior version of this spec: no worked argument. The
equimarginal setup above defines the *method*, not a conclusion — whether
the current loadout is actually unbalanced, and which way to shift it, is
the analysis, and it isn't written here.
