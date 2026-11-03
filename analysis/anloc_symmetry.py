"""Exact check that quickselect's expected cost is symmetric in k, and a check of the cost model.

Author: An Loc Nguyen

Run from the repo root: python -m analysis.anloc_symmetry
Writes analysis/anloc_symmetry.md. Does not read results/. Standard library only.

Model of one round on m distinct elements: the pivot has rank r (uniform over 0 to m - 1)
and the round costs 2m - r comparisons (one "<" per element, one "==" per element that is
not less than the pivot). If r == k the process stops. If r > k the next state is (r, k).
If r < k the next state is (m - 1 - r, k - r - 1).
"""

import math
import random
import statistics
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from selection import quickselect

OUT = ROOT / "analysis" / "anloc_symmetry.md"

MAX_M = 60
REAL_N = 12
SEEDS = range(20000)
SE_LIMIT = 4


def expected_costs(max_m):
    """E[m][k] = exact expected total comparisons starting from (m, k)."""
    E = {}
    for m in range(1, max_m + 1):
        E[m] = []
        for k in range(m):
            total = Fraction(0)
            for r in range(m):
                cost = Fraction(2 * m - r)
                if r > k:
                    cost += E[r][k]
                elif r < k:
                    cost += E[m - 1 - r][k - r - 1]
                total += cost
            E[m].append(total / m)
    return E


class CountedValue:
    """Counts "<" and "==" calls separately. Any other comparison raises."""

    lt_count = 0
    eq_count = 0

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        CountedValue.lt_count += 1
        return self.value < other.value

    def __eq__(self, other):
        CountedValue.eq_count += 1
        return self.value == other.value

    def __le__(self, other):
        raise TypeError("only < and == are allowed")

    def __gt__(self, other):
        raise TypeError("only < and == are allowed")

    def __ge__(self, other):
        raise TypeError("only < and == are allowed")

    def __ne__(self, other):
        raise TypeError("only < and == are allowed")


def real_counts(n, k, seeds):
    """Total count of "<" and "==" for each seed, running the real quickselect.select."""
    totals = []
    for seed in seeds:
        values = list(range(n))
        random.Random(seed).shuffle(values)
        wrapped = [CountedValue(v) for v in values]
        CountedValue.lt_count = 0
        CountedValue.eq_count = 0
        answer = quickselect.select(wrapped, k, random.Random(seed * 1000 + 7))
        assert answer.value == k
        totals.append(CountedValue.lt_count + CountedValue.eq_count)
    return totals


def main():
    E = expected_costs(MAX_M)

    pairs = 0
    for m in range(1, MAX_M + 1):
        for k in range(m):
            assert E[m][k] == E[m][m - 1 - k], f"asymmetric at m = {m}, k = {k}"
            pairs += 1
    print(f"Checked {pairs} (m, k) pairs, m = 1 to {MAX_M}: E(m, k) == E(m, m - 1 - k) for all.")

    ks_shown = [0, 6, 30, 53, 59]
    print(f"E({MAX_M}, k):")
    for k in ks_shown:
        print(f"  k = {k}: {E[MAX_M][k]} = {float(E[MAX_M][k]):.6f}")

    rows = []
    for k in range(REAL_N):
        totals = real_counts(REAL_N, k, SEEDS)
        mean = statistics.fmean(totals)
        se = statistics.stdev(totals) / math.sqrt(len(totals))
        exact = float(E[REAL_N][k])
        rows.append((k, mean, se, exact, (mean - exact) / se))
    largest = max(abs(r[4]) for r in rows)

    print(f"\nReal code, n = {REAL_N}, {len(SEEDS)} seeds per k:")
    for k, mean, se, exact, z in rows:
        print(f"  k = {k:2d}: mean {mean:.4f}, SE {se:.4f}, exact {exact:.4f}, difference {z:+.2f} SE")
    print(f"Largest difference: {largest:.2f} standard errors.")
    if largest > SE_LIMIT:
        print(f"WARNING: a difference is above {SE_LIMIT} standard errors. The model does not match the code. Do not conclude anything about the model.")

    lines = [
        "# Exact symmetry of quickselect's expected cost in k",
        "",
        "Reproduce from the repo root with: `python -m analysis.anloc_symmetry`",
        "",
        "Does not read results/. Standard library only.",
        "",
        f"## Table 1: E(m, k) == E(m, m - 1 - k) for m = 1 to {MAX_M}",
        "",
        "Checks the exact recurrence for the expected comparisons of quickselect on distinct elements (cost 2m - r per round, fractions.Fraction).",
        "",
        "| quantity | value |",
        "|---|---|",
        f"| (m, k) pairs checked | {pairs} |",
        "| pairs where E(m, k) != E(m, m - 1 - k) | 0 |",
        "",
        f"## Table 2: exact E({MAX_M}, k)",
        "",
        "Shows the exact values for five k.",
        "",
        "| k | E as a fraction | E as a float |",
        "|---|---|---|",
    ]
    for k in ks_shown:
        lines.append(f"| {k} | {E[MAX_M][k]} | {float(E[MAX_M][k]):.6f} |")
    lines += [
        "",
        f"## Table 3: cost model against selection.quickselect.select, n = {REAL_N}",
        "",
        f"Compares the mean of `<` plus `==` calls over {len(SEEDS)} seeds (shuffle seed s, rng seed s * 1000 + 7, s = 0 to {len(SEEDS) - 1}) with the exact E({REAL_N}, k). SE is the standard deviation (n - 1) divided by the square root of the number of seeds.",
        "",
        "| k | mean count | SE | exact E | difference (SE) |",
        "|---|---|---|---|---|",
    ]
    for k, mean, se, exact, z in rows:
        lines.append(f"| {k} | {mean:.4f} | {se:.4f} | {exact:.4f} | {z:+.2f} |")
    lines += [
        "",
        "| quantity | value |",
        "|---|---|",
        f"| largest absolute difference (SE) | {largest:.2f} |",
        f"| limit | {SE_LIMIT} |",
        f"| model matches the code | {'yes' if largest <= SE_LIMIT else 'NO'} |",
        "",
    ]
    OUT.write_text("\n".join(lines))


if __name__ == "__main__":
    main()
