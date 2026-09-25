---
type: spec
capability: economic-research
engagement: cost-exchange-ratio
date: 2026-09-25
status: draft            # draft | built | audited
built_with: "Claude (claude.ai), from a session titled 'Missile deterrence' — see prompt-log.md"
---

# Cost-exchange ratio — research paper spec

Guam missile defense, analyzed as a cost-exchange problem: is the U.S. building
Guam's missile defense on the expensive side of the exchange, and if so, where
should the next defense dollar go instead?

## Success criterion
The paper succeeds if a defense-appropriations staffer can use it to compare
the protection each option buys per dollar, and see which way to move the
next dollar.

## Framework: the course tools and what each one does
| Course tool | What it does in this paper |
|---|---|
| Marginal cost | Defender's cost to stop *one more* missile, compared with attacker's cost to add one |
| Equimarginal principle | Spend where the protection bought per extra dollar is highest, until all options are equal at the margin |
| Incentives / best response | The attacker picks the cheapest way to beat the defense, so the defender's choice shapes what the attacker builds |
| Elasticity of supply | Interceptor output responds slowly to price (years-long lead times), so buying more now mostly raises cost rather than stock |
| Market structure | A few prime contractors and one buyer (bilateral monopoly); cost-plus contracts weaken cost discipline |

## Core calculation
Cost to the defender of defeating one incoming missile:

```
C_kill = (n x C_interceptor) / P_k
```

Where `n` is interceptors fired per threat (often two), `C_interceptor` is
unit cost, and `P_k` is the probability the salvo kills the target. The
**cost-exchange ratio** is `C_kill` divided by the attacker's cost per
missile. A ratio above 1 means the defender pays more per exchange than the
attacker. Use published ranges, and show the result as a band rather than
one number.

## Evidence plan
1. **Interceptor unit costs:** SM-3 IB and IIA, SM-6, THAAD, GBI, PAC-3 MSE.
   Sources: DoD budget justification books (MDA, Navy), CRS, CBO.
2. **Threat missile cost estimates:** a Chinese medium-range ballistic
   missile, a cruise missile, and a one-way attack drone. Sources: CSIS
   Missile Threat, published analyst estimates, each labeled as an estimate.
3. **Alternatives' costs:** hardened shelters and fuel storage, dispersal to
   extra airfields and ports, directed-energy pilot programs, and
   left-of-launch measures (strike and cyber). Use unclassified program
   lines only.
4. **Stockpile and production:** annual production rates against recent
   expenditure. This is the short-run supply-elasticity evidence.

## Required figure
A horizontal bar chart on a log scale showing unit cost for each interceptor
beside each threat type, with a shaded band marking the cost-exchange ratio
for each pairing. The recommendation depends on this figure: it has to show
at a glance that the gap is an order of magnitude, not a rounding error.

A second figure is optional: a simple diagram of the defender's rising
marginal-cost curve against the attacker's flat one.

Figures go in `analysis/figures/`.

## Method rules
- Every cost figure carries its source, year, and whether it's procurement
  or unit cost. Convert all figures to constant dollars in one base year.
- Where estimates disagree, report the range and run the conclusion at both
  ends.
- State explicitly what the paper can't see (classified `P_k` values, true
  attacker costs).

## AI log
Keep a dated table in `prompt-log.md`: prompt, what AI returned, what was
checked, what was kept or changed. Log every number AI suggested and the
primary source used to confirm or replace it.

## Acceptance tests
Check before submitting:
- [ ] Does the reader know who should decide, and exactly what to change?
- [ ] Could the figure stand alone with its caption, and does the text use it?
- [ ] Is the conclusion still true at the unfavorable end of every cost range?
- [ ] Is the strongest objection stated fairly and answered?
- [ ] Is every number traceable to a primary or government source?

## Starting sources
Leads for building the evidence. None has been checked against this spec
yet, and no figures are drawn from them here. Confirm every number against
a primary or government source and log it.

- [Breaking Defense — first ballistic intercept test from Guam](https://breakingdefense.com/2024/12/guam-missile-defenses-conduct-first-ever-ballistic-intercept/) — the system's parts (AN/TPY-6 radar, vertical launchers), the site cut from 22 to 16, and the salvo-size warning
- [Defense News — MDA's FY26 budget](https://www.defensenews.com/pentagon/2025/06/30/missile-defense-agencys-fy26-budget-targets-homeland-missile-defense/) — Guam command network and underlayer funding, plus Golden Dome
- [DoD FY2026 MDA military construction justification](https://comptroller.war.gov/Portals/45/Documents/defbudget/FY2026/budget_justification/pdfs/07_Military_Construction/10-Missile_Defense_Agency.pdf) and [FY2027 version](https://comptroller.war.gov/Portals/45/Documents/defbudget/FY2027/budget_justification/pdfs/07_Military_Construction/8-Missile_Defense_Agency.pdf) — primary source for Guam construction costs
- [CBO — Potential Costs of a National Missile Defense System](https://www.cbo.gov/publication/62422) — cost framing and interceptor cost ranges
- [Baird Maritime — pros and cons of "Fortress Guam"](https://www.bairdmaritime.com/security/weaponry/feature-weighing-the-pros-and-cons-of-fortress-guam-in-light-of-us-anti-ballistic-missile-tests) — an opposing view to use for the objection
- [The Defense Post — SM-3 Block IB production order (2026)](https://thedefensepost.com/2026/03/17/sm-3-block-ib/) — production and cost reporting
- Still to find: MDA and Navy budget justification books (interceptor unit
  costs), CSIS Missile Threat page on the DF-26, the CBO budget and
  long-term outlook (defense vs. net interest), USGS mineral commodity
  summaries, records of China's critical-mineral export controls, and Guam
  Bureau of Statistics and Plans data on construction labor and imports.

## Not included here
The source planning document also contained a worked macro argument (a
three-channel fiscal/supply/trade case for why interceptors' true marginal
cost exceeds their sticker price) and a worked rebuttal to the "you can't
put a price on security" objection. Both are argument, not a spec of what to
build — per `AGENTS.md`, that reasoning belongs in the analysis, written by
the engagement owner, not handed over pre-written. Left out of this file on
purpose.
