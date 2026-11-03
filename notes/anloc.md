# Notes: An Loc Nguyen

## 2026-10-24

## What I did
- Implemented generators, the Counted wrapper and quickselect with Claude Code (Sonnet 5.5 at medium effort).
- Quickselect has an iterative 3-way partition and a 2-way variant for the duplicates experiment.
- A 3-way split costs 1 comparison for an element less than the pivot and 2 otherwise (< then ==).
- On all_equal at n = 2000: 4,000 comparisons for select and 1,500,499 for select_two_way.

## Bugs
- The scaffold stub Counted(value, counter) conflicted with the class-level counter.
- An independent review found no wrong answer on valid input. The expected-time comment was wrong (it assumed every pivot is good).

## Decisions
- Claude Code changed the stub to Counted(value), and I told Trung.
- I added a NaN precondition and corrected the expected-time comment.

## 2026-10-30

Reconstructed from git log on 3 Nov.

## What I did
- fefce1b "docs: update README and CLAUDE.md, drop E7, ignore quick outputs": changed README.md, CLAUDE.md, .gitignore (2 lines added) and bench/adversary.py. The CLAUDE.md diff renames the project title, marks E7 as dropped, lists the run commands as e1 to e6 or all, and lists the test files.

## 2026-10-31

Reconstructed from git log on 3 Nov.

## What I did
- c40d3e0 "docs: finalize predictions P1 to P9": changed report/predictions.md (53 lines added, 15 removed).
- e783183 "docs: refine P7 and disclose numbers seen before locking": changed report/predictions.md (3 lines).

## 2026-11-01

Reconstructed from git log on 3 Nov.

## What I did
- 7d5380b "docs: record authorship and differences for predictions" and affc099 "docs: record Trung's predictions in the comparison table": both only change report/predictions.md, and both are on the branch backup-predictions, not on main.
- No commit by Nguyen An Loc on main this day. The lock commit 3ae1dd7 is by Taki (Thanh Trung Le).

## 2026-11-02

## What I did
- Thanh Trung pushed first and tagged predictions-locked on his commit.
- My rebase dropped my two predictions commits. I kept them on a local branch (recreated from commit affc099).

## Bugs
- The Authorship and Differences text in the locked file is Trung's, and "Changes An Loc made: none" is wrong.

## Decisions
- I will correct the "none" statement in the report.
- The locked P1 to P9c were drafted by Claude Code from the structure of the algorithms and then reviewed and edited by me.

## Correction, 3 Nov (from git blame -w report/predictions.md)
- The Authorship paragraph is An Loc's: heading in c40d3e0, text in e783183, both by Nguyen An Loc.
- The heading "Differences with Trung's draft" is from c40d3e0 (Nguyen An Loc). Its text, including the line "Changes An Loc made: none. We locked An Loc's draft unchanged.", was added in 3ae1dd7 by the git name Taki (Thanh Trung Le).
- So "The Authorship and Differences text in the locked file is Trung's" (2 Nov, above) is true only for the Differences text, and "Changes An Loc made: none" is in the Differences section, not in the Authorship note.

## 2026-11-03

Reconstructed from git log on 3 Nov.

## What I did
- 035b0d6 "docs: add AI error log rows and An Loc session notes": changed notes/ai-error-log.md (11 lines added) and notes/anloc.md.
- 7525174 "feat: script for E3 and E5 quickselect numbers with split < and == counts": added analysis/anloc_numbers.py and analysis/anloc_numbers.md.
- 07f63d4 "docs: correct Counted docstring on why other comparisons raise": changed the docstring in bench/counting.py (4 lines added, 3 removed).
- eb5a4d2 "feat: supplementary 300-seed test of quickselect asymmetry in k": added analysis/anloc_asymmetry.py and analysis/anloc_asymmetry.md.
- 7ce63e5 "docs: draft An Loc sections 1, 2, 4.3, 4.5 and rows P3, P8a, P8b": changed report/report.md.
- 4b6d266 "docs: update E2 counts, E5 noise wording, time statistic and P8a": changed report/report.md, analysis/anloc_numbers.py and analysis/anloc_numbers.md.
- 9247a92 "docs: fix predictions authorship wording, P8a verdict and E5 table header": changed report/report.md.
- a207d83 "docs: tidy notes": changed notes/anloc.md and notes/ai-error-log.md.
- d409fee "docs: fix P8b time, CLRS note and predictions branch note": changed report/report.md.
- 8203b4c "docs: add An Loc sections 5.2, 7, 8.1, 8.2, 8.3": changed report/report.md.
- d9168b9 "docs: correct git wording in 8.3 and trim 5.2": changed report/report.md.
