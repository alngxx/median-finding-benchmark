"""Tests for bench/generators.py and bench/counting.py."""

import pytest

from bench import generators
from bench.counting import Counted, count_comparisons
from selection import baseline

N = 100

RANDOM_FAMILIES = [
    generators.random_perm,
    generators.few_distinct,
    generators.shared_prefix_strings,
]

ALL_FAMILIES = RANDOM_FAMILIES + [
    generators.sorted_list,
    generators.reverse_sorted,
    generators.all_equal,
    generators.organ_pipe,
]


@pytest.mark.parametrize("gen", ALL_FAMILIES)
def test_length_and_determinism(gen):
    assert len(gen(N, 1)) == N
    assert gen(N, 1) == gen(N, 1)


@pytest.mark.parametrize("gen", RANDOM_FAMILIES)
def test_different_seeds_differ(gen):
    assert gen(N, 1) != gen(N, 2)


def test_random_perm_is_permutation():
    assert sorted(generators.random_perm(N, 3)) == list(range(N))


def test_sorted_and_reverse():
    assert generators.sorted_list(5, 0) == [0, 1, 2, 3, 4]
    assert generators.reverse_sorted(5, 0) == [4, 3, 2, 1, 0]


def test_all_equal():
    assert len(set(generators.all_equal(N, 0))) == 1


def test_few_distinct():
    a = generators.few_distinct(1000, 1, d = 5)
    assert len(set(a)) <= 5
    assert len(set(generators.few_distinct(1000, 1))) <= 10


@pytest.mark.parametrize("n", [1, 2, 7, 8, 100])
def test_organ_pipe_up_then_down(n):
    a = generators.organ_pipe(n, 0)
    assert len(a) == n
    peak = a.index(max(a))
    assert all(a[i] <= a[i + 1] for i in range(peak))
    assert all(a[i] >= a[i + 1] for i in range(peak, n - 1))


def test_shared_prefix_strings():
    prefix_len = 20
    a = generators.shared_prefix_strings(N, 1, prefix_len = prefix_len)
    prefix = a[0][:prefix_len]
    assert prefix.islower()
    assert all(s.startswith(prefix) for s in a)
    assert all(len(s) == prefix_len + 10 for s in a)
    b = generators.shared_prefix_strings(N, 2, prefix_len = prefix_len)
    assert all(s.startswith(prefix) for s in b)


def test_counted_blocked_operators():
    a, b = Counted(1), Counted(2)
    with pytest.raises(TypeError):
        a > b
    with pytest.raises(TypeError):
        a <= b
    with pytest.raises(TypeError):
        a >= b
    with pytest.raises(TypeError):
        a != b


def test_counted_counts_lt_and_eq():
    Counted.count = 0
    a, b = Counted(1), Counted(2)
    assert a < b
    assert a == Counted(1)
    assert Counted.count == 2


@pytest.mark.parametrize(
    "a",
    [[5, 3, 9, 1, 7, 3], ["pear", "apple", "fig", "kiwi", "apple"]],
    ids = ["ints", "strings"],
)
def test_count_comparisons_with_baseline(a):
    original = list(a)
    for k in range(len(a)):
        answer, comparisons = count_comparisons(baseline.select, a, k)
        assert answer == sorted(original)[k]
        assert comparisons > 0
    assert a == original
