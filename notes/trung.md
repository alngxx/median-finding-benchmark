# Notes: Thanh Trung Le

One entry per working session. Copy the block below for each new session.

Entries before 28 Oct were reconstructed on 3 Nov from my chat history with Claude and the git log.

## 2026-10-20 / 21

## What I did
- Agreed the topic with An Loc: median finding, randomized quickselect vs deterministic median of medians (Theme 2).
- Accepted the role swap in An Loc's plan version 2: I am primary author of median of medians and also write the runner and the plots.
- Claude built an earlier scaffold (`pa2-selection`) with a runner for E1 to E5 and tested it with temporary implementations. That scaffold was not used directly; parts of its runner and plots were adapted later.

## Decisions
- Use An Loc's repository (`alngxx/median-finding-benchmark`) as the only repository.

## 2026-10-24

## What I did
- Read An Loc's brief and, with Claude, wrote a revised plan: dated schedule, E2 `select_two_way` at n = 10^4, E6 up to 10^5 with 5 instances, E8 dropped.

## Decisions
- E2 `select_two_way` cannot run at n = 10^5: An Loc's 1,500,499 comparisons at n = 2000 is about 0.375 n^2, so about 3.75 * 10^9 comparisons per call.

## 2026-10-25

## What I did
- Median of medians (`selection/median_of_medians.py`): Claude wrote it at my request, I read it and ran it. Groups of g (default 5), 3-way partition, only the pivot step is recursive, the rest is a loop.
- Checked on a clone of the repo: the shared contract tests pass; it is correct on the six families and on strings; it runs only with `<` and `==` (through `Counted`); n = 10^6 takes about 1.2 s; it works with the recursion limit set to 100.

## Decisions
- `BASE_CUTOFF = 25` for every group size, not 5 * g as in the original prompt, so that E4 compares group sizes alone.

## 2026-10-26

## What I did
- `tests/test_median_of_medians.py` (written by Claude).
- Mutation testing: injected bugs into median of medians one at a time and checked whether the tests fail.
- Pushed median of medians and its tests (974cee9).

## Bugs
- Two injected bugs passed every test because they still return right answers: pivot = first group median (loses the O(n) guarantee; the test run went from about 4 s to 51 s) and the recursive call ignoring `group_size` (would make E4 wrong). Added a "comparisons below 30n on every family" test and a test of the group size passed to the recursive call. Both bugs are now caught.
- `git push` failed with 403: my account was not a collaborator. An Loc added me.

## 2026-10-27 / 28

## What I did
- `bench/run_bench.py`, `bench/plot.py`, `tests/test_bench_smoke.py` (adapted with Claude from the earlier scaffold): e1 to e6, `all`, e7 refused with a message, `--quick`, `--max-n`, `--out`, the `prefix_len` column, every answer checked against `sorted(a)[k]`, and quickselect and median of medians must agree. Plots show the spread (IQR bands and error bars).
- 207 tests pass. Pushed (0747e10).
- Claude ran a 2-instance pilot of the harness and told me a few rough findings (listed in `notes/pilot-numbers-seen.md`).

## Bugs
- The first plots had overlapping labels and legends. Fixed after looking at the rendered figures.

## 2026-10-28 / 29

## What I did
- Ran pytest (207 passed) on Windows, Python 3.13.1, in a new .venv.
- Ran the full e1-e6 (3230 s) before predictions were locked. Moved the output to ../pilot-run-28oct without opening it. Will re-run after the predictions-locked tag.

## Bugs
- `python` pointed to MSYS2 Python without pip, while `pytest` used another Python, so matplotlib was missing for `python`. Fixed with a .venv from `py`.

## Decisions
- Always run through .venv\Scripts\python so tests, runner and plots use one interpreter.
- Re-run all experiments after the tag instead of keeping the early run.

## 2026-10-29

## What I did
- Sent An Loc a status report.
- Drafted my predictions with Claude. Both of us had seen rough pilot numbers, so the draft says so and every reason is derived from the algorithms.

## 2026-10-31 / 11-01

## What I did
- Mapped my draft onto An Loc's P1 to P9c headings and listed the differences (P4, P6, P9c).
- Filled the "Differences with Trung's draft" section, committed (3ae1dd7) and pushed the tag `predictions-locked`. The tag was not on GitHub at first because only the commit had been pushed; `git push --tags` fixed it.

## Decisions
- Lock An Loc's predictions and record mine as "noted, not adopted", because mine were written after seeing pilot numbers.

## 2026-11-01

## What I did
- Ran e1 to e6 after the tag and pushed the results (4f701e8).
- That run was not valid: the same configuration (random, n = 10^5, k = n/2) took 64 ms for median of medians in E1 but 154 ms in E4 and 161 ms in E5. The CPU slowed down during the run, probably Windows power saving after the screen turned off.
- Re-ran everything with Power mode set to Best performance, plugged in, screen on, no other programs: 1,553 s (3cc528c). The same configuration now agrees within 4% for median of medians and `sorted()`, and the comparison counts are identical in both runs.
- Set `git config user.name "Thanh Trung Le"`. Earlier commits show as "Taki".

## Bugs
- The slowed-down run, caught by comparing an identical configuration across experiments.

## Decisions
- Keep the bad run's commit in the history and explain it in the methodology.

## 2026-11-02

## What I did
- Pushed the report skeleton with all 8 sections, the median-of-medians part of Section 1 and Section 3 drafted with Claude (4040d51).

## 2026-11-03

## What I did
- Read An Loc's status. Added my rows to `notes/ai-error-log.md`.
- Memory layout check (`analysis/trung_memory_layout.py`, written with Claude): same values and same comparisons, different memory layout. [Fill in the numbers from my machine.]

## Decisions
- The E5 gap between k = n/10 and 9n/10 was noise, not our counting rule (An Loc's symmetry check). The explanation Claude suggested was removed.

## What I understand now

[Write in your own words: for example why the median of medians pivot discards about 3n/10 on each side, why g = 3 loses linearity, and why time per element is not just comparisons per element.]