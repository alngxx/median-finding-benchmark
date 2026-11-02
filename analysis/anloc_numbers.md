# An Loc's numbers

Reproduce from the repo root with: `python -m analysis.anloc_numbers`

Source: results/e3.csv and results/e5.csv. Values are rounded to 3 significant figures.

## E3: quickselect comparisons over 1000 rng seeds (n = 100000, k = 50000, one instance)

| statistic | comparisons | comparisons / n |
|---|---|---|
| mean | 505,000 | 5.05 |
| median | 487,000 | 4.87 |
| standard deviation (n - 1) | 149,000 | 1.49 |
| 95th percentile | 783,000 | 7.83 |
| 99th percentile | 899,000 | 8.99 |
| minimum | 208,000 | 2.08 |
| maximum | 986,000 | 9.86 |

| quantity | value |
|---|---|
| max / mean | 1.95 |
| median of medians, single run | 969,000 (9.69 n) |
| seeds where quickselect used fewer comparisons than median of medians | 998 of 1000 |

## E5: position of k (n = 100000, 10 instances). Comparisons: median, min and max over instances. Time: median, min and max over all 50 timed runs per row, the statistic bench/plot.py uses for its time figures.

| algorithm | k | comparisons / n (median) | min | max | time ms (median) | min | max |
|---|---|---|---|---|---|---|---|
| quickselect | 0 | 2.59 | 2.17 | 3.86 | 6.58 | 4.00 | 33.5 |
| quickselect | 10000 | 3.14 | 2.43 | 6.46 | 8.49 | 5.00 | 16.7 |
| quickselect | 50000 | 4.52 | 3.05 | 8.74 | 11.8 | 7.21 | 20.8 |
| quickselect | 90000 | 4.35 | 2.06 | 5.81 | 9.77 | 4.49 | 29.8 |
| median_of_medians | 0 | 9.90 | 9.87 | 9.95 | 63.6 | 61.0 | 72.2 |
| median_of_medians | 10000 | 9.90 | 9.88 | 9.95 | 63.6 | 60.9 | 71.5 |
| median_of_medians | 50000 | 9.91 | 9.69 | 9.96 | 63.1 | 60.6 | 67.4 |
| median_of_medians | 90000 | 9.92 | 9.78 | 9.94 | 63.0 | 61.3 | 64.8 |

| median of medians, largest relative difference across the four k | value |
|---|---|
| comparisons / n | 0.146% |
| time | 0.950% |

## E5: quickselect, mean count per element of < and == (n = 100000, 10 instances)

Totals matched results/e5.csv in 40 of 40 runs (quickselect, rng seed = instance seed * 1000).

| k | < per element | == per element | total per element |
|---|---|---|---|
| 0 | 1.79 | 1.00 | 2.79 |
| 10000 | 2.33 | 1.32 | 3.65 |
| 50000 | 3.07 | 1.72 | 4.79 |
| 90000 | 2.76 | 1.49 | 4.25 |
