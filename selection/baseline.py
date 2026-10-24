"""Reference baseline, not a graded algorithm."""

import random


def select(a: list, k: int, rng: random.Random | None = None):
    """Return sorted(a)[k]. Raise ValueError if a is empty or k is out of range."""
    if len(a) == 0 or k < 0 or k >= len(a):
        raise ValueError("empty list or k out of range")
    return sorted(a)[k]
