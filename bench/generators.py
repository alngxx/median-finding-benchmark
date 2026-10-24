"""Seeded input families.

Author: An Loc Nguyen

Every function is deterministic for a given (n, seed) and uses its own
random.Random(seed), never the global random state.
"""

import random
import string


def random_perm(n: int, seed: int) -> list[int]:
    """Random permutation of 0 to n - 1."""
    a = list(range(n))
    random.Random(seed).shuffle(a)
    return a


def sorted_list(n: int, seed: int) -> list[int]:
    """0 to n - 1 in ascending order. The seed is unused."""
    return list(range(n))


def reverse_sorted(n: int, seed: int) -> list[int]:
    """n - 1 down to 0. The seed is unused."""
    return list(range(n - 1, -1, -1))


def all_equal(n: int, seed: int) -> list[int]:
    """n copies of 0. The seed is unused."""
    return [0] * n


def few_distinct(n: int, seed: int, d: int = 10) -> list[int]:
    """n values drawn uniformly from 0 to d - 1."""
    rng = random.Random(seed)
    return [rng.randrange(d) for _ in range(n)]


def organ_pipe(n: int, seed: int) -> list[int]:
    """Rises from 0 to a peak at the middle, then falls. The seed is unused."""
    up = list(range((n + 1) // 2))
    down = list(range(n // 2 - 1, -1, -1))
    return up + down


def shared_prefix_strings(n: int, seed: int, prefix_len: int = 50) -> list[str]:
    """n strings: a fixed lowercase prefix of prefix_len letters, then 10 random letters.

    The prefix depends only on prefix_len. Duplicates are possible.
    """
    letters = string.ascii_lowercase
    prefix = "".join(letters[i % 26] for i in range(prefix_len))
    rng = random.Random(seed)
    return [prefix + "".join(rng.choice(letters) for _ in range(10)) for _ in range(n)]
