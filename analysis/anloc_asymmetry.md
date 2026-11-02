# Supplementary: asymmetry in k

Supplementary, not part of the committed E5 data. It does not read results/.

Reproduce from the repo root with: `python -m analysis.anloc_asymmetry`

Setup: quickselect.select on random_perm(n, seed), n = 100000, 300 seeds (1000 to 1299), rng = random.Random(seed * 1000), the same instance and rng seed for every k. SE is the standard error of the mean (standard deviation with n - 1, divided by the square root of the number of seeds). Values are rounded to 3 significant figures.

## Mean per element by k

| k | < mean | < SE | == mean | == SE | total mean | total SE |
|---|---|---|---|---|---|---|
| 10000 | 2.66 | 0.0497 | 1.32 | 0.0201 | 3.98 | 0.0611 |
| 50000 | 3.38 | 0.0588 | 1.70 | 0.0425 | 5.07 | 0.0957 |
| 90000 | 2.77 | 0.0513 | 1.40 | 0.0451 | 4.17 | 0.0942 |

## Paired difference, k = 90000 minus k = 10000

| count | mean difference | SE |
|---|---|---|
| < per element | 0.111 | 0.0815 |
| == per element | 0.0796 | 0.0434 |
| total per element | 0.190 | 0.123 |

## Mean < per element, side by side

| k | < mean | < SE |
|---|---|---|
| 10000 | 2.66 | 0.0497 |
| 90000 | 2.77 | 0.0513 |
