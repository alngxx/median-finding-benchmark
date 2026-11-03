# Memory layout check

Reproduce from the repo root with: `python -m analysis.trung_memory_layout`

Supplementary, not part of the committed E1 data. Instance seeds 2000 to 2004, k = n // 2, 5 timed runs per instance and layout, median over all runs. Both layouts hold the same values and use the same rng seeds, so the comparison counts are identical (checked at n = 100000).

| algorithm | n | shuffled (ns per element) | in list order (ns per element) | shuffled / in order |
|---|---|---|---|---|
| quickselect | 100000 | 129 | 132 | 0.98 |
| median_of_medians | 100000 | 674 | 669 | 1.01 |
| baseline_sorted | 100000 | 119 | 119 | 1.00 |
| quickselect | 464159 | 506 | 263 | 1.92 |
| median_of_medians | 464159 | 1037 | 890 | 1.17 |
| baseline_sorted | 464159 | 279 | 215 | 1.30 |
| quickselect | 1000000 | 558 | 267 | 2.09 |
| median_of_medians | 1000000 | 1318 | 1082 | 1.22 |
| baseline_sorted | 1000000 | 356 | 285 | 1.25 |
