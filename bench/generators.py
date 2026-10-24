"""Seeded input families.

Author: An Loc Nguyen
"""


def random_perm(n: int, seed: int) -> list[int]:
    """Random permutation of n distinct ints."""
    raise NotImplementedError


def sorted_list(n: int, seed: int) -> list[int]:
    """Ints in ascending order."""
    raise NotImplementedError


def reverse_sorted(n: int, seed: int) -> list[int]:
    """Ints in descending order."""
    raise NotImplementedError


def all_equal(n: int, seed: int) -> list[int]:
    """n copies of one int."""
    raise NotImplementedError


def few_distinct(n: int, seed: int, d: int = 10) -> list[int]:
    """n ints drawn from d distinct values."""
    raise NotImplementedError


def organ_pipe(n: int, seed: int) -> list[int]:
    """Ints that rise to a peak, then fall."""
    raise NotImplementedError


def shared_prefix_strings(n: int, seed: int, prefix_len: int = 50) -> list[str]:
    """n strings that all start with the same prefix of prefix_len characters."""
    raise NotImplementedError
