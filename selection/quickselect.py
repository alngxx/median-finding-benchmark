"""Randomized quickselect.

Primary author: An Loc Nguyen
"""

import random


def select(a: list, k: int, rng: random.Random | None = None):
    """Return the k-th smallest value of a (0-indexed). Iterative, 3-way partition."""
    raise NotImplementedError


def select_two_way(a: list, k: int, rng: random.Random | None = None):
    """Same as select, but with a 2-way partition. For comparison only."""
    raise NotImplementedError
