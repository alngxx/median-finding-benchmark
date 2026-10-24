"""Contract tests shared by every select function.

A test is skipped while the function raises NotImplementedError.
"""

import random

import pytest

from selection import baseline, median_of_medians, quickselect

SELECT_FUNCTIONS = {
    "quickselect": quickselect.select,
    "median_of_medians": median_of_medians.select,
    "baseline": baseline.select,
}

shuffler = random.Random(1)
two_distinct = [0] * 10 + [1] * 10
shuffler.shuffle(two_distinct)

EDGE_LISTS = {
    "single": [7],
    "all_equal": [5] * 20,
    "two_distinct": two_distinct,
    "sorted": list(range(30)),
    "reverse_sorted": list(range(30, 0, -1)),
}


@pytest.fixture(params = list(SELECT_FUNCTIONS))
def select_fn(request):
    return SELECT_FUNCTIONS[request.param]


def call(select_fn, a, k, seed = 0):
    try:
        return select_fn(list(a), k, random.Random(seed))
    except NotImplementedError:
        pytest.skip("not implemented yet")


def test_random_lists(select_fn):
    for seed in range(200):
        rng = random.Random(seed)
        n = rng.randint(1, 60)
        a = [rng.randint(0, 40) for _ in range(n)]
        expected = sorted(a)
        for k in (rng.randrange(n), 0, n - 1):
            assert call(select_fn, a, k, seed) == expected[k]


@pytest.mark.parametrize("name", list(EDGE_LISTS))
def test_edge_lists(select_fn, name):
    a = EDGE_LISTS[name]
    expected = sorted(a)
    for k in range(len(a)):
        assert call(select_fn, a, k) == expected[k]


@pytest.mark.parametrize(
    "a, k",
    [([], 0), ([1, 2, 3], -1), ([1, 2, 3], 3)],
    ids = ["empty", "k_negative", "k_equals_n"],
)
def test_value_error(select_fn, a, k):
    with pytest.raises(ValueError):
        call(select_fn, a, k)
