<!-- PR TARGET: https://github.com/richiegaas/richie-gaas | Stage 1.2 -->
# Stage 1.2 review — spec, build, audit

**Spec:** [`capabilities/marginal-analysis/spec.md`](https://github.com/richiegaas/richie-gaas/blob/main/capabilities/marginal-analysis/spec.md)

> Graded 2026-09-07 against the workbook you committed on 5 September. Two passes ago this stage was held because the model file was one byte. There is a real, working model now, it finds the right allocation, and it does so by a method almost nobody else used. The score is held down by the specification, not by the build — and there is one specific input below that closes the gap you flagged and could not find.

| Criterion | Where it stands |
|---|---|
| Spec completeness — inputs, structure, calculation flow | The inputs table has every value with a source, and the two rates are given as the unrounded ratios, which is right. Three things hold this down. Carrot hours are entered as 0.833 rather than 2.5/3, and that one input is the whole of the discrepancy you flagged — see below. The Structure section describes five sheets for a workbook that has three and numbers two different sheets "Sheet 4." And the Calculation logic still says labor cost for the farmer equals $34.72 times crop hours per bed times the number of beds, which is not what your workbook does — the workbook pools all three crops' hours and bills the first 720 of the pooled total to the farmer. Your own audit found that exact gap, twice, and the spec body never absorbed the correction. |
| Spec validation rules | The specification's Validation rules section is three lines: every calculated cell has a formula, no error cells, land on an integer under P = MC. No tolerances, no expected values, no statement of what any check would catch. The check figures that should live here — 99 hours at one tomato bed, 2,334.37 at ten, the 10/20/30 mix, the crossings at 10, 10 and 6 — are buried at the bottom of Calculation logic instead. What rescues this criterion is that the workbook computes nine rules with an ALL RULES PASS roll-up and a profit-reconciliation test to half a cent, which is more than the document ever asked for. The build is stricter than the specification, which is the wrong way round: someone rebuilding from your document would produce a weaker workbook than the one you have. |
| Workbook satisfies the contract | This is the strong half. The model is real, it has been through Excel, the named ranges are consistent, the Solver model is documented on its own sheet with all seven constraints written out, and the allocation is confirmed by full enumeration over the entire feasible grid rather than by trusting a solver — that enumeration is something almost nobody in this cohort did, and it is the only method that proves a global optimum rather than a local one. Two things cost you. The profit lands at $42,768.30 against a published $42,761.66, and the standalone crossings do not reproduce. Both are traceable and both are below. |
| Audit note | Three rounds of gap-finding, each documenting where a builder would have to guess, which terms were undefined, and which questions the document could not answer — and each round is visibly harder on the draft than the one before it. This is the best specification-auditing discipline in the cohort and it is not close. The part that earns everything this criterion asks for is what you did with the profit gap: you tried several rate and rounding variants, none landed inside the stated band, and rather than quietly absorbing the difference you wrote it into the workbook as a flagged finding with the reasoning attached. That is the correct professional response to a number you cannot reconcile. |

### The gap is one input, and it is the carrot hours

Your note says every rate and rounding variant you tried lands $6 to $13 above the published figure and never inside the band. The variant that lands on it is not a rate and not a rounding rule — it is CAR_HRS.

The case prints 0.833 as a display value. The underlying figure is 2.5/3, which is 0.8333 recurring. Across twenty carrot beds compounded at 2.5% that difference is about 0.39 of an hour, and at the blended rate it moves total cost by roughly $7.

I ran your exact model with only that one input changed and everything else — including your rounding to the nearest minute and the nearest ten cents — left alone. Profit comes out at $42,761.70, which is inside your $5 band. With no intermediate rounding at all it is $42,761.66 exactly, and total labor hours are 5,277.2161 against your 5,276.8333.

So your flag was right, your refusal to absorb it was right, and the residual was a rounded input rather than a modelling error. That is worth adding to the audit as a resolved finding: what you suspected, what you tested, what you missed, and what closed it.

### The crossings are not a third rate — they are your two rates in sequence

Your Standalone Diagnostics sheet is the best piece of thinking in this submission. You could not reproduce 10, 10 and 6 under a single costing convention, so rather than fudge it you built both readings side by side and said plainly that neither one produces all three. That is exactly right, and you were one step away.

Look at what your own two columns give you. At the pure farmer rate your carrot crossing is 10 and your mesclun crossing is 6. At the pure temporary rate your tomato crossing is 10. Every published figure is already in your sheet — just never in the same column.

The rule that produces all three at once is the farmer-first one you already use on the Model sheet, applied to each standalone schedule as well: the first 720 hours of that crop's own requirement are charged at $34.72, and only the overflow at $17.36. Carrots and mesclun never reach 720 hours until late in their schedules, so they price at the farmer rate and cross where your farmer column says. Tomatoes cross 720 hours between bed 4 and bed 5, so the top of their schedule is farmer-priced and the rest is temporary-priced, and the crossing lands at 10.

That rule also explains the one thing in this case that looks broken. On a farmer-first tomato schedule, marginal cost rises to $7,660.86 at bed 5 and then falls to $4,906.27 at bed 6, because the farmer's hours ran out and the marginal hour got cheaper. A marginal cost that falls is worth understanding, and you have the sheet to show it in.

### What to fix, and where

The workbook is in better shape than the document that is supposed to describe it, and the corrections belong in the document.

- Change CAR_HRS to 2.5/3 in the inputs table and in the sheet, and record the result in the audit.

- Rewrite the Calculation logic labor-cost lines to describe pooled hours with the farmer absorbing the first 720 — what the workbook actually does. Your audit already told you this twice.

- Fix the Structure section: three sheets, named as they are named, each described by what it must contain.

- Move the check figures out of Calculation logic and into Validation rules, each with a tolerance and a line saying what it would catch. The nine rules your workbook already computes are the list; the document just has to name them.

The rule the stage is built on is that when something is wrong you correct the specification and regenerate, so the document keeps describing what exists. Right now someone rebuilding from your spec would get a different model from the one in your repository.

---

### How to work this review

Treat this PR the way an analyst treats feedback from a senior reviewer — a review is a proposal to engage with, not a checklist to rubber-stamp.

1. **Read it yourself first.** Form your own view before you change anything. Disagreeing *with a documented reason* is a legitimate, senior response.
2. **Stress-test it with an LLM.** Paste this review and your spec into your assistant and ask it to (a) explain anything you are unsure of, and (b) argue the *other side* — where might the reviewer be wrong, and what would you give up by making each change.
3. **Then correct the spec, not the workbook.** This is the rule that makes the stage work: when a check fails, you fix the specification and regenerate, so the document keeps describing what was actually built.
4. **Close the loop.** Reply in this thread with what you changed and what you pushed back on, then commit and push.

*Your score and the per-criterion breakdown are in your Lamaku comment, not here — this repository is public.*

— Adam
