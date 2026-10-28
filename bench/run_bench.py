"""Experiment runner. Writes results/<experiment>.csv.

Primary author: Thanh Trung Le

Experiments:
    E1: scaling. Random permutations, k = n // 2, 10 log-spaced sizes from 10^3 to 10^6,
        10 instances per size. Quickselect, median of medians (g = 5), baseline.
    E2: input families at n = 10^5 for the same three algorithms. Part "e2_dup" compares
        quickselect.select with quickselect.select_two_way at n = 10^4, because the 2-way
        partition is quadratic on all equal input (about 3.75 * 10^9 comparisons at n = 10^5).
    E3: quickselect tail. One random instance, n = 10^5, rng seeds 0 to 999, comparisons only.
    E4: median of medians with group size 3, 5, 7, 9 over the E1 sizes.
    E5: k = 0, n // 10, n // 2, 9 * n // 10 at n = 10^5.
    E6: strings with a shared prefix of 0, 20 and 100 characters, k = n // 2, the E1 sizes up
        to 10^5 and 5 instances per size (10^6 strings times 3 prefixes is too slow).
    E7: McIlroy-style adversary (bench/adversary.py). Not implemented.

Measurement rules:
    - Inputs are generated and copied outside the timed region.
    - One untimed warm-up run per configuration.
    - 5 timed runs with time.perf_counter, garbage collector off. Every run is stored.
    - Comparison counts come from a separate untimed run through count_comparisons.
    - Every answer is checked against sorted(a)[k], and quickselect and median of medians
      must return the same value on every instance. A mismatch aborts the run.

Columns of every results/<experiment>.csv:
    experiment, algorithm, group_size, family, n, k, instance_seed, rng_seed,
    rep, seconds, comparisons, prefix_len
Timing rows have rep = 0 to 4 and an empty comparisons field.
Counting rows have rep = "count" and an empty seconds field.

Usage:
    python -m bench.run_bench e1             one experiment
    python -m bench.run_bench e1 e2 e3       several
    python -m bench.run_bench all            e1 to e6
    python -m bench.run_bench all --quick    tiny sizes, writes to results/quick/
    python -m bench.run_bench e1 --max-n 300000
"""

import argparse
import csv
import gc
import os
import platform
import random
import subprocess
import sys
import time
from pathlib import Path

from bench import generators
from bench.counting import count_comparisons
from selection import baseline, median_of_medians, quickselect

ROOT = Path(__file__).resolve().parent.parent

COLUMNS = [
    "experiment", "algorithm", "group_size", "family", "n", "k", "instance_seed",
    "rng_seed", "rep", "seconds", "comparisons", "prefix_len",
]

FAMILIES = {
    "random": generators.random_perm,
    "sorted": generators.sorted_list,
    "reverse": generators.reverse_sorted,
    "all_equal": generators.all_equal,
    "few_distinct": generators.few_distinct,
    "organ_pipe": generators.organ_pipe,
}

E1_SIZES = [1000, 2154, 4642, 10000, 21544, 46416, 100000, 215443, 464159, 1000000]

FULL = {
    "sizes": E1_SIZES,
    "instances": 10,
    "reps": 5,
    "e2_n": 100000,
    "dup_n": 10000,
    "e3_n": 100000,
    "e3_runs": 1000,
    "e5_n": 100000,
    "e6_max_n": 100000,
    "e6_instances": 5,
    "out": ROOT / "results",
}

QUICK = {
    "sizes": [100, 316, 1000],
    "instances": 2,
    "reps": 2,
    "e2_n": 1000,
    "dup_n": 300,
    "e3_n": 1000,
    "e3_runs": 20,
    "e5_n": 1000,
    "e6_max_n": 1000,
    "e6_instances": 2,
    "out": ROOT / "results" / "quick",
}

PREFIX_LENGTHS = [0, 20, 100]
GROUP_SIZES = [3, 5, 7, 9]


# Each algorithm is (name, function, group_size). group_size is None for the non-MoM ones.
def mom(g):
    return ("median_of_medians", median_of_medians.select, g)


QUICKSELECT = ("quickselect", quickselect.select, None)
TWO_WAY = ("quickselect_two_way", quickselect.select_two_way, None)
BASELINE = ("baseline_sorted", baseline.select, None)
MAIN = [QUICKSELECT, mom(5), BASELINE]


class Writer:
    def __init__(self, path):
        path.parent.mkdir(parents = True, exist_ok = True)
        self.path = path
        self.file = open(path, "w", newline = "")
        self.csv = csv.DictWriter(self.file, fieldnames = COLUMNS)
        self.csv.writeheader()

    def row(self, **values):
        self.csv.writerow({c: values.get(c, "") for c in COLUMNS})

    def close(self):
        self.file.close()


def call(fn, a, k, rng, g):
    if g is None:
        return fn(a, k, rng)
    return fn(a, k, rng, group_size = g)


def check(answer, expected, where):
    if not answer == expected:
        sys.exit(f"WRONG ANSWER in {where}: got {answer!r}, expected {expected!r}")


def check_agree(answers, where):
    if "quickselect" in answers and "median_of_medians" in answers:
        if not answers["quickselect"] == answers["median_of_medians"]:
            sys.exit(f"quickselect and median_of_medians disagree in {where}: {answers}")


def measure(out, s, experiment, algo, family, a, k, seed, expected, prefix_len = ""):
    """Warm-up, s["reps"] timed runs, then one counting run. Returns the answer."""
    name, fn, g = algo
    base = {
        "experiment": experiment, "algorithm": name, "group_size": g if g else "",
        "family": family, "n": len(a), "k": k, "instance_seed": seed, "prefix_len": prefix_len,
    }
    where = f"{experiment} {name} g={g} {family} n={len(a)} k={k} seed={seed} prefix={prefix_len}"

    call(fn, list(a), k, random.Random(seed * 1000 + 999), g)

    answer = None
    for rep in range(s["reps"]):
        rng_seed = seed * 1000 + rep
        b = list(a)
        rng = random.Random(rng_seed)
        gc.disable()
        try:
            start = time.perf_counter()
            answer = call(fn, b, k, rng, g)
            seconds = time.perf_counter() - start
        finally:
            gc.enable()
        check(answer, expected, where)
        out.row(**base, rng_seed = rng_seed, rep = rep, seconds = f"{seconds:.9f}")

    rng_seed = seed * 1000
    if g is None:
        counted, comparisons = count_comparisons(fn, a, k, rng = random.Random(rng_seed))
    else:
        counted, comparisons = count_comparisons(fn, a, k, rng = random.Random(rng_seed), group_size = g)
    check(counted, expected, where + " (counting run)")
    out.row(**base, rng_seed = rng_seed, rep = "count", comparisons = comparisons)
    return answer


def run_algorithms(out, s, experiment, algos, family, a, k, seed, prefix_len = ""):
    expected = sorted(a)[k]
    answers = {}
    for algo in algos:
        answers[algo[0]] = measure(out, s, experiment, algo, family, a, k, seed, expected, prefix_len)
    check_agree(answers, f"{experiment} {family} n={len(a)} k={k} seed={seed}")


def e1(s, out):
    for n in s["sizes"]:
        for seed in range(s["instances"]):
            a = generators.random_perm(n, seed)
            run_algorithms(out, s, "e1", MAIN, "random", a, n // 2, seed)
        log(f"e1 n = {n} done")


def e2(s, out):
    for family, make in FAMILIES.items():
        for seed in range(s["instances"]):
            a = make(s["e2_n"], seed)
            run_algorithms(out, s, "e2", MAIN, family, a, len(a) // 2, seed)
        log(f"e2 {family} done")
    for family, make in FAMILIES.items():
        for seed in range(s["instances"]):
            a = make(s["dup_n"], seed)
            run_algorithms(out, s, "e2_dup", [QUICKSELECT, TWO_WAY], family, a, len(a) // 2, seed)
        log(f"e2_dup {family} done")


def e3(s, out):
    seed = 0
    a = generators.random_perm(s["e3_n"], seed)
    k = len(a) // 2
    expected = sorted(a)[k]
    base = {"experiment": "e3", "family": "random", "n": len(a), "k": k, "instance_seed": seed, "rep": "count"}
    for rng_seed in range(s["e3_runs"]):
        answer, comparisons = count_comparisons(quickselect.select, a, k, rng = random.Random(rng_seed))
        check(answer, expected, f"e3 rng_seed={rng_seed}")
        out.row(**base, algorithm = "quickselect", rng_seed = rng_seed, comparisons = comparisons)
        if (rng_seed + 1) % 100 == 0:
            log(f"e3 {rng_seed + 1} of {s['e3_runs']} seeds")
    answer, comparisons = count_comparisons(median_of_medians.select, a, k)
    check(answer, expected, "e3 median_of_medians")
    out.row(**base, algorithm = "median_of_medians", group_size = 5, comparisons = comparisons)
    answer, comparisons = count_comparisons(baseline.select, a, k)
    check(answer, expected, "e3 baseline")
    out.row(**base, algorithm = "baseline_sorted", comparisons = comparisons)


def e4(s, out):
    for n in s["sizes"]:
        for seed in range(s["instances"]):
            a = generators.random_perm(n, seed)
            run_algorithms(out, s, "e4", [mom(g) for g in GROUP_SIZES], "random", a, n // 2, seed)
        log(f"e4 n = {n} done")


def e5(s, out):
    n = s["e5_n"]
    for seed in range(s["instances"]):
        a = generators.random_perm(n, seed)
        for k in [0, n // 10, n // 2, 9 * n // 10]:
            run_algorithms(out, s, "e5", MAIN, "random", a, k, seed)
        log(f"e5 instance {seed} done")


def e6(s, out):
    sizes = [n for n in s["sizes"] if n <= s["e6_max_n"]]
    for prefix_len in PREFIX_LENGTHS:
        for n in sizes:
            for seed in range(s["e6_instances"]):
                a = generators.shared_prefix_strings(n, seed, prefix_len = prefix_len)
                run_algorithms(out, s, "e6", MAIN, "strings", a, n // 2, seed, prefix_len)
        log(f"e6 prefix {prefix_len} done")


EXPERIMENTS = {"e1": e1, "e2": e2, "e3": e3, "e4": e4, "e5": e5, "e6": e6, "e7": None}

START = time.perf_counter()


def log(message):
    print(f"[{time.perf_counter() - START:7.1f} s] {message}", file = sys.stderr, flush = True)


def cpu_name():
    if sys.platform.startswith("linux"):
        try:
            for line in open("/proc/cpuinfo"):
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
        except OSError:
            pass
    if sys.platform == "darwin":
        try:
            return subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"], text = True).strip()
        except (OSError, subprocess.SubprocessError):
            pass
    return platform.processor() or "unknown"


def write_environment(s, names):
    s["out"].mkdir(parents = True, exist_ok = True)
    settings = {key: value for key, value in s.items() if key != "out"}
    lines = [
        f"experiments: {' '.join(names)}",
        f"python: {platform.python_implementation()} {platform.python_version()}",
        f"os: {platform.platform()}",
        f"cpu: {cpu_name()}",
        f"logical cpus: {os.cpu_count()}",
        f"median_of_medians.BASE_CUTOFF: {median_of_medians.BASE_CUTOFF}",
        f"settings: {settings}",
    ]
    (s["out"] / "environment.txt").write_text("\n".join(lines) + "\n")


def main(argv = None):
    parser = argparse.ArgumentParser(description = "Run the selection experiments.")
    parser.add_argument("experiments", nargs = "+", choices = list(EXPERIMENTS) + ["all"])
    parser.add_argument("--quick", action = "store_true", help = "tiny sizes, writes to results/quick/")
    parser.add_argument("--max-n", type = int, help = "drop E1, E4 and E6 sizes above this value")
    parser.add_argument("--out", type = Path, help = "output folder (default results/ or results/quick/)")
    args = parser.parse_args(argv)

    s = dict(QUICK if args.quick else FULL)
    if args.max_n is not None:
        dropped = [n for n in s["sizes"] if n > args.max_n]
        s["sizes"] = [n for n in s["sizes"] if n <= args.max_n]
        print(f"--max-n {args.max_n}: sizes capped, dropped {dropped}. Say so in the report.", file = sys.stderr)
    if args.out is not None:
        s["out"] = args.out

    names = ["e1", "e2", "e3", "e4", "e5", "e6"] if "all" in args.experiments else list(dict.fromkeys(args.experiments))
    if "e7" in names:
        sys.exit("E7 is not implemented yet, see bench/adversary.py")
    write_environment(s, names)
    for name in names:
        log(f"starting {name}")
        out = Writer(s["out"] / f"{name}.csv")
        try:
            EXPERIMENTS[name](s, out)
        finally:
            out.close()
        log(f"wrote {out.path}")


if __name__ == "__main__":
    main()
