# Exact symmetry of quickselect's expected cost in k

Reproduce from the repo root with: `python -m analysis.anloc_symmetry`

Does not read results/. Standard library only.

## Table 1: E(m, k) == E(m, m - 1 - k) for m = 1 to 60

Checks the exact recurrence for the expected comparisons of quickselect on distinct elements (cost 2m - r per round, fractions.Fraction).

| quantity | value |
|---|---|
| (m, k) pairs checked | 1830 |
| pairs where E(m, k) != E(m, m - 1 - k) | 0 |

## Table 2: exact E(60, k)

Shows the exact values for five k.

| k | E as a fraction | E as a float |
|---|---|---|
| 0 | 566325637506509751237741089/3230237388259077233637600 | 175.320130 |
| 6 | 41627007355524977161987951/190013964015239837272800 | 219.073412 |
| 30 | 158041099792717558415716261/570041892045719511818400 | 277.244711 |
| 53 | 41627007355524977161987951/190013964015239837272800 | 219.073412 |
| 59 | 566325637506509751237741089/3230237388259077233637600 | 175.320130 |

## Table 3: cost model against selection.quickselect.select, n = 12

Compares the mean of `<` plus `==` calls over 20000 seeds (shuffle seed s, rng seed s * 1000 + 7, s = 0 to 19999) with the exact E(12, k). SE is the standard deviation (n - 1) divided by the square root of the number of seeds.

| k | mean count | SE | exact E | difference (SE) |
|---|---|---|---|---|
| 0 | 32.9176 | 0.0497 | 32.8968 | +0.42 |
| 1 | 37.3061 | 0.0751 | 37.2898 | +0.22 |
| 2 | 40.6536 | 0.0882 | 40.6070 | +0.53 |
| 3 | 42.9726 | 0.0970 | 42.9939 | -0.22 |
| 4 | 44.5108 | 0.1030 | 44.5419 | -0.30 |
| 5 | 45.2778 | 0.1080 | 45.3038 | -0.24 |
| 6 | 45.2831 | 0.1112 | 45.3038 | -0.19 |
| 7 | 44.6605 | 0.1138 | 44.5419 | +1.04 |
| 8 | 43.0737 | 0.1161 | 42.9939 | +0.69 |
| 9 | 40.6362 | 0.1171 | 40.6070 | +0.25 |
| 10 | 37.2274 | 0.1152 | 37.2898 | -0.54 |
| 11 | 32.8743 | 0.1079 | 32.8968 | -0.21 |

| quantity | value |
|---|---|
| largest absolute difference (SE) | 1.04 |
| limit | 4 |
| model matches the code | yes |
