# Median Finding Benchmark: Quickselect vs Median-of-medians

Group comparison of two selection algorithms for UTS 41052 Advanced Algorithms, Programming Assignment 2.

Video: https://youtu.be/vJGVU6C06bs

Selection returns the k-th smallest value of an unsorted list. We compare randomized quickselect with deterministic median of medians, both in pure Python, on running time and comparison counts.

## What is in the repo

- `selection/`: quickselect (iterative, 3-way partition, plus a 2-way version for the duplicates experiment), median of medians (group size 5 by default), and a `sorted()` baseline.
- `bench/generators.py`: seeded input families of ints and strings.
- `bench/counting.py`: the `Counted` wrapper and `count_comparisons`.
- `bench/run_bench.py`: the runner for experiments E1 to E6.
- `bench/plot.py`: figures from the result files.
- `tests/`: pytest tests for every module.
- `analysis/`: per-person scripts that print the numbers quoted in the report, each with the `.md` file it writes.
- `report/report.md`: the written report. `report/predictions.md`: the predictions, locked with the git tag `predictions-locked` before any experiment and never edited since.
- `results/` and `figures/`: generated CSV files and plots, committed. Only `bench/run_bench.py` and `bench/plot.py` write to them.
- `notes/`: one working log per member (`anloc.md`, `trung.md`), `ai-error-log.md` (every AI mistake) and `pilot-numbers-seen.md`.
- `reflections/`: one individual reflection per member.
- `slides.html`: slides for the video. The video link is above and in the header of `report/report.md`.

Experiment E7 (a McIlroy-style adversary) was dropped for lack of time. `bench/adversary.py` is an unimplemented placeholder.

## Primary authors

Each file has one primary author, named in its module docstring.

| File | Primary author |
|------|----------------|
| selection/quickselect.py | An Loc Nguyen |
| selection/median_of_medians.py | Thanh Trung Le |
| selection/baseline.py | none (reference only, not graded) |
| bench/generators.py | An Loc Nguyen |
| bench/counting.py | An Loc Nguyen |
| bench/adversary.py | none (unimplemented placeholder) |
| bench/run_bench.py | Thanh Trung Le |
| bench/plot.py | Thanh Trung Le |

## Contract

Both algorithms share one signature:

```python
select(a: list, k: int, rng: random.Random | None = None) -> value
```

- `k` is 0-indexed. `select` raises `ValueError` if the list is empty or `k` is out of range.
- `select` may modify `a`.
- Elements are compared only with `<` and `==`.

## Setup

Python 3.10 or newer. Create a virtual environment in the repo folder.

```
python -m venv .venv
```

Activate it on macOS or Linux:

```
source .venv/bin/activate
```

Activate it on Windows:

```
.venv\Scripts\activate
```

Install the requirements and run the tests:

```
pip install -r requirements.txt
pytest
```

## Run the experiments

Run one or more experiments (`e1` to `e6`), or all of them:

```
python -m bench.run_bench e1
python -m bench.run_bench e1 e2 e3
python -m bench.run_bench all
```

Options:

- `--quick`: tiny sizes for a fast check. Output goes to `results/quick/`.
- `--max-n N`: drop the E1, E4 and E6 sizes above N. State this in the report if you use it.
- `--out FOLDER`: write to FOLDER instead of `results/` (or `results/quick/` with `--quick`).

Each run writes `results/<experiment>.csv` and `results/environment.txt` (Python version, operating system, CPU and settings). Only `bench/run_bench.py` writes to `results/`. The column list and the measurement rules are in the docstring of `bench/run_bench.py`.

## Make the plots

```
python -m bench.plot
```

This reads `results/*.csv` and writes `figures/*.png`. With `--quick` it reads `results/quick/*.csv` and writes `figures/quick/*.png`. A figure is skipped if its CSV does not exist.

## Reproduce the analysis numbers

These scripts read `results/` or rerun quickselect, and each rewrites its own file in `analysis/`. Run them from the repo root. Times are from one run on a Mac with Python 3.12.

```
python -m analysis.anloc_numbers
python -m analysis.anloc_asymmetry
python -m analysis.anloc_symmetry
python -m analysis.trung_memory_layout
```

- `analysis.anloc_numbers`: the E3 and E5 numbers in the report, from `results/e3.csv` and `results/e5.csv`, plus separate counts of `<` and `==` for the E5 quickselect runs. Fast, about 4 seconds.
- `analysis.anloc_asymmetry`: the supplementary 300-seed run on quickselect's cost at three values of k. It does not read `results/`. Slow, about 80 seconds.
- `analysis.anloc_symmetry`: an exact check, with fractions, that quickselect's expected cost is the same at k and at its mirror position, and a check of the cost model against the real code on small lists. About 5 seconds.
- `analysis.trung_memory_layout`: the supplementary memory layout test in the report (Section 5.1). It does not read `results/` and uses its own instance seeds. Run time not recorded.
