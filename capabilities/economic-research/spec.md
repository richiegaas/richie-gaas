---
type: spec
capability: economic-research
engagement: cost-exchange-ratio
date: 2026-10-01
status: draft            # draft | built | audited
built_with: "Claude Code — mechanical sections only; see 'Not included here'"
---

# Interceptor loadout allocation — research paper spec

Guam Defense System procurement, modeled as a constrained optimization: given
a fixed interceptor budget, annual production caps, and a mix of threats
(ballistic, cruise, air-breathing, UAS), which quantities of which
interceptor types maximize expected threats defeated? Built as an Excel and
Solver model, structured like the marginal-analysis engagement.

## Success criterion
The model succeeds if an appropriations staffer can see which interceptor
mix buys the most protection per dollar, how that mix moves when the raid
changes, and which assumptions the answer depends on.

## Course concepts the model uses
| Concept | Where it shows up |
|---|---|
| Equimarginal principle | At the optimum, the last dollar on every interceptor type in use buys the same extra protection |
| Diminishing marginal returns | Each added interceptor against a threat class defeats fewer additional threats than the last |
| Opportunity cost and shadow prices | The budget constraint's shadow price is the protection one more dollar would buy; production caps have shadow prices too |
| Incentives / best response | The attacker shifts its raid toward whatever the loadout covers worst, so scenarios replace a single forecast |
| Elasticity of supply | Annual production caps are hard constraints: money can't buy interceptors the factories can't make |

## Inputs — interceptor contract
Prices and system costs below are draft ranges from secondary sources, to
be replaced with budget-book figures before building. The "Check before
you build" notes flag what has to be resolved first.

| Interceptor | Named prefix | Max per loadout | Threats engaged | Price/interceptor | Cost of rest of system (1 system) | Source | Status |
|---|---|---|---|---|---|---|---|
| PAC-3 (CRI) | `PAC3_` | 12 (note 1) | ABT, CM, RW, UAS, BM, ARM | $3–4M | $1.0–1.2B per Patriot battery, shared with PAC-3 MSE (note 3) | [Norsk Luftvern cost database](https://norskluftvern.com/2026/01/03/air-defense-systems-cost-database-acquisition-interceptor-and-lifecycle-costs/); battery: [Wikipedia, citing FY2022 cost](https://en.wikipedia.org/wiki/MIM-104_Patriot) | Draft |
| PAC-3 MSE | `MSE_` | 64 (note 1) | BM, CM, ABT, ARM | $4–5.5M | Same Patriot battery as PAC-3 | Norsk Luftvern; Army missile procurement justification book (to pull) | Draft |
| THAAD | `THAAD_` | 48 | BM | $12–15M | $1.5–2.0B per battery | Norsk Luftvern; MDA budget book (to pull) | Draft |
| SM-3 (choose IB or IIA, note 6) | `SM3_` | 16 (note 2) | BM | IB $12–15M · IIA $28–36M | Aegis Guam system, shared with SM-2 and SM-6 (note 3) | Norsk Luftvern; MDA budget book (to pull) | Draft |
| SM-2 | `SM2_` | Not given (note 2) | BM, ABT, UAS (note 5) | About $2M | Aegis Guam system (shared) | [CSIS, Feb 2024](https://www.csis.org/analysis/cost-and-value-air-and-missile-defense-intercepts) | Draft |
| SM-6 | `SM6_` | 8 (note 2) | BM, CM, UAS (note 5) | $4.3M (FY2021 average) | Aegis Guam system (shared) | [Wikipedia, RIM-174](https://en.wikipedia.org/wiki/RIM-174_Standard_ERAM); Navy budget book (to pull) | Draft |

Each row becomes named inputs in the workbook: `<PREFIX>PRICE`,
`<PREFIX>MAXLOAD`, `<PREFIX>SYS_COST`, and one engagement flag per threat
class (for example `SM6_ENGAGES_CM` = TRUE).

**Threat codes:** BM = ballistic missile · CM = cruise missile · ABT =
air-breathing threat (aircraft) · RW = rotary wing (helicopter) · UAS =
drone · ARM = anti-radiation missile.

### Check before you build
1. **One unit for "loadout."** The rows mix launchers and batteries. A
   Patriot M903 launcher holds 16 PAC-3 CRI or 12 PAC-3 MSE, and a battery
   nominally has six launchers ([Wikipedia](https://en.wikipedia.org/wiki/MIM-104_Patriot)).
   THAAD's 48 matches a six-launcher battery of 8 each. The draft 12 for
   PAC-3 looks like the MSE-per-launcher figure, and 64 for MSE doesn't
   match either unit. Pick one unit (per battery or per site) and restate
   every row in it.
2. **SM-2, SM-3, and SM-6 share launcher cells.** In Aegis Guam they all
   load into the same Mk 41 cells, so separate maximums (16, 8, blank) are
   the wrong constraint. Replace them with one shared constraint,
   `SM2_Q + SM3_Q + SM6_Q <= MK41_CELLS`, using the Aegis Guam cell count
   (to source). PAC-3 CRI and MSE share Patriot launchers the same way.
3. **System cost is a fixed cost, counted once.** The first THAAD
   interceptor bought requires a whole battery; the second doesn't. The
   model needs a yes/no "build this system" decision with its fixed cost,
   and the shared Aegis Guam and Patriot costs must be counted once, not
   per interceptor type. This is the fixed-vs-marginal-cost distinction:
   price per interceptor is the marginal cost only after the system
   exists. Reported Aegis Guam figures run to about $1.9B
   ([Army Recognition, 2026](https://www.armyrecognition.com/news/army-news/2026/us-spends-1-9-billion-on-aegis-guam-missile-defense-system-to-stop-chinas-hypersonic-attacks));
   verify against MDA's books.
4. **Confirm each system is planned for Guam.** GAO confirms SM-3 and SM-6
   in the Guam Defense System
   ([GAO-25-108187](https://www.gao.gov/assets/gao-25-108187.pdf)). THAAD
   has been deployed on Guam since 2013. SM-2 and Patriot weren't
   confirmed in the sources checked so far — confirm both or label them as
   options the paper is testing.
5. **Threat lists.** SM-2 is mainly an aircraft and cruise-missile
   interceptor, with only limited terminal ballistic capability in older
   variants — check whether BM belongs in its row. SM-6's threat list had
   CM listed twice; it also engages aircraft (ABT) and, in its newest
   variant, hypersonic weapons in the terminal phase
   ([Wikipedia](https://en.wikipedia.org/wiki/RIM-174_Standard_ERAM)).
6. **Missing pieces.** Choose SM-3 IB or IIA — the price roughly doubles.
   Consider adding a hypersonic (HGV) threat column, since that's the
   threat Guam's system is most often justified against. The drone (UAS)
   layer has no low-cost interceptor yet in this table, so every drone
   would be shot down with a $2–5M missile — that gap is itself a finding
   worth keeping, not fixing.

## The model
**Decision variables.** `Q_ij` = number of interceptors of type `i`
assigned to threat class `j` (zero wherever the table above says the type
can't engage that class). Total bought of type `i`: `Q_i = sum_j Q_ij`.

**Threats defeated in each class**, which gives diminishing returns
automatically as the defense nears saturation:

```
D_j = R_j * (1 - exp(-sum_i(P_ij * Q_ij) / R_j))
```

`R_j` is the number of incoming threats of class `j` in the raid, and
`P_ij` is the single-shot kill probability of type `i` against class `j`.

**Objective.** Maximize the weighted threats defeated, where `W_j` is the
damage a leaked threat of class `j` would do:

```
max sum_j(W_j * D_j)
```

**Constraints.**
- Budget: `sum_i(C_i * Q_i) <= B`
- Production: `Q_i <= CAP_i` (annual rate x years to FY2032)
- Minimum coverage: `D_j >= FLOOR_j * R_j` for every class, so no threat
  class is abandoned
- `Q_ij` are whole numbers, >= 0
- Site coverage: Patriot batteries are limited in number and in the sites they protect; see **Site constraints** below

**Equimarginal check.** At the optimum, for every type in use, extra
protection per dollar equals the budget's shadow price `lambda`. Use this
to audit the Solver result by hand:

```
(W_j * P_ij * exp(-sum_k(P_kj * Q_kj) / R_j)) / C_i = lambda
```

## Site constraints
Added 2026-10-08. The defense is spread over 16 sites, and the three
systems do not reach them the same way. The sites and the Patriot numbers are
user-specified; the even spread of threats over sites is a placeholder.

| Rule | Value |
|---|---|
| Sites to defend (`SITES`) | 16 |
| Aegis and THAAD (`AEGIS_SITES`, `THAAD_SITES`) | Their interceptors can defend all 16 sites, but only the threat classes their `P_ij` row allows |
| Sites one Patriot battery protects (`SITES_PER_PATRIOT`) | At most 2 |
| Patriot batteries on Guam (`PATRIOT_MAX`) | 8 (the limit; the model may build fewer), so Patriot can cover all 16 sites |
| Where Patriot interceptors defend | Only the sites their batteries cover |

**Decision variables.** `b` (`PATRIOT_BATTERIES`) = number of Patriot
batteries, a whole number from 0 to `PATRIOT_MAX`. The interceptor grid
splits in two: `QC_ij` = interceptors of type `i` at Patriot-covered sites
against class `j`, and `QU_ij` = interceptors at sites without Patriot cover.
`Q_ij = QC_ij + QU_ij`. Patriot interceptors can only appear in `QC`.

**Threats defeated.** The covered share of sites is `f = min(SITES,
SITES_PER_PATRIOT x b) / SITES`, and raid threats are assumed spread evenly
across sites, so a share `f` of every class arrives at covered sites:

```
D_j = Dc_j + Du_j
Dc_j = f R_j (1 - exp(-sum_i(P_ij * QC_ij) / (f R_j)))
Du_j = (1 - f) R_j (1 - exp(-sum_i(P_ij * QU_ij) / ((1 - f) R_j)))
```

**Constraints added.**
- `b` is a whole number, `0 <= b <= PATRIOT_MAX`
- `QU_ij = 0` for the Patriot types; `QC_ij = 0` for every type when `b = 0`
- Patriot launchers across all batteries: `QC_CRI/16 + QC_MSE/12 <= PATRIOT_LAUNCHERS x b`
- The budget pays `SYS_COST_PATRIOT` once per battery

**Workbook.** `model.xlsx` carries these rules in the site-constraint
blocks below the hand checks (rows 98 to 141), the `QC` decision grid, the
five rules in rows 130 to 134 (rolled into `ALL_VALID`), and four site hand
checks. The Scenarios sheet's reference results are recomputed with the site
constraints.

## Inputs — the named contract
| Name | Meaning | Source | Status |
|---|---|---|---|
| `C_i` | Unit cost per interceptor, constant dollars | MDA, Navy, and Army budget books; CBO; CRS | To source |
| `CAP_i` | Interceptors producible through FY2032 | Budget books; production-order reporting | To source |
| `B` | Interceptor share of the Guam Defense System budget | MDA budget books; the roughly $8B program total | To source |
| `P_ij` | Single-shot kill probability | Published ranges only; classified values out of scope | Labeled assumption |
| `R_j` | Threats per class in each raid scenario | CSIS Missile Threat; analyst estimates | Labeled assumption |
| `W_j` | Relative damage of a leaked threat | Stated judgment, varied in sensitivity runs | Labeled assumption |
| `FLOOR_j` | Minimum share of each class defeated | Stated policy choice | Labeled assumption |
| `SITES` | Number of sites to defend | Arms Control Association (Oct 2025) lead lists 16 sites; not yet verified; confirmed by the user | To source |
| `SITES_PER_PATRIOT`, `PATRIOT_MAX` | Sites one Patriot battery protects (2) and the number of batteries on Guam (8, treated as the limit) | User-specified | To source |
| `AEGIS_SITES`, `THAAD_SITES` | Sites Aegis and THAAD can defend (all 16) | User-specified | To source |

## Raid scenarios
Hold the attacker's spending constant and change only how it is split, so
cheaper threats show up as larger raids:
1. **A, ballistic-heavy:** mostly medium- and intermediate-range ballistic missiles.
2. **B, cruise and air-breathing-heavy:** mostly cruise missiles and aircraft.
3. **C, drone saturation:** mostly cheap one-way attack drones.

Solve each scenario separately. Then find the **robust mix**: the single
loadout with the best worst-case result across all three (maximin). Report
the regret — how much protection the robust mix gives up compared with
each scenario's own optimum.

## Figures
1. **Required — optimal loadout by scenario.** A stacked bar chart of
   budget share by interceptor type for scenarios A, B, and C plus the
   robust mix. Shows directly whether the recommended mix depends on the
   raid.
2. **Recommended — marginal protection per dollar.** One curve per
   interceptor type against dollars spent, with the shadow-price line
   `lambda` where they meet. Makes the equimarginal principle visible.
3. **Optional — sensitivity.** A tornado chart showing how much the robust
   mix shifts when each `P_ij` and `W_j` moves across its range.

Figures go in `analysis/figures/`.

## Method rules
- Every dollar figure is in constant dollars for one stated base year,
  with source, year, and unit or procurement basis.
- Every assumption is labeled as one, with the range used in sensitivity runs.
- Cost figures for Guam-based systems should include the shipping and
  labor premium specific to the location (freight, Jones Act exposure if
  applicable, H-2B-dependent construction labor) rather than reusing
  mainland figures — verify each.
- State plainly that the model is stylized: it shows the decision rule and
  its sensitivities, not a claim to the true classified optimum.
- Build audit, as in the marginal-analysis engagement: a hand check of one
  cell, two Solver starting points, and the equimarginal check above.
- Every AI-suggested number is logged in `prompt-log.md` with the source
  that confirmed or replaced it.

## Success criteria
Check before submitting:
- [ ] Identifies and explains the challenge: what it is, who it affects, why now.
- [ ] Links it to the course's economics, micro and macro.
- [ ] Analyzes implications: the mix now, and how it changes under scenarios A, B, and C.
- [ ] Recommends a loadout or a decision rule, names who decides, and defends it against the objection.
- [ ] Figure 1 stands alone with its caption, and the text uses it.
- [ ] The recommendation survives the sensitivity runs, or the paper says exactly where it breaks.
- [ ] Every number is traceable to a primary or government source, or labeled as an assumption.

## Macro channels the model should surface
Three channels explain where the model's constraints come from and why
they tighten over time. Place this section after the scenario results and
before the recommendation, at about 600-700 words.

| Channel | Course concepts | Evidence to gather |
|---|---|---|
| Fiscal policy and opportunity cost | Government budget constraint, deficit financing, crowding out (loanable funds), opportunity cost | CBO budget outlook: defense vs. net interest outlays over time; CBO or CRS cost estimates for Golden Dome and missile defense |
| Inelastic supply and defense inflation | Price elasticity of supply, short run vs. long run, demand shocks, sector-specific (cost-push) inflation | Unit-cost trends across several years of MDA and Navy budget books; annual production rates vs. recent expenditure |
| Trade and input dependence | Supply shocks, terms of trade, comparative advantage, gains from trade vs. security externalities | USGS mineral commodity summaries (import reliance); China's export-control announcements; U.S.-Japan co-production agreements |

**How each channel enters the model:**

| Channel | Model element | What to show |
|---|---|---|
| Fiscal policy and opportunity cost | The budget `B` and its shadow price `lambda` | What one more dollar for Guam buys, and what that dollar is taken from elsewhere |
| Inelastic supply and defense inflation | Production caps `CAP_i` and rising unit costs `C_i` | Which caps bind, and how the optimal mix shifts when the scarcest interceptor gets more expensive |
| Trade and input dependence | A supply-shock scenario on `C_i` and `CAP_i` | Rerun the robust mix with critical-mineral export controls raising costs or cutting output for the most exposed interceptors |

## Starting sources
Leads for building the evidence. None has been checked against this spec
yet, and no figures are drawn from them here. Confirm every number against
a primary or government source and log it.

- [GAO-25-108187 — DOD Faces Support Challenges for Defense of Guam (May 2025)](https://www.gao.gov/assets/gao-25-108187.pdf) — components by service, the FY2027–FY2032 timeline, AN/TPY-6 halt
- [Arms Control Association — Guam missile defense system receives go-ahead (Oct 2025)](https://www.armscontrol.org/act/2025-10/news-briefs/guam-missile-defense-system-receives-go-ahead) — roughly $8B, 16 sites, SM-3 and SM-6 in Mk 41 launchers, local housing and healthcare impacts
- [Breaking Defense — first ballistic intercept test from Guam](https://breakingdefense.com/2024/12/guam-missile-defenses-conduct-first-ever-ballistic-intercept/) — the site cut from 22 to 16, salvo-size warning
- [Defense News — MDA's FY26 budget](https://www.defensenews.com/pentagon/2025/06/30/missile-defense-agencys-fy26-budget-targets-homeland-missile-defense/) — Guam command network and underlayer funding
- [DoD FY2026 MDA military construction justification](https://comptroller.war.gov/Portals/45/Documents/defbudget/FY2026/budget_justification/pdfs/07_Military_Construction/10-Missile_Defense_Agency.pdf) and [FY2027 version](https://comptroller.war.gov/Portals/45/Documents/defbudget/FY2027/budget_justification/pdfs/07_Military_Construction/8-Missile_Defense_Agency.pdf) — primary source for Guam construction costs
- [CBO — Potential Costs of a National Missile Defense System](https://www.cbo.gov/publication/62422) — interceptor cost framing
- [Army Recognition — prototype systems sent to Guam (2025)](https://www.armyrecognition.com/archives/archives-aerospace-defense/defense-news-aerospace-2025/u-s-sends-prototype-missile-defense-systems-to-guam-as-new-360-degree-shield-takes-shape) — lead for the Army layers; confirm against Army budget books
- Still to find: MDA, Navy, and Army procurement justification books for
  unit costs and production quantities (SM-3 IIA, SM-6, PAC-3 MSE, IFPC);
  CSIS Missile Threat pages for raid scenarios; published kill-probability
  ranges; USGS mineral commodity summaries; Guam Bureau of Statistics and
  Plans data.

## Not included here
Two things from the source planning document are argument, not a spec of
what to build, and stay out of this file on the same principle as before:

- **"The objection to answer"** — a worked rebuttal to "optimizing on
  unclassified guesses is meaningless." That defense is the paper's to
  make.
- **"Why this strengthens the recommendation"** (from the macro section)
  — a conclusion about what the recommendation has to pair with if
  production/input constraints bind rather than money. That's an
  analytical claim, not a model requirement.

Two build instructions that were bundled with that argument *are* included
above, stripped of their framing: the Guam-specific cost-premium note (now
under Method rules) and the "state the model is stylized" reminder (also
Method rules) — both are things the model needs to do, not conclusions
about what the paper should find.

`docs/briefs/research-brief.md` is not touched by this update.
