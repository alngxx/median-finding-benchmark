"""Quickselect numbers for E3 and E5, regenerated from results/e3.csv and results/e5.csv.

Author: An Loc Nguyen

Run from the repo root: python -m analysis.anloc_numbers
Writes analysis/anloc_numbers.md. The last table counts "<" and "==" separately by rerunning
the E5 quickselect counting runs (same instance seeds, same rng seeds) with a local wrapper.
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

OUT = ROOT / "analysis" / "anloc_numbers.md"


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


def e3_section(d):
    q = d[d["algorithm"] == "quickselect"]
    c = q["comparisons"].astype(float)
    n = int(q["n"].iloc[0])
    k = int(q["k"].iloc[0])
    mom = d[d["algorithm"] == "median_of_medians"]["comparisons"].astype(float)
    mom_count = float(mom.iloc[0])
    stats = [
        ("mean", c.mean()),
        ("median", c.median()),
        ("standard deviation (n - 1)", c.std()),
        ("95th percentile", c.quantile(0.95)),
        ("99th percentile", c.quantile(0.99)),
        ("minimum", c.min()),
        ("maximum", c.max()),
    ]
    rows = [(name, sig3(v), sig3(v / n)) for name, v in stats]
    fewer = int((c < mom_count).sum())
    parts = [
        f"## E3: quickselect comparisons over {len(c)} rng seeds (n = {n}, k = {k}, one instance)",
        table(["statistic", "comparisons", "comparisons / n"], rows),
        table(["quantity", "value"], [
            ("max / mean", sig3(c.max() / c.mean())),
            ("median of medians, single run", f"{sig3(mom_count)} ({sig3(mom_count / n)} n)"),
            ("seeds where quickselect used fewer comparisons than median of medians", f"{fewer} of {len(c)}"),
        ]),
    ]
    return "\n\n".join(parts)


def e5_section(d):
    d = d.copy()
    d["rep"] = d["rep"].astype(str)
    n = int(d["n"].iloc[0])
    ks = sorted(d["k"].unique())
    summary = {}
    rows = []
    for algo in ["quickselect", "median_of_medians"]:
        for k in ks:
            sub = d[(d["algorithm"] == algo) & (d["k"] == k)]
            counts = sub[sub["rep"] == "count"].set_index("instance_seed")["comparisons"].astype(float) / n
            ms = sub[sub["rep"] != "count"]["seconds"].astype(float) * 1000
            summary[(algo, k)] = (counts.median(), ms.median())
            rows.append((
                algo, k,
                sig3(counts.median()), sig3(counts.min()), sig3(counts.max()),
                sig3(ms.median()), sig3(ms.min()), sig3(ms.max()),
            ))
    header = ["algorithm", "k", "comparisons / n (median)", "min", "max",
              "time ms (median)", "min", "max"]
    reps = len(d[(d["algorithm"] == "quickselect") & (d["k"] == ks[0]) & (d["rep"] != "count")])
    mom_counts = [summary[("median_of_medians", k)][0] for k in ks]
    mom_times = [summary[("median_of_medians", k)][1] for k in ks]
    rel_counts = (max(mom_counts) - min(mom_counts)) / min(mom_counts)
    rel_times = (max(mom_times) - min(mom_times)) / min(mom_times)
    parts = [
        f"## E5: position of k (n = {n}, {d['instance_seed'].nunique()} instances). Comparisons: median, min and max over instances. "
        f"Time: median, min and max over all {reps} timed runs per row, the statistic bench/plot.py uses for its time figures.",
        table(header, rows),
        table(["median of medians, largest relative difference across the four k", "value"], [
            ("comparisons / n", f"{sig3(rel_counts * 100)}%"),
            ("time", f"{sig3(rel_times * 100)}%"),
        ]),
    ]
    return "\n\n".join(parts)


def split_section(d):
    """Rerun the E5 quickselect counting runs with separate counters. Returns (text, matched)."""
    q = d[(d["algorithm"] == "quickselect") & (d["rep"].astype(str) == "count")]
    n = int(q["n"].iloc[0])
    ks = [int(k) for k in sorted(q["k"].unique())]
    seeds = [int(seed) for seed in sorted(q["instance_seed"].unique())]
    totals = {k: [] for k in ks}
    lts = {k: [] for k in ks}
    eqs = {k: [] for k in ks}
    mismatches = []
    for seed in seeds:
        a = generators.random_perm(n, seed)
        for k in ks:
            SplitCounted.lt = 0
            SplitCounted.eq = 0
            wrapped = [SplitCounted(x) for x in a]
            quickselect.select(wrapped, k, random.Random(seed * 1000))
            lts[k].append(SplitCounted.lt)
            eqs[k].append(SplitCounted.eq)
            totals[k].append(SplitCounted.lt + SplitCounted.eq)
            row = q[(q["instance_seed"] == seed) & (q["k"] == k)]
            expected = int(row["comparisons"].iloc[0])
            if expected != SplitCounted.lt + SplitCounted.eq:
                mismatches.append((seed, k, expected, SplitCounted.lt + SplitCounted.eq))
    runs = len(seeds) * len(ks)
    matched = runs - len(mismatches)
    check = f"Totals matched results/e5.csv in {matched} of {runs} runs (quickselect, rng seed = instance seed * 1000)."
    if mismatches:
        lines = [table(["instance seed", "k", "csv comparisons", "rerun total"], mismatches)]
        return "\n\n".join([f"## E5: separate counts of < and ==", check] + lines), False
    rows = []
    for k in ks:
        lt = sum(lts[k]) / len(seeds) / n
        eq = sum(eqs[k]) / len(seeds) / n
        rows.append((k, sig3(lt), sig3(eq), sig3(lt + eq)))
    text = "\n\n".join([
        f"## E5: quickselect, mean count per element of < and == (n = {n}, {len(seeds)} instances)",
        check,
        table(["k", "< per element", "== per element", "total per element"], rows),
    ])
    return text, True


def main():
    e3 = pd.read_csv(ROOT / "results" / "e3.csv")
    e5 = pd.read_csv(ROOT / "results" / "e5.csv")
    split_text, ok = split_section(e5)
    sections = [e3_section(e3), e5_section(e5), split_text]
    header = (
        "# An Loc's numbers\n\n"
        "Reproduce from the repo root with: `python -m analysis.anloc_numbers`\n\n"
        "Source: results/e3.csv and results/e5.csv. Values are rounded to 3 significant figures."
    )
    text = header + "\n\n" + "\n\n".join(sections) + "\n"
    OUT.write_text(text)
    print(text)
    if not ok:
        sys.exit("MISMATCH between the rerun counts and results/e5.csv. Stop before interpreting.")


if __name__ == "__main__":
    main()
