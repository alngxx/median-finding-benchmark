"""Comparison counting.

Author: An Loc Nguyen
"""


class Counted:
    """Wraps a value and counts comparisons in a shared counter.

    Defines only __lt__ and __eq__. Any other comparison raises TypeError.
    Python falls back to a reflected __lt__ for ">" and inverts __eq__ for "!=",
    so the implementation must block those paths explicitly.
    """

    def __init__(self, value, counter):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError


def count_comparisons(select_fn, a: list, k: int, **kwargs):
    """Run select_fn on a wrapped copy of a. Return (answer_value, comparisons)."""
    raise NotImplementedError
