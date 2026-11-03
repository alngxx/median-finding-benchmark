"""Supplementary test: does memory layout, not comparison count, explain the time per element?

Author: Thanh Trung Le (written with Claude)

Run from the repo root: python -m analysis.trung_memory_layout
Writes analysis/trung_memory_layout.md. Supplementary, not part of the committed E1 data: it does
not read results/ and uses its own instance seeds (2000 to 2004, E1 used 0 to 9).

Idea: random_perm(n, seed) builds the int objects in value order (list(range(n))) and then
shuffles the list, so walking the list jumps around memory. Copying every value with x + 0
creates new int objects in list order, so walking the list reads memory in order. Both lists
hold the same values, and the same rng seed is used, so every algorithm makes exactly the same
comparisons on both. Only the memory layout differs. If time per element still differs, the
difference cannot come from the comparison count.
"""

import gc
import random
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from bench import generators
from bench.counting import count_comparisons
from selection import baseline, median_of_medians, quickselect

OUT = ROOT / "analysis" / "trung_memory_layout.md"
SIZES = [100000, 464159, 1000000]
SEEDS = range(2000, 2005)
REPS = 5
ALGORITHMS = [
    ("quickselect", quickselect.select),
    ("median_of_medians", median_of_medians.select),
    ("baseline_sorted", baseline.select),
]


def in_list_order(a):
    """Same values as a, but new int objects created in list order."""
    return [x + 0 for x in a]


def time_once(fn, a, k, rng_seed):
    b = list(a)
    rng = random.Random(rng_seed)
    gc.disable()
    try:
        start = time.perf_counter()
        answer = fn(b, k, rng)
        seconds = time.perf_counter() - start
    finally:
        gc.enable()
    return answer, seconds


def main():
    rows = []
    for n in SIZES:
        k = n // 2
        times = {(name, layout): [] for name, _ in ALGORITHMS for layout in ("shuffled", "in order")}
        for seed in SEEDS:
            shuffled = generators.random_perm(n, seed)
            ordered = in_list_order(shuffled)
            expected = sorted(shuffled)[k]
            for name, fn in ALGORITHMS:
                fn(list(shuffled), k, random.Random(seed))
                fn(list(ordered), k, random.Random(seed))
                for rep in range(REPS):
                    # Alternate the two layouts so a slow drift of the machine hits both equally.
                    for layout, a in (("shuffled", shuffled), ("in order", ordered)):
                        answer, seconds = time_once(fn, a, k, seed * 1000 + rep)
                        if not answer == expected:
                            sys.exit(f"wrong answer: {name} {layout} n={n} seed={seed}")
                        times[(name, layout)].append(seconds)
        if n == SIZES[0]:
            # Same values and same rng seed, so the comparison counts must be identical.
            for name, fn in ALGORITHMS:
                a = generators.random_perm(n, SEEDS[0])
                _, c1 = count_comparisons(fn, a, k, rng = random.Random(7))
                _, c2 = count_comparisons(fn, in_list_order(a), k, rng = random.Random(7))
                if not c1 == c2:
                    sys.exit(f"comparison counts differ for {name}: {c1} and {c2}")
        for name, _ in ALGORITHMS:
            s = statistics.median(times[(name, "shuffled")])
            o = statistics.median(times[(name, "in order")])
            rows.append((name, n, s / n * 1e9, o / n * 1e9, s / o))
        print(f"n = {n} done", file = sys.stderr)

    lines = [
        "# Memory layout check",
        "",
        "Reproduce from the repo root with: `python -m analysis.trung_memory_layout`",
        "",
        "Supplementary, not part of the committed E1 data. Instance seeds 2000 to 2004, k = n // 2, "
        f"{REPS} timed runs per instance and layout, median over all runs. Both layouts hold the same "
        "values and use the same rng seeds, so the comparison counts are identical (checked at "
        f"n = {SIZES[0]}).",
        "",
        "| algorithm | n | shuffled (ns per element) | in list order (ns per element) | shuffled / in order |",
        "|---|---|---|---|---|",
    ]
    for name, n, s, o, ratio in rows:
        lines.append(f"| {name} | {n} | {s:.0f} | {o:.0f} | {ratio:.2f} |")
    OUT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
