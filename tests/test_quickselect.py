"""Tests for selection/quickselect.py."""

import random

import pytest

from bench.counting import Counted, count_comparisons
from bench.generators import all_equal, random_perm
from selection.quickselect import select, select_two_way

BOTH = [select, select_two_way]


@pytest.fixture(params = BOTH, ids = ["select", "select_two_way"])
def select_fn(request):
    return request.param


def test_random_lists(select_fn):
    for seed in range(500):
        rng = random.Random(seed)
        n = rng.randint(1, 500)
        a = [rng.randint(0, 100) for _ in range(n)]
        k = rng.randrange(n)
        assert select_fn(list(a), k, random.Random(seed)) == sorted(a)[k]


EDGE_LISTS = {
    "single": [7],
    "all_equal": [5] * 20,
    "two_distinct": [0, 1, 1, 0, 1, 0, 0, 1, 1, 0],
    "sorted": list(range(30)),
    "reverse_sorted": list(range(30, 0, -1)),
    "negatives": [-3, 4, -10, 0, 2, -3, 8, -1],
    "strings": ["pear", "apple", "fig", "kiwi", "apple", "banana"],
}


@pytest.mark.parametrize("name", list(EDGE_LISTS))
def test_edge_lists(select_fn, name):
    a = EDGE_LISTS[name]
    expected = sorted(a)
    for k in range(len(a)):
        assert select_fn(list(a), k, random.Random(k)) == expected[k]


@pytest.mark.parametrize(
    "a, k",
    [([], 0), ([1, 2, 3], -1), ([1, 2, 3], 3)],
    ids = ["empty", "k_negative", "k_equals_n"],
)
def test_value_error(select_fn, a, k):
    with pytest.raises(ValueError):
        select_fn(a, k)


def test_default_rng(select_fn):
    assert select_fn([3, 1, 2], 1) == 2


def test_only_lt_and_eq(select_fn):
    a = random_perm(200, 1) + [5, 5, 5]
    answer, comparisons = count_comparisons(select_fn, a, 100, rng = random.Random(0))
    assert answer == sorted(a)[100]
    assert comparisons > 0


def test_counted_blocks_other_operators():
    with pytest.raises(TypeError):
        Counted(1) > Counted(2)


def test_same_seed_same_count(select_fn):
    a = random_perm(500, 3)
    _, first = count_comparisons(select_fn, a, 250, rng = random.Random(42))
    _, second = count_comparisons(select_fn, a, 250, rng = random.Random(42))
    assert first == second


def test_large_input_no_recursion_error():
    a = random_perm(100000, 1)
    assert select(a, 50000, random.Random(0)) == 50000


def test_two_way_quadratic_on_all_equal():
    a = all_equal(2000, 0)
    _, three_way = count_comparisons(select, a, 1000, rng = random.Random(0))
    _, two_way = count_comparisons(select_two_way, a, 1000, rng = random.Random(0))
    print(f"all_equal n = 2000: 3-way {three_way}, 2-way {two_way}")
    assert two_way > 10 * three_way
