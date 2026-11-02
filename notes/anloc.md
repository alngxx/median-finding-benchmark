# Notes: An Loc Nguyen

One entry per working session. Copy the block below for each new session.

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

## 2026-11-02

## What I did
- Thanh Trung pushed first and tagged predictions-locked on his commit.
- My rebase dropped my two predictions commits. I kept them on a local branch (recreated from commit affc099).

## Bugs
- The Authorship and Differences text in the locked file is Trung's, and "Changes An Loc made: none" is wrong.

## Decisions
- I will correct the "none" statement in the report.
- The locked P1 to P9c were drafted by Claude Code from the structure of the algorithms and then reviewed and edited by me.
