"""Comparison counting.

Author: An Loc Nguyen
"""


class Counted:
    """Wraps a value and counts comparisons in a class-level counter.

    Only __lt__ and __eq__ compare and count. The explicit TypeError overrides
    (__le__, __gt__, __ge__, __ne__) do not fix the counting. They enforce the
    rule that algorithms use only < and ==, so a violation fails loudly and both
    algorithms are held to the same operations.
    """

    count = 0

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        Counted.count += 1
        return self.value < other.value

    def __eq__(self, other):
        Counted.count += 1
        return self.value == other.value

    def __le__(self, other):
        raise TypeError("only < and == are allowed")

    def __gt__(self, other):
        raise TypeError("only < and == are allowed")

    def __ge__(self, other):
        raise TypeError("only < and == are allowed")

    def __ne__(self, other):
        raise TypeError("only < and == are allowed")


def count_comparisons(select_fn, a: list, k: int, **kwargs):
    """Run select_fn on a wrapped copy of a. Return (answer_value, comparisons).

    The original list is not modified.
    """
    wrapped = [Counted(x) for x in a]
    Counted.count = 0
    answer = select_fn(wrapped, k, **kwargs)
    return answer.value, Counted.count
