"""Test the type casting functions."""

from typing import TypeVar

import pytest

from algobase.functional import maybe_bind, pipe

T = TypeVar("T")


@pytest.mark.parametrize(
    "x, f",
    [("some_string", str), (1, int), (1.0, float), (True, bool), ([0, 1, 2], list)],
)
def test_maybe_bind_cast(x: T, f: type[T]) -> None:
    """Test that maybe_bind() returns the correct value when casting some value."""
    assert isinstance(maybe_bind(x, f), f)
    assert maybe_bind(x, f) == x


@pytest.mark.parametrize(
    "x, f",
    [(None, str), (None, int), (None, float), (None, bool), (None, list)],
)
def test_maybe_bind_cast_none(x: None, f: type[T]) -> None:
    """Test that maybe_bind() returns None when casting None."""
    assert maybe_bind(x, f) is None
    assert maybe_bind(x, f) == x


def test_pipe() -> None:
    """Tests the pipe function."""

    def f(x: int) -> str:
        return str(x)

    def g(x: str) -> bool:
        return x == "1"

    assert pipe(1, f, g) is True
    assert pipe(1, f, g) == g(f(1))
