"""Test the type casting functions."""

from typing import TypeVar

import pytest

from algobase.functional import first_true, maybe_apply, provide_context

T = TypeVar("T")


@pytest.mark.parametrize(
    "x, f",
    [("some_string", str), (1, int), (1.0, float), (True, bool), ([0, 1, 2], list)],
)
def test_maybe_apply_cast(x: T, f: type[T]) -> None:
    """Test that maybe_apply() returns the correct value when casting some value."""
    assert isinstance(maybe_apply(x, f), f)
    assert maybe_apply(x, f) == x


@pytest.mark.parametrize(
    "x, f",
    [(None, str), (None, int), (None, float), (None, bool), (None, list)],
)
def test_maybe_apply_cast_none(x: None, f: type[T]) -> None:
    """Test that maybe_apply() returns None when casting None."""
    assert maybe_apply(x, f) is None
    assert maybe_apply(x, f) == x


def test_provide_context() -> None:
    """Tests the provide_context() function."""
    context = provide_context(a=4, b=5, c=6)

    def f(x, y, z, a, b, c):
        """Function that accepts context arguments."""
        return x + y + z + a + b + c

    assert context(f, 1, 2, z=3) == 21


def test_first_true() -> None:
    """Tests the first_true() function."""
    iterable = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    def predicate(n: int) -> bool:
        """Predicate function.

        Args:
            n (int): The number to check.

        Returns:
            bool: True if the number is 5, False otherwise.
        """
        return n == 5

    assert first_true(iterable, predicate=predicate) == 5


def test_first_true_default() -> None:
    """Tests the first_true() function with a default value provided."""
    iterable = [0, 1, 2, 3, 4]

    def predicate(n: int) -> bool:
        """Predicate function.

        Args:
            n (int): The number to check.

        Returns:
            bool: True if the number is 5, False otherwise.
        """
        return n == 5

    assert first_true(iterable, default=5, predicate=predicate) == 5
