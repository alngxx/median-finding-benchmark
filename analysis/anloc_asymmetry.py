"""Supplementary test: is quickselect's cost asymmetric in k because of our counting rule?

Author: An Loc Nguyen

Run from the repo root: python -m analysis.anloc_asymmetry
Writes analysis/anloc_asymmetry.md. Supplementary, not part of the committed E5 data: it does
not read results/ and uses its own instance seeds (1000 to 1299, E5 used 0 to 9).
"""

import math
import random
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from bench import generators
from selection import quickselect

OUT = ROOT / "analysis" / "anloc_asymmetry.md"
N = 100000
KS = [N // 10, N // 2, 9 * N // 10]
SEEDS = range(1000, 1300)


class SplitCounted:
    """Counts "<" and "==" calls separately in class-level counters."""

    lt = 0
    eq = 0

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        SplitCounted.lt += 1
        return self.value < other.value

    def __eq__(self, other):
        SplitCounted.eq += 1
        return self.value == other.value

    def __le__(self, other):
        raise TypeError("only < and == are allowed")

    def __gt__(self, other):
        raise TypeError("only < and == are allowed")

    def __ge__(self, other):
        raise TypeError("only < and == are allowed")

    def __ne__(self, other):
        raise TypeError("only < and == are allowed")


def sig3(x):
    """Round to 3 significant figures."""
    if x == 0:
        return "0"
    r = float(f"{x:.3g}")
    if abs(r) >= 1000:
        return f"{r:,.0f}"
    decimals = max(0, 2 - math.floor(math.log10(abs(r))))
    return f"{r:.{decimals}f}"


def table(header, rows):
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def mean_and_se(values):
    s = pd.Series(values, dtype = float)
    return s.mean(), s.std() / math.sqrt(len(s))


def run():
    """Returns {k: DataFrame with one row per seed and columns lt, eq, total (per element)}."""
    rows = {k: [] for k in KS}
    for i, seed in enumerate(SEEDS):
        a = generators.random_perm(N, seed)
        for k in KS:
            SplitCounted.lt = 0
            SplitCounted.eq = 0
            wrapped = [SplitCounted(x) for x in a]
            quickselect.select(wrapped, k, random.Random(seed * 1000))
            rows[k].append({
                "lt": SplitCounted.lt / N,
                "eq": SplitCounted.eq / N,
                "total": (SplitCounted.lt + SplitCounted.eq) / N,
            })
        if (i + 1) % 50 == 0:
            print(f"{i + 1} of {len(SEEDS)} seeds done", flush = True)
    return {k: pd.DataFrame(r) for k, r in rows.items()}


def main():
    data = run()
    seeds = len(SEEDS)
    first, last = KS[0], KS[-1]

    per_k = []
    for k in KS:
        row = [k]
        for col in ["lt", "eq", "total"]:
            m, se = mean_and_se(data[k][col])
            row += [sig3(m), sig3(se)]
        per_k.append(row)

    paired = []
    for col, name in [("lt", "< per element"), ("eq", "== per element"), ("total", "total per element")]:
        diff = data[last][col] - data[first][col]
        m, se = mean_and_se(diff)
        paired.append((name, sig3(m), sig3(se)))

    side = []
    for k in (first, last):
        m, se = mean_and_se(data[k]["lt"])
        side.append((k, sig3(m), sig3(se)))

    sections = [
        "# Supplementary: asymmetry in k\n\n"
        "Supplementary, not part of the committed E5 data. It does not read results/.\n\n"
        "Reproduce from the repo root with: `python -m analysis.anloc_asymmetry`\n\n"
        f"Setup: quickselect.select on random_perm(n, seed), n = {N}, {seeds} seeds "
        f"({SEEDS[0]} to {SEEDS[-1]}), rng = random.Random(seed * 1000), the same instance and rng seed "
        "for every k. SE is the standard error of the mean (standard deviation with n - 1, divided by "
        "the square root of the number of seeds). Values are rounded to 3 significant figures.",
        "## Mean per element by k\n\n" + table(
            ["k", "< mean", "< SE", "== mean", "== SE", "total mean", "total SE"], per_k),
        f"## Paired difference, k = {last} minus k = {first}\n\n" + table(
            ["count", "mean difference", "SE"], paired),
        "## Mean < per element, side by side\n\n" + table(["k", "< mean", "< SE"], side),
    ]
    text = "\n\n".join(sections) + "\n"
    OUT.write_text(text)
    print(text)


if __name__ == "__main__":
    main()
