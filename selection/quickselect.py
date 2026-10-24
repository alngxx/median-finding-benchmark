"""Randomized quickselect.

Primary author: An Loc Nguyen
"""

import random


def select(a: list, k: int, rng: random.Random | None = None):
    """Return the k-th smallest value of a (0-indexed). Iterative, 3-way partition.

    Compares elements only with < and ==. Replaces a with a sublist as it
    runs, so the caller's list is not changed.
    """
    if len(a) == 0 or k < 0 or k >= len(a):
        raise ValueError("empty list or k out of range")
    if rng is None:
        rng = random.Random()

    while True:
        pivot = a[rng.randrange(len(a))]

        # Invariant: every element of less is < pivot, every element of equal is == pivot,
        # every element of greater is > pivot. So the k-th smallest of a is in less if
        # k < len(less), is the pivot if k lands in equal, and otherwise is the
        # (k - len(less) - len(equal))-th smallest of greater.
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

        # A random pivot lands in the middle half of the sorted order with probability 1/2,
        # and then the kept part has at most 3/4 of the elements. So the expected work
        # is n + 3n/4 + (3/4)^2 n + ... = O(n).
        if k < len(less):
            a = less
        elif k < len(less) + len(equal):
            return pivot
        else:
            k -= len(less) + len(equal)
            a = greater


def select_two_way(a: list, k: int, rng: random.Random | None = None):
    """Same as select, but with a 2-way Lomuto partition. For comparison only.

    Uses only <. Elements equal to the pivot all go to the right of it, so the
    pivot lands at the left end of a run of equal values. On a list of all
    equal elements every round removes one element, which makes it quadratic.
    Modifies a.
    """
    if len(a) == 0 or k < 0 or k >= len(a):
        raise ValueError("empty list or k out of range")
    if rng is None:
        rng = random.Random()

    lo = 0
    hi = len(a) - 1
    while True:
        p = rng.randrange(lo, hi + 1)
        a[p], a[hi] = a[hi], a[p]
        pivot = a[hi]
        i = lo
        for j in range(lo, hi):
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[hi] = a[hi], a[i]

        # a[lo..i-1] are < pivot, a[i] is the pivot at its final index, a[i+1..hi] are not < pivot.
        if k == i:
            return a[i]
        if k < i:
            hi = i - 1
        else:
            lo = i + 1
