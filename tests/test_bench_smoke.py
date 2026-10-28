"""Smoke tests for bench/run_bench.py and bench/plot.py.

Each experiment runs with --quick into a temporary folder, so results/ is never touched.
"""

import csv

import pytest

from bench import plot, run_bench

EXPERIMENTS = ["e1", "e2", "e3", "e4", "e5", "e6"]


@pytest.fixture(scope = "module")
def quick_results(tmp_path_factory):
    folder = tmp_path_factory.mktemp("results")
    run_bench.main(EXPERIMENTS + ["--quick", "--out", str(folder)])
    return folder


def read_rows(folder, name):
    with open(folder / f"{name}.csv", newline = "") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames, list(reader)


@pytest.mark.parametrize("name", EXPERIMENTS)
def test_csv_has_columns_and_rows(quick_results, name):
    columns, rows = read_rows(quick_results, name)
    assert columns == run_bench.COLUMNS
    assert rows
    assert all(row["experiment"].startswith(name) for row in rows)


@pytest.mark.parametrize("name", ["e1", "e2", "e4", "e5", "e6"])
def test_timed_experiments_store_every_rep_and_a_count(quick_results, name):
    _, rows = read_rows(quick_results, name)
    timed = [row for row in rows if row["rep"] != "count"]
    counted = [row for row in rows if row["rep"] == "count"]
    assert timed and counted
    assert all(float(row["seconds"]) > 0 and row["comparisons"] == "" for row in timed)
    assert all(int(row["comparisons"]) > 0 and row["seconds"] == "" for row in counted)
    reps = {row["rep"] for row in timed}
    assert reps == {str(r) for r in range(run_bench.QUICK["reps"])}


def test_e2_includes_two_way_partition(quick_results):
    _, rows = read_rows(quick_results, "e2")
    dup = {row["algorithm"] for row in rows if row["experiment"] == "e2_dup"}
    assert dup == {"quickselect", "quickselect_two_way"}


def test_e3_has_one_row_per_seed(quick_results):
    _, rows = read_rows(quick_results, "e3")
    seeds = [row["rng_seed"] for row in rows if row["algorithm"] == "quickselect"]
    assert len(seeds) == run_bench.QUICK["e3_runs"]


def test_e4_covers_all_group_sizes(quick_results):
    _, rows = read_rows(quick_results, "e4")
    assert {row["group_size"] for row in rows} == {"3", "5", "7", "9"}


def test_e6_fills_prefix_len_only_in_e6(quick_results):
    _, rows = read_rows(quick_results, "e6")
    assert {row["prefix_len"] for row in rows} == {"0", "20", "100"}
    _, rows = read_rows(quick_results, "e1")
    assert all(row["prefix_len"] == "" for row in rows)


def test_environment_file(quick_results):
    text = (quick_results / "environment.txt").read_text()
    assert "python:" in text and "cpu:" in text


def test_wrong_answer_aborts(monkeypatch, tmp_path):
    monkeypatch.setitem(run_bench.QUICK, "sizes", [100])
    monkeypatch.setattr(run_bench, "MAIN", [("broken", lambda a, k, rng = None: -1, None)])
    with pytest.raises(SystemExit, match = "WRONG ANSWER"):
        run_bench.main(["e1", "--quick", "--out", str(tmp_path)])


def test_disagreement_aborts():
    with pytest.raises(SystemExit, match = "disagree"):
        run_bench.check_agree({"quickselect": 1, "median_of_medians": 2}, "test")


def test_e7_is_refused(tmp_path):
    with pytest.raises(SystemExit, match = "E7"):
        run_bench.main(["e7", "--quick", "--out", str(tmp_path)])


def test_plots_are_made(quick_results, tmp_path):
    plot.main(["--results", str(quick_results), "--figures", str(tmp_path)])
    made = {p.name for p in tmp_path.glob("*.png")}
    assert made == {
        "e1_time_loglog.png", "e1_comparisons_per_n.png", "e2_families_time.png",
        "e2_duplicates_comparisons.png", "e3_quickselect_tail.png", "e4_group_size.png",
        "e5_k_position.png", "e6_shared_prefix.png",
    }
