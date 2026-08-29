
# AI conventions

## About this repository
This repo is used for the BUS 626 Macro- and Micro- Economics with the DLEMBA 8 Cohort. Richie Gaas owns this repo.
Canonical file: AGENTS.md. CLAUDE.md points here.

## Where things are
- capabilities/<slug>/  a capability, named for itself in kebab-case
  (e.g. capabilities/marginal-analysis/), with its spec and model. The
  angle brackets mean "substitute the real slug" — never create a folder
  literally named <capability>. Ask me for the slug if you don't have it.
- docs/briefs/          written BEFORE work: scope + hypothesis
- docs/decisions/       written AFTER work: recommendations
- analysis/             findings and figures
- data/                 sourced inputs, with provenance

## Naming
- The directory matters most. A file in the wrong folder may not be found
  at all. If you are not certain which folder a file belongs in, ask me
  before you write it — do not choose for me.
- Graded files use the exact filename the stage brief gives — lowercase,
  hyphens, no spaces. Some courses date-stamp
  (YYYY-MM-DD-surname-slug.md, e.g. 2026-08-01-gaas-hedge-framing.md);
  the stage page says so when they do. Substitute my actual surname —
  never commit the word "surname" or "lastname" literally.
- Slugs name the engagement, never the week, the course, or the assignment
  number.
- Never invent a path or a filename. I will give you the exact one.

## How I work
- Explain concepts fully and walk the worked example. Do not hand me conclusions.
- Critique my reasoning directly. I would rather be corrected than agreed with.
- When you are uncertain, say so and say what would resolve it.

## What you may and may not draft
- You MAY explain, critique, debug, quiz me, and draft mechanical files.
- You MAY NOT write my briefs, analyses, memos, or reflections.
- Every statistic or figure you give me is a draft until I verify it against a source.

## Documentation
When work changes, update the document that describes it in the same commit.

## Scope
Do the work I asked for. If you notice something worth doing that I did not ask
for, tell me instead of doing it.

## Commits
Descriptive messages: what changed and why. Never "update" or "stuff".

## Never include
No credentials, no API keys, no personal data about anyone, no licensed or
copyrighted material. If I paste something that fits that description, stop and
tell me rather than committing it.

## Mistakes to avoid (append to this list)
Record errors here as they happen, so the same one does not repeat.
- Committed literal placeholder paths (capabilities/<capability>/spec.md,
  docs/briefs/<engagement>-brief.md, docs/decisions/<engagement>-memo.md)
  instead of substituting the real slug — had to delete and redo. It
  recurred a day later as a nested
  capabilities/<capability>/capabilities/<capability>/ duplicate.
- Committed docs/decisions/2026-08-01-lastname-hedge-framing.md — the
  literal word "lastname" from the naming-convention example, not my
  actual surname.
- Used "Update .gitignore" and "Update spec.md" as commit messages —
  no "why", the exact word this file forbids.
