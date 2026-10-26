"""Deterministic median of medians.

Primary author: Thanh Trung Le
"""

import random

# Lists with at most this many elements are solved directly with insertion sort.
BASE_CUTOFF = 25


def insertion_sort(b: list) -> None:
    """Sort b in place, comparing only with <."""
    for i in range(1, len(b)):
        x = b[i]
        j = i - 1
        while j >= 0 and x < b[j]:
            b[j + 1] = b[j]
            j -= 1
        b[j + 1] = x


def select(a: list, k: int, rng: random.Random | None = None, group_size: int = 5):
    """Return the k-th smallest value of a (0-indexed). Groups of group_size.

    Compares elements only with < and ==. rng is ignored. It is accepted so the
    signature matches quickselect.
    """
    if len(a) == 0 or k < 0 or k >= len(a):
        raise ValueError("empty list or k out of range")
    if not isinstance(group_size, int) or group_size < 3 or group_size % 2 == 0:
        raise ValueError("group_size must be an odd integer >= 3")

    while True:
        if len(a) <= BASE_CUTOFF:
            insertion_sort(a)
            return a[k]

        medians = []
        for start in range(0, len(a), group_size):
            group = a[start:start + group_size]
            insertion_sort(group)
            medians.append(group[(len(group) - 1) // 2])

        # Invariant: the pivot is the median of the group medians. Half of the groups have a
        # median <= pivot, and in each of those groups (g + 1) / 2 elements are <= their median,
        # so at least about (g + 1) / (4g) of all elements are <= pivot. That is 3n / 10 for
        # g = 5, and the same holds for >= pivot. So each side has at most about 7n / 10
        # elements, and T(n) <= T(n / 5) + T(7n / 10) + O(n) is linear because 1/5 + 7/10 < 1.
        # For g = 3 the fractions are 1/3 and 2/3, which sum to 1, so the cost becomes n log n.
        pivot = select(medians, (len(medians) - 1) // 2, group_size = group_size)

        less = []
        equal = []
        greater = []
        for x in a:
            if x < pivot:
                less.append(x)
            elif x == pivot:
                equal.append(x)
            else:
                greater.append(x)

        if k < len(less):
            a = less
        elif k < len(less) + len(equal):
            return pivot
        else:
            k -= len(less) + len(equal)
            a = greater