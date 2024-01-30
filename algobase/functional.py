"""Functions for type casting."""

from collections.abc import Callable
from typing import TypeVar

a = TypeVar("a")
b = TypeVar("b")


def maybe_bind(x: a | None, f: Callable[[a], b | None]) -> b | None:
    """Return the result of applying the function to the value if the value is not None, otherwise return None.

    Args:
        x (a | None): The value to apply the function to.
        f (Callable[[a], b  |  None]): The function to apply to the value.

    Returns:
        _type_: _description_
    """
    return f(x) if x is not None else None
