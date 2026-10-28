"""Makes figures/*.png from results/*.csv.

Primary author: Thanh Trung Le
First version generated with AI help (Claude), then reviewed and run by the author.

Every figure shows the spread, not only the middle value: lines have an interquartile band
and bars have interquartile error bars. A figure is skipped if its CSV does not exist.

Usage:
    python -m bench.plot            results/*.csv -> figures/*.png
    python -m bench.plot --quick    results/quick/*.csv -> figures/quick/*.png
"""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

# An algorithm keeps the same colour in every figure.
ALGOS = {
    "quickselect": ("Quickselect (random pivot)", "#2a78d6", "o"),
    "median_of_medians": ("Median of medians (g = 5)", "#eb6834", "s"),
    "baseline_sorted": ("sorted() baseline (C)", "#1baf7a", "^"),
    "quickselect_two_way": ("Quickselect, 2-way partition", "#eda100", "D"),
}
GROUPS = {3: ("g = 3", "#2a78d6", "o"), 5: ("g = 5", "#eb6834", "s"), 7: ("g = 7", "#1baf7a", "^"), 9: ("g = 9", "#6250d6", "D")}
FAMILY_ORDER = ["random", "sorted", "reverse", "all_equal", "few_distinct", "organ_pipe"]

plt.rcParams.update({
    "figure.facecolor": "#fcfcfb",
    "axes.facecolor": "#fcfcfb",
    "savefig.facecolor": "#fcfcfb",
    "axes.edgecolor": "#52514e",
    "xtick.color": "#52514e",
    "ytick.color": "#52514e",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": "#e6e5e0",
    "axes.axisbelow": True,
    "font.size": 10,
    "legend.frameon": False,
    "lines.linewidth": 1.5,
    "lines.markersize": 5,
})


def load(folder, name):
    path = folder / f"{name}.csv"
    if not path.exists():
        print(f"skip {name}: {path} not found")
        return None
    return pd.read_csv(path, dtype = {"rep": str})


def timing_rows(df):
    t = df[df["rep"] != "count"].copy()
    t["seconds"] = t["seconds"].astype(float)
    return t


def count_rows(df):
    c = df[df["rep"] == "count"].copy()
    c["comparisons"] = c["comparisons"].astype(float)
    return c


def quartiles(values):
    """Median, and the distances down to the 25th and up to the 75th percentile."""
    med = values.median()
    return med, med - values.quantile(0.25), values.quantile(0.75) - med


def save(fig, folder, name):
    folder.mkdir(parents = True, exist_ok = True)
    fig.tight_layout()
    fig.savefig(folder / f"{name}.png", dpi = 150)
    plt.close(fig)
    print(f"wrote {folder / name}.png")


def legend_right(ax):
    ax.legend(loc = "upper left", bbox_to_anchor = (1.01, 1.0))


def legend_below(ax, columns):
    ax.legend(loc = "upper center", bbox_to_anchor = (0.5, -0.12), ncol = columns)


def line_with_band(ax, x, y, style):
    """Median line with an interquartile band. x and y are aligned Series."""
    label, color, marker = style
    grouped = y.groupby(x)
    med = grouped.median()
    ax.fill_between(med.index, grouped.quantile(0.25), grouped.quantile(0.75), color = color, alpha = 0.15, linewidth = 0)
    ax.plot(med.index, med.values, color = color, marker = marker, label = label)


def grouped_bars(ax, categories, series, values_for):
    """One bar per (category, series) with interquartile error bars."""
    width = 0.8 / len(series)
    for i, key in enumerate(series):
        label, color, _ = ALGOS[key]
        xs, meds, lows, highs = [], [], [], []
        for j, cat in enumerate(categories):
            values = values_for(cat, key)
            if values.empty:
                continue
            med, low, high = quartiles(values)
            xs.append(j + (i - (len(series) - 1) / 2) * width)
            meds.append(med)
            lows.append(low)
            highs.append(high)
        ax.bar(xs, meds, width = width * 0.92, color = color, label = label,
               yerr = [lows, highs], error_kw = {"ecolor": "#52514e", "elinewidth": 1, "capsize": 2})
    ax.set_xticks(range(len(categories)))
    ax.grid(axis = "x", visible = False)


def e1_figures(df, folder):
    t = timing_rows(df)
    fig, ax = plt.subplots(figsize = (8, 4.5))
    for key, style in ALGOS.items():
        d = t[t["algorithm"] == key]
        if not d.empty:
            line_with_band(ax, d["n"], d["seconds"], style)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("n (list length)")
    ax.set_ylabel("time per call (s)")
    ax.set_title("E1: time vs n, random permutations, k = n/2 (median and IQR)")
    legend_right(ax)
    save(fig, folder, "e1_time_loglog")

    c = count_rows(df)
    fig, ax = plt.subplots(figsize = (8, 4.5))
    for key, style in ALGOS.items():
        d = c[c["algorithm"] == key]
        if not d.empty:
            line_with_band(ax, d["n"], d["comparisons"] / d["n"], style)
    ax.set_xscale("log")
    ax.set_ylim(bottom = 0)
    ax.set_xlabel("n (list length)")
    ax.set_ylabel("comparisons / n")
    ax.set_title("E1: comparisons per element vs n (median and IQR over instances)")
    legend_right(ax)
    save(fig, folder, "e1_comparisons_per_n")


def e2_figures(df, folder):
    t = timing_rows(df[df["experiment"] == "e2"])
    if not t.empty:
        algos = [a for a in ALGOS if a in set(t["algorithm"])]
        families = [f for f in FAMILY_ORDER if f in set(t["family"])]
        fig, ax = plt.subplots(figsize = (8, 4.5))
        grouped_bars(ax, families, algos, lambda f, a: t[(t["family"] == f) & (t["algorithm"] == a)]["seconds"] * 1000)
        ax.set_xticklabels([f.replace("_", " ") for f in families])
        ax.set_ylabel("time per call (ms)")
        ax.set_title(f"E2: input families, n = {int(t['n'].iloc[0]):,}, k = n/2 (median and IQR)")
        legend_below(ax, len(algos))
        save(fig, folder, "e2_families_time")

    c = count_rows(df[df["experiment"] == "e2_dup"])
    if not c.empty:
        families = [f for f in FAMILY_ORDER if f in set(c["family"])]
        fig, ax = plt.subplots(figsize = (10, 4))
        for offset, key in [(-0.12, "quickselect"), (0.12, "quickselect_two_way")]:
            label, color, marker = ALGOS[key]
            d = c[c["algorithm"] == key]
            ax.scatter(d["comparisons"], [families.index(f) + offset for f in d["family"]],
                       color = color, marker = marker, s = 30, label = label, zorder = 3)
        ax.set_yticks(range(len(families)), [f.replace("_", " ") for f in families])
        ax.set_xscale("log")
        ax.grid(axis = "y", visible = False)
        ax.set_xlabel("comparisons per call (log scale), one dot per instance")
        ax.set_title(f"E2 duplicates: 3-way vs 2-way partition, n = {int(c['n'].iloc[0]):,}")
        legend_right(ax)
        save(fig, folder, "e2_duplicates_comparisons")


def e3_figure(df, folder):
    c = count_rows(df)
    qs = c[c["algorithm"] == "quickselect"]["comparisons"]
    if qs.empty:
        return
    n = int(c["n"].iloc[0])
    fig, ax = plt.subplots(figsize = (10, 4.5))
    ax.hist(qs / n, bins = 40, color = ALGOS["quickselect"][1], edgecolor = "#fcfcfb", linewidth = 0.8)
    gray = "#52514e"
    marks = [
        ("mean", qs.mean(), gray, "--"),
        ("99th percentile", qs.quantile(0.99), gray, ":"),
        ("max", qs.max(), gray, "-."),
    ]
    mom_count = c[c["algorithm"] == "median_of_medians"]["comparisons"]
    if not mom_count.empty:
        marks.append(("median of medians (g = 5)", mom_count.iloc[0], ALGOS["median_of_medians"][1], "-"))
    for text, value, color, style in marks:
        ax.axvline(value / n, color = color, linewidth = 1.4, linestyle = style, label = f"{text}: {value / n:.2f}")
    legend_right(ax)
    ax.set_xlabel("comparisons / n")
    ax.set_ylabel(f"number of runs (of {len(qs)})")
    ax.set_title(f"E3: quickselect over {len(qs)} rng seeds, one instance, n = {n:,}")
    save(fig, folder, "e3_quickselect_tail")


def e4_figures(df, folder):
    df = df.copy()
    df["group_size"] = df["group_size"].astype(int)
    c = count_rows(df)
    t = timing_rows(df)
    fig, (left, right) = plt.subplots(1, 2, figsize = (11, 4.5))
    for g, style in GROUPS.items():
        d = c[c["group_size"] == g]
        if not d.empty:
            line_with_band(left, d["n"], d["comparisons"] / d["n"], style)
        d = t[t["group_size"] == g]
        if not d.empty:
            line_with_band(right, d["n"], d["seconds"] / d["n"] * 1e6, style)
    for ax, ylabel in [(left, "comparisons / n"), (right, "time per element (µs)")]:
        ax.set_xscale("log")
        ax.set_ylim(bottom = 0)
        ax.set_xlabel("n (list length)")
        ax.set_ylabel(ylabel)
    left.set_title("E4: comparisons per element by group size")
    right.set_title("E4: time per element by group size")
    legend_right(right)
    save(fig, folder, "e4_group_size")


def e5_figure(df, folder):
    c = count_rows(df)
    if c.empty:
        return
    n = int(c["n"].iloc[0])
    ks = sorted(c["k"].unique())
    names = {0: "k = 0", n // 10: "k = n/10", n // 2: "k = n/2", 9 * n // 10: "k = 9n/10"}
    algos = [a for a in ALGOS if a in set(c["algorithm"])]
    c["per_n"] = c["comparisons"] / c["n"]
    fig, ax = plt.subplots(figsize = (8, 4.5))
    grouped_bars(ax, ks, algos, lambda k, a: c[(c["k"] == k) & (c["algorithm"] == a)]["per_n"])
    ax.set_xticklabels([names.get(k, f"k = {k}") for k in ks])
    ax.set_ylabel("comparisons / n")
    ax.set_title(f"E5: position of k, n = {n:,} (median and IQR over instances)")
    legend_below(ax, len(algos))
    save(fig, folder, "e5_k_position")


def e6_figure(df, folder):
    df = df.copy()
    df["prefix_len"] = df["prefix_len"].astype(int)
    n = int(df["n"].max())
    df = df[df["n"] == n]
    t = timing_rows(df)
    c = count_rows(df)
    fig, (left, right) = plt.subplots(1, 2, figsize = (11, 4.5))
    for key, style in ALGOS.items():
        d = t[t["algorithm"] == key]
        if not d.empty:
            line_with_band(left, d["prefix_len"], d["seconds"] / d["n"] * 1e6, style)
        d = c[c["algorithm"] == key]
        if not d.empty:
            line_with_band(right, d["prefix_len"], d["comparisons"] / d["n"], style)
    for ax, ylabel in [(left, "time per element (µs)"), (right, "comparisons / n")]:
        ax.set_xticks(sorted(df["prefix_len"].unique()))
        ax.set_ylim(bottom = 0)
        ax.set_xlabel("shared prefix length (characters)")
        ax.set_ylabel(ylabel)
    left.set_title(f"E6: time per element, strings, n = {n:,}")
    right.set_title(f"E6: comparisons per element, strings, n = {n:,}")
    legend_right(right)
    save(fig, folder, "e6_shared_prefix")


def main(argv = None):
    parser = argparse.ArgumentParser(description = "Make figures from results/*.csv.")
    parser.add_argument("--quick", action = "store_true", help = "read results/quick/, write figures/quick/")
    parser.add_argument("--results", type = Path, help = "folder with the CSVs")
    parser.add_argument("--figures", type = Path, help = "folder for the PNGs")
    args = parser.parse_args(argv)
    results = args.results or (ROOT / "results" / "quick" if args.quick else ROOT / "results")
    figures = args.figures or (ROOT / "figures" / "quick" if args.quick else ROOT / "figures")

    makers = {"e1": e1_figures, "e2": e2_figures, "e3": e3_figure, "e4": e4_figures, "e5": e5_figure, "e6": e6_figure}
    for name, make in makers.items():
        df = load(results, name)
        if df is not None:
            make(df, figures)


if __name__ == "__main__":
    main()