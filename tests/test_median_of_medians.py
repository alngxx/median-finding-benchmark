"""Tests for selection/median_of_medians.py."""

import inspect
import random
import sys

import pytest

from bench.counting import count_comparisons
from bench.generators import (
    all_equal,
    few_distinct,
    organ_pipe,
    random_perm,
    reverse_sorted,
    shared_prefix_strings,
    sorted_list,
)
from selection import median_of_medians
from selection.median_of_medians import BASE_CUTOFF, select

GROUP_SIZES = [3, 5, 7, 9]


@pytest.fixture(params = GROUP_SIZES, ids = [f"g{g}" for g in GROUP_SIZES])
def group_size(request):
    return request.param


def test_random_lists(group_size):
    rng = random.Random(2026)
    for _ in range(500):
        n = rng.randint(1, 2000)
        a = [rng.randint(-500, 500) for _ in range(n)]
        k = rng.randrange(n)
        assert select(list(a), k, group_size = group_size) == sorted(a)[k]


def test_every_k_on_small_lists(group_size):
    rng = random.Random(7)
    for n in range(1, 60):
        a = [rng.randint(0, 10) for _ in range(n)]
        expected = sorted(a)
        for k in range(n):
            assert select(list(a), k, group_size = group_size) == expected[k]


@pytest.mark.parametrize("n", [BASE_CUTOFF - 1, BASE_CUTOFF, BASE_CUTOFF + 1, 2 * BASE_CUTOFF + 1])
def test_sizes_around_base_cutoff(group_size, n):
    a = random_perm(n, 3)
    for k in (0, n // 2, n - 1):
        assert select(list(a), k, group_size = group_size) == k


EDGE_LISTS = {
    "single": [7],
    "all_equal": [5] * 200,
    "two_distinct": [0, 1] * 100,
    "sorted": list(range(300)),
    "reverse_sorted": list(range(300, 0, -1)),
    "negatives": [-3, 4, -10, 0, 2, -3, 8, -1] * 10,
    "floats": [0.5, -1.25, 3.0, 2.75, 0.0, 1e-9, -1e9, 2.75] * 10,
    "strings": ["pear", "apple", "fig", "kiwi", "apple", "banana"] * 10,
}


@pytest.mark.parametrize("name", list(EDGE_LISTS))
def test_edge_lists(group_size, name):
    a = EDGE_LISTS[name]
    expected = sorted(a)
    for k in (0, len(a) // 2, len(a) - 1):
        assert select(list(a), k, group_size = group_size) == expected[k]


FAMILIES = [random_perm, sorted_list, reverse_sorted, all_equal, few_distinct, organ_pipe]


@pytest.mark.parametrize("family", FAMILIES, ids = [f.__name__ for f in FAMILIES])
def test_input_families(family):
    a = family(5001, 1)
    expected = sorted(a)
    for k in (0, 2500, 5000):
        assert select(list(a), k) == expected[k]


@pytest.mark.parametrize("prefix_len", [0, 20, 100])
def test_shared_prefix_strings(prefix_len):
    a = shared_prefix_strings(2000, 1, prefix_len = prefix_len)
    assert select(list(a), 1000) == sorted(a)[1000]


@pytest.mark.parametrize(
    "a, k",
    [([], 0), ([1, 2, 3], -1), ([1, 2, 3], 3)],
    ids = ["empty", "k_negative", "k_equals_n"],
)
def test_value_error_on_k(a, k):
    with pytest.raises(ValueError):
        select(a, k)


@pytest.mark.parametrize("bad_group_size", [1, 2, 4, 6, 5.0, "5", None])
def test_value_error_on_group_size(bad_group_size):
    with pytest.raises(ValueError):
        select([3, 1, 2], 1, group_size = bad_group_size)


def test_rng_is_ignored():
    a = random_perm(1000, 5)
    answers = {select(list(a), 500, random.Random(seed)) for seed in range(5)}
    assert answers == {500}
    assert select(list(a), 500, None) == 500


def test_uses_only_lt_and_eq(group_size):
    # Counted raises TypeError on <=, >, >= and !=, so this fails if any other comparison is used.
    for family in FAMILIES:
        a = family(3001, 2)
        answer, comparisons = count_comparisons(select, a, 1500, group_size = group_size)
        assert answer == sorted(a)[1500]
        assert comparisons > 0


def test_count_is_deterministic():
    a = random_perm(10000, 9)
    first = count_comparisons(select, a, 5000)
    second = count_comparisons(select, a, 5000)
    assert first == second


def test_large_input_is_linear_in_comparisons():
    small = random_perm(10000, 4)
    large = random_perm(100000, 4)
    _, c_small = count_comparisons(select, small, 5000)
    _, c_large = count_comparisons(select, large, 50000)
    # 10 times more elements should cost about 10 times more comparisons, not 10 log 10 times.
    assert c_large / c_small < 15


def test_large_input_runs_with_low_recursion_limit():
    # Only the pivot step recurses, on a list g times smaller, so 15 extra frames are enough.
    a = random_perm(200000, 6)
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(len(inspect.stack()) + 15)
    try:
        assert select(a, 100000) == 100000
    finally:
        sys.setrecursionlimit(old_limit)


@pytest.mark.parametrize("family", FAMILIES, ids = [f.__name__ for f in FAMILIES])
@pytest.mark.parametrize("g", [5, 7, 9])
def test_comparisons_stay_linear_on_every_family(family, g):
    # The worst-case guarantee: a weak pivot rule (for example the first median) still gives
    # right answers but needs far more comparisons on sorted input. Measured values are about
    # 4n to 12n for g = 5, so 30n leaves a wide margin.
    n = 20001
    a = family(n, 3)
    answer, comparisons = count_comparisons(select, a, n // 2, group_size = g)
    assert answer == sorted(a)[n // 2]
    assert comparisons < 30 * n


def test_group_size_is_passed_to_the_pivot_step(group_size, monkeypatch):
    # E4 compares group sizes, so the recursive pivot call must use the same group size.
    seen = []
    original = median_of_medians.select

    def spy(a, k, rng = None, group_size = 5):
        seen.append(group_size)
        return original(a, k, rng, group_size = group_size)

    monkeypatch.setattr(median_of_medians, "select", spy)
    a = random_perm(5000, 8)
    assert original(a, 2500, group_size = group_size) == 2500
    assert seen and set(seen) == {group_size}