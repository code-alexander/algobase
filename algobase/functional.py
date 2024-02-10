"""Functions for type casting."""

from collections.abc import Callable, Iterable
from typing import ParamSpec, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def maybe_apply(x: A | None, f: Callable[[A], B]) -> B | None:
    """Return the result of applying the function to the value if the value is not None, otherwise return None.

    Args:
        x (A | None): The value to apply the function to.
        f (Callable[[A], B | None]): The function to apply to the value.

    Returns:
        B | None: The result of applying the function to the value, or None if the value is None.
    """
    return f(x) if x is not None else None


IT = TypeVar("IT")


def first_true(
    iterable: Iterable[IT],
    default: IT | None = None,
    predicate: Callable[[IT], bool] | None = None,
) -> IT | None:
    """Returns the first true value in the iterable.

    If no true value is found, it returns `default`.
    If `predicate` is not None, it returns the first item for which predicate(item) is true.

    Args:
        iterable (Iterable[IT]): The iterable.
        default (IT | None, optional): The default value to return if no true value is found. Defaults to None.
        predicate (Callable[[IT], bool] | None, optional): The predicate function. Defaults to None.

    Returns:
        IT | None: The item in the iterable that is true, or `default` if no true value is found.
    """
    return next(filter(predicate, iterable), default)


T = TypeVar("T")
P = ParamSpec("P")


def provide_context(*args: P.args, **kwargs: P.kwargs) -> Callable[[Callable[P, T]], T]:
    """A closure that provides context arguments to a function.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        Callable[[Callable[P, T]], T]: The wrapped function.
    """

    def wrapped(fn: Callable[P, T], *fn_args: P.args, **fn_kwargs: P.kwargs) -> T:
        """Calls the function with the context arguments and any additional arguments passed in.

        Args:
            fn (Callable[P, T]): The function to call.
            *fn_args: Variable length argument list.
            **fn_kwargs: Arbitrary keyword arguments.

        Returns:
            T: The result of calling the function.
        """
        return fn(*args, *fn_args, **kwargs, **fn_kwargs)

    return wrapped
