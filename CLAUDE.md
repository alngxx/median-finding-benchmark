# Median Finding Benchmark
Group algorithm comparison for UTS 41052 Advanced Algorithms (Spring 2026),
Programming Assignment 2. Problem: selection (return the k-th smallest value
of an unsorted list). We compare randomized quickselect with deterministic
median of medians in pure Python, on running time and comparison counts.
Two people. Each is primary author of one algorithm and is graded on their
own code, so every file has one named author.

## Stack
- Python 3.10 or newer (the code uses `X | None` type hints)
- Pure Python for the algorithms: no NumPy, no `sorted()` or `list.sort()` inside them
- Tests: pytest
- Results and plots only: pandas, matplotlib
- No database, no server, no deployment

## Structure
```
selection/quickselect.py        ← randomized, iterative, 3-way partition (An Loc Nguyen)
selection/median_of_medians.py  ← deterministic, groups of g, default 5 (Thanh Trung Le)
selection/baseline.py           ← sorted(a)[k], reference only, not a graded algorithm

bench/generators.py             ← seeded input families, ints and strings (An Loc Nguyen)
bench/counting.py               ← Counted wrapper, count_comparisons (An Loc Nguyen)
bench/adversary.py              ← unimplemented placeholder, E7 (adversary) was dropped
bench/run_bench.py              ← experiments E1 to E6, writes results/*.csv (Thanh Trung Le)
bench/plot.py                   ← figures/*.png from results/*.csv (Thanh Trung Le)

tests/                          ← test_contract.py (all three select functions),
                                  test_quickselect.py, test_median_of_medians.py,
                                  test_generators_counting.py (generators and Counted),
                                  test_bench_smoke.py (run_bench and plot)
analysis/                       ← per-person scripts that print numbers from results/
report/predictions.md           ← locked with a git tag before any experiment
results/  figures/              ← generated files, committed
notes/anloc.md, notes/trung.md  ← one entry per working session
notes/ai-error-log.md           ← every AI mistake, same day
```

## Rules
- Shared contract for both algorithms:
  `select(a: list, k: int, rng: random.Random | None = None) -> value`
- k is 0-indexed. Raise `ValueError` if the list is empty or k is out of range
- An algorithm may modify `a`. The harness passes a fresh copy outside the timed region
- Compare elements ONLY with `<` and `==`. Never use `>`, `<=`, `>=`, `!=`,
  `min()`, `max()` or key functions on elements. The `Counted` wrapper counts
  comparisons through `__lt__` and `__eq__` and raises on anything else
- Handle duplicates with a 3-way partition (less, equal, greater)
- No deep recursion. Quickselect must be iterative (Python's limit is 1000)
- Use `random.Random(seed)` for all randomness. Never the global random state.
  Every experiment takes explicit seeds
- Each file has one primary author named in its module docstring. Only edit
  the files the prompt names. Never edit the other person's module. If you
  find a bug there, report it and do not fix it
- `report/predictions.md` must not change after the git tag `predictions-locked`
- Files in `results/` come from `bench/run_bench.py` only. Never edit them by hand.
  Every number in the report must come from a CSV
- Never state a number or claim as fact without a source in the repo or a
  verified citation. Write "not verified" instead
- Write code as a competent Year 3 CS student: correct logic, practical
  variable names, no over-engineering
- Comments are minimal. Exception: each algorithm module gets one clear comment
  on its invariant (the partition step, or why the pivot discards a constant
  fraction). The video deep dive and the reflection depend on it
- Always generate code with spaces around every "=" (e.g., `x = 5`, not `x=5`),
  including keyword arguments and default values (e.g., `d = 10`)
- Never use the long dash in any file. Use the normal dash "-"
- For any writing (README, report text, docstrings longer than one line), use
  the /writing-clearly-and-concisely skill
- Never run `git add`, `git commit`, `git push`, `git tag` or any other git
  command that changes state. The user runs all git commands. `git status`,
  `git diff` and `git log` are fine
- If you get something wrong and the user corrects you, tell the user to log it
  in `notes/ai-error-log.md`

## Commands
- Install: `pip install -r requirements.txt`
- Run tests: `pytest`
- Quick benchmark check: `python -m bench.run_bench e1 --quick`
- Full experiment: `python -m bench.run_bench e1` (also e2 to e6, or `all`). E7 was dropped
- Make plots: `python -m bench.plot`


# Andrej Karpathy's guidelines
Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think before coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity first

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-driven execution

**Define success criteria upfront, then run.**

Transform tasks into verifiable goals stated before you start:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan up front:
[Step] → success: [check]
[Step] → success: [check]
[Step] → success: [check]

Once success criteria are stated, run to completion against them. Don't add
extra self-review passes or re-verification steps beyond what the stated
criteria require - a stated test suite passing is the verification; no need
to double-check it again afterward.

**Exception:** for numbered/plan-mode tasks specifically, the prompt may ask
for a single adversarial-review-subagent pass at the end, checking the diff
against the approved plan (requirements implemented, edge cases tested,
nothing out-of-scope changed). This is not the same agent re-checking its
own already-stated criteria - it's an independent reviewer catching plan
drift the stated criteria didn't cover. It does not apply to small/routine
fixes; on those, this rule's default (no extra passes) still holds.

## 5. Reporting back

**Match report length to what changed, skip narrating routine steps**

- First line answers "what happened" - did it work, what changed. Detail after.
- Skip narrating routine steps ("now I'll check the imports..."). Report findings,
  not process.
- For a small/surgical change, a few lines is enough. Don't pad with restated
  context or a summary of what was already discussed in the prompt.
- Flag real uncertainties or tradeoffs found during work - don't flag things
  already covered by the stated plan.

## 6. Scope discipline

**Deliver what was asked, at the scope intended.**

- Make routine judgment calls yourself; check in only when different readings
  of the request would lead to materially different work.
- If the request seems mistaken or a better approach exists, say so in a
  sentence and continue with the task as asked, rather than quietly widening,
  narrowing, or transforming it.
- Finish the whole task. Stop short of actions clearly beyond what was asked.
