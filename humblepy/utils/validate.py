"""Functions for data validation."""

import typing

import algosdk
import pydantic_core


def validate_address(value: str) -> str:
    """Checks that the value is a valid Algorand address.

    Args:
        value (str): The value to check.

    Raises:
        ValueError: If the value is not a valid Algorand address.

    Returns:
        str: The value passed in.
    """
    if not algosdk.encoding.is_valid_address(value):
        raise ValueError(f"'{value}' is not a valid Algorand address.")
    return value


@typing.overload  # pragma: no cover
def validate_encoded_length(value: str, max_length: int) -> str:
    ...


@typing.overload  # pragma: no cover
def validate_encoded_length(
    value: pydantic_core.Url, max_length: int
) -> pydantic_core.Url:
    ...


def validate_encoded_length(
    value: str | pydantic_core.Url, max_length: int
) -> str | pydantic_core.Url:
    """Checks that the value is not longer than `max_length` when encoded in UTF-8.

    Args:
        value (str | pydantic_core.Url): The value to check.
        max_length (int): The maximum length of the value when encoded in UTF-8.

    Raises:
        ValueError: If the value is longer than `max_length` when encoded in UTF-8.

    Returns:
        _type_: The value passed in.
    """
    url = value if isinstance(value, str) else value.unicode_string()
    if len(url.encode("utf-8")) > max_length:
        raise ValueError(f"'{value}' is > {max_length} bytes when encoded in UTF-8.")
    return value
