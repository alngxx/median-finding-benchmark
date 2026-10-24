# PA2 Selection

Group comparison of two selection algorithms for UTS 41052 Advanced Algorithms, Programming Assignment 2.

Selection returns the k-th smallest value of an unsorted list. We compare randomized quickselect with deterministic median of medians, both in pure Python, on running time and comparison counts.

The repo holds the scaffold only. The algorithms, generators and runner are stubs.

## Primary authors

Each file has one primary author, named in its module docstring.

| File | Primary author |
|------|----------------|
| selection/quickselect.py | An Loc Nguyen |
| selection/median_of_medians.py | Thanh Trung Le |
| selection/baseline.py | none (reference only, not graded) |
| bench/generators.py | An Loc Nguyen |
| bench/counting.py | An Loc Nguyen |
| bench/adversary.py | not decided |
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

Python 3.10 or newer.

```
pip install -r requirements.txt
```

## Run the tests

```
pytest
```

A test is skipped while its function raises `NotImplementedError`.

## Run the experiments

Quick check of one experiment:

```
python -m bench.run_bench e1 --quick
```

Full run of one experiment (`e1` to `e7`):

```
python -m bench.run_bench e1
```

Each run writes `results/<experiment>.csv`. Only `bench/run_bench.py` writes to `results/`.

## Make the plots

```
python -m bench.plot
```

This reads `results/*.csv` and writes `figures/*.png`.
