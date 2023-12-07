"""Functions for data validation."""

from typing import overload

from algosdk.encoding import is_valid_address
from pydantic_core import Url

from humblepy.utils.read import read_ipfs_gateways


def validate_address(value: str) -> str:
    """Checks that the value is a valid Algorand address.

    Args:
        value (str): The value to check.

    Raises:
        ValueError: If the value is not a valid Algorand address.

    Returns:
        str: The value passed in.
    """
    if not is_valid_address(value):
        raise ValueError(f"'{value}' is not a valid Algorand address.")
    return value


@overload  # pragma: no cover
def validate_encoded_length(value: str, max_length: int) -> str:
    ...


@overload  # pragma: no cover
def validate_encoded_length(value: Url, max_length: int) -> Url:
    ...


def validate_encoded_length(value: str | Url, max_length: int) -> str | Url:
    """Checks that the value is not longer than `max_length` when encoded in UTF-8.

    Args:
        value (str | Url): The value to check.
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


def validate_not_ipfs_gateway(url: Url) -> Url:
    """Checks that the URL host is not a known public IPFS gateway.

    Args:
        url (Url): The URL to check.

    Raises:
        ValueError: If the URL host is a known public IPFS gateway.

    Returns:
        Url: The URL passed in.
    """
    gateways = read_ipfs_gateways()
    if any(Url(gateway).host == url.host for gateway in gateways):
        raise ValueError(f"'{url.host}' is an IPFS gateway.")
    return url
