"""Functions for type casting."""

from collections.abc import Callable
from typing import TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def maybe_bind(x: A | None, f: Callable[[A], B | None]) -> B | None:
    """Return the result of applying the function to the value if the value is not None, otherwise return None.

    Args:
        x (a | None): The value to apply the function to.
        f (Callable[[a], b  |  None]): The function to apply to the value.

    Returns:
        _type_: _description_
    """
    return f(x) if x is not None else None


def pipe(x: A, f: Callable[[A], B], g: Callable[[B], C]) -> C:
    """Pipe a value through two functions.

    ```pipe(x, f, g)``` is equivalent to ```g(f(x))```

    Args:
        x (A): The value to pipe through the functions.
        f (Callable[[A], B]): The first function to apply to the value.
        g (Callable[[B], C]): The second function to apply to the result of the first function.

    Returns:
        C: The piped value.
    """
    return g(f(x))
