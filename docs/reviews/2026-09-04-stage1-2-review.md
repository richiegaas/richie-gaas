<!-- PR TARGET: https://github.com/richiegaas/richie-gaas | Stage 1.2 -->
# Stage 1.2 review — spec, build, audit

**Spec:** [`capabilities/marginal-analysis/spec.md`](https://github.com/richiegaas/richie-gaas/blob/main/capabilities/marginal-analysis/spec.md)

> Graded 2026-09-04, first pass on this stage. Your specification went from under two thousand bytes to nearly twenty-one thousand and it is now genuinely about this case, with the labor function written correctly. The gap-finding you ran against it is the most thorough work of its kind anyone in this cohort has done — and it is also the reason the score is where it is, because you found the defects and left them in.

| Criterion | Where it stands |
|---|---|
| Spec completeness — inputs, structure, calculation flow | Real and buildable in outline. Every case input is present with a value and a source, the four sheets are named with a purpose each, and the labor function is correct with the exponent on q — LABOR_HRS(q) = q x HRS_PER_BED x 36 x (1 + DIM_PCT)^q — which is the single thing most likely to be got wrong here. What holds it back is the set of contradictions your own audit lists and the document still contains: the farmer's cap is 720 hours in one place and a 40-hour week in another, which is 1,440; fertilizer is defined as Additional Costs and then never enters the profit formula; "Fixed Costs" is used in Total Costs and is no longer defined anywhere; and the two labor-cost formulas have no q in them, so they do not grow with the number of beds. |
| Spec validation rules | Two lines: every calculated cell contains a formula, and no error cells. Both are worth having and neither can tell you the model is right. There is no acceptance figure from the case, no hand-calculated anchor, no tolerance, and no procedure for running the optimizer twice from different starting points. This is the cheapest large gain available to you and it is perhaps forty minutes of work. |
| Workbook satisfies the contract | capabilities/marginal-analysis/model.xlsx is a one-byte placeholder. The specification frontmatter reads status: built and built_with: "Claude Code, from this file", so the document asserts a workbook that does not exist. Nothing is lost yet — the stage is not due until 6 September — but the frontmatter should say draft until it is true. |
| Audit note | Three rounds of gap-finding, and as a piece of thinking it is the strongest in the cohort — see below. It is scored here at less than half because an audit in this stage is run after the build, against the workbook, and records what you did about each finding. Yours is a critique of the document with no build behind it and no actions recorded. |

> The spec-side criteria are summarised above. Held rather than entered — with no workbook, a total would misdescribe the work, and there are two days left.

### Your audit is the best gap-finding in the cohort and you stopped one step short

Read what you produced. Across three rounds you identified that the farmer's hour cap contradicts itself, that fertilizer never enters profit, that "Fixed Costs" lost its definition when a formula was renamed, that two labor-cost formulas are missing their q, that $50,000 divided by 720 hours does not give $34.72, that nothing states how many temporary workers are hired or what triggers hiring one, that the sheets are numbered out of dependency order, that no rule says how to land on an integer under P = MC, and that "nearest 10th cent" could mean two different things.

Every one of those is real. Several of them — the missing q, the undefined Fixed Costs, the fertilizer dropping out of profit — would produce a workbook that runs cleanly and returns a wrong answer, which is the most dangerous kind of defect there is.

And then the specification still says all of those things. The audit is a list of questions rather than a record of corrections. You did the hard part — finding them — and skipped the easy part.

That is the one habit to change, and it is worth more to you than any single fix: when a gap-finding pass returns a defect, the next commit closes it. Otherwise the document tells a builder both that it is ambiguous and that you knew.

### The four to close first, in order

- The farmer's hours. Pick 720 for the season and delete the 40-hour week line. Your own audit works out why 720 is right — half of a 40-hour week over 36 weeks — so write the conclusion into the document and remove the alternative.

- Fertilizer into profit. Total Costs = fertilizer + labor + the $20,000 fixed cost. Right now fertilizer is defined and orphaned, so a builder either drops $44,000 of real cost or guesses.

- The missing q. Labor cost is the rate multiplied by LABOR_HRS(q), which already contains the 36 weeks. As currently written the formula multiplies by 36 a second time and never scales with beds at all.

- Rates from their sources. FARMER_RATE is 50,000 divided by 1,440 and TEMP_RATE is 25,000 divided by 1,440, entered as those divisions rather than as $34.72 and $17.36. Another workbook in this cohort came out $13.16 high on a $42,762 profit from exactly that rounding, and its own check caught it.

### Then the validation section, which is forty minutes and worth the most

Four rows with required values, so the workbook can fail visibly:

- One tomato bed takes 1 x 2.50 x 36 x 1.10 = 99 hours exactly.

- Ten tomato beds take 10 x 2.50 x 36 x 1.10^10 = 2,334.37 hours. This is the one that catches a model applying the rate once instead of compounding it per bed — a defect that passes the q = 1 check perfectly.

- The optimal mix is 10 tomato / 20 carrot / 30 mesclun, and season profit is $42,762 within $5. The tolerance matters: a check with no tolerance either passes by luck or fails on rounding.

- Standalone price-equals-marginal-cost crossings at 10, 10 and 6 beds, within one bed.

Those four rows are what turn a description into a contract. With two days left they are worth more than any further writing in the body.

---

### How to work this review

Treat this PR the way an analyst treats feedback from a senior reviewer — a review is a proposal to engage with, not a checklist to rubber-stamp.

1. **Read it yourself first.** Form your own view before you change anything. Disagreeing *with a documented reason* is a legitimate, senior response.
2. **Stress-test it with an LLM.** Paste this review and your spec into your assistant and ask it to (a) explain anything you are unsure of, and (b) argue the *other side*.
3. **Then correct the spec, not the workbook.** When a check fails, you fix the specification and regenerate, so the document keeps describing what was actually built.
4. **Close the loop.** Reply in this thread with what you changed and what you pushed back on, then commit and push.

*Your score and the per-criterion breakdown are in your Lamaku comment, not here — this repository is public.*

— Adam
