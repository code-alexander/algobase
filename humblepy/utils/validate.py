"""Functions for data validation."""

import base64
import binascii
import hashlib
import string
from collections.abc import Iterable
from functools import cache
from typing import overload

from algosdk.encoding import is_valid_address
from babel import Locale, UnknownLocaleError
from pydantic_core import Url

from humblepy.utils.read import read_ipfs_gateways, read_mime_types


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
        str | Url: The value passed in.
    """
    url = value if isinstance(value, str) else value.unicode_string()
    if len(url.encode("utf-8")) > max_length:
        raise ValueError(f"'{value}' is > {max_length} bytes when encoded in UTF-8.")
    return value


@cache
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


def validate_base64(value: str) -> str:
    """Checks that the value is a valid base64 string.

    Args:
        value (str): The value to check.

    Raises:
        ValueError: If the value is not a valid base64 string.

    Returns:
        str: The value passed in.
    """
    try:
        base64.b64decode(value, validate=True)
    except binascii.Error:
        raise ValueError(f"'{value}' is not valid base64.")
    return value


def validate_sri(value: str) -> str:
    """Checks that the value is a valid W3C Subresource Integrity (SRI) value.

    Args:
        value (str): The value to check.

    Raises:
        ValueError: If the value is not a valid SRI.

    Returns:
        str: The value passed in.
    """
    supported_algorithms = {"sha256", "sha384", "sha512"}
    hash_algorithm = next(
        (x for x in supported_algorithms if value.startswith(f"{x}-")), None
    )
    if hash_algorithm is None:
        raise ValueError(
            f"'{value}' is not a valid SRI. String must start with 'sha256-', 'sha384-', or 'sha512-'."
        )
    hasher = hashlib.new(hash_algorithm)
    hash_digest = value.removeprefix(f"{hash_algorithm}-")
    try:
        validate_base64(hash_digest)
    except ValueError as e:
        raise ValueError(f"'{value}' is not a valid SRI. Hash digest {e}")
    if len(base64.b64decode(hash_digest)) != hasher.digest_size:
        raise ValueError(
            f"'{value}' is not a valid SRI. Expected {hasher.digest_size} byte hash digest, got {len(hash_digest)} bytes."
        )
    return value


def validate_arc3_sri(value: str) -> str:
    """Checks that the value is a valid SHA-256 Subresource Integrity (SRI) value.

    Args:
        value (str): The value to check.

    Raises:
        ValueError: If the value is not a valid SRI.

    Returns:
        str: The value passed in.
    """
    if not value.startswith("sha256-"):
        raise ValueError(
            f"'{value}' is not a valid ARC-3 SRI. String must start with 'sha256-'."
        )
    return validate_sri(value)


@cache
def validate_mime_type(value: str, primary_type: str | None = None) -> str:
    """Checks that the value is a valid MIME type.

    If `primary_type` is not `None`, then the value must be a valid MIME type with the specified primary type.
    E.g. if `primary_type` is 'image', then the value must be a valid MIME type starting with 'image/'.

    Args:
        value (str): The value to check.
        primary_type (str | None, optional): The primary type of the MIME type. Defaults to None.

    Raises:
        ValueError: If the value is not a valid MIME type.

    Returns:
        str: The value passed in.
    """
    if value not in read_mime_types():
        raise ValueError(f"'{value}' is not a valid MIME type.")
    if primary_type is not None and not value.startswith(f"{primary_type}/"):
        raise ValueError(f"'{value}' is not a valid {primary_type} MIME type.")
    return value


def validate_hex(value: str) -> str:
    """Checks that the value is a valid hexadecimal string.

    Args:
        value (str): The value to check.

    Raises:
        ValueError: If the value is not a valid hexadecimal string.

    Returns:
        str: The value passed in.
    """
    if not all(x in string.hexdigits for x in value):
        raise ValueError(f"'{value}' is not a valid hex string.")
    return value


def validate_locale(value: str) -> str:
    """Checks that the value is a valid Unicode CLDR locale.

    Args:
        value (str): The value to check.

    Raises:
        ValueError: If the value is not a valid locale identifier.
        UnknownLocaleError: If the value is not a valid Unicode CLDR locale.

    Returns:
        str: The value passed in.
    """
    try:
        Locale.parse(value)
    except ValueError as e:
        raise ValueError(f"'{value}' is not a valid locale identifier: {e}")
    except UnknownLocaleError:
        raise ValueError(f"'{value}' is not a valid Unicode CLDR locale.")
    return value


def validate_contains_substring(value: str | Url, substring: str) -> str | Url:
    """Checks that the value contains the substring.

    Args:
        value (str | Url): The value to check.
        substring (str): The substring to check for.

    Raises:
        ValueError: If the value does not contain the substring.

    Returns:
        str | Url: The value passed in.
    """
    value_string = value if isinstance(value, str) else value.unicode_string()
    if substring not in value_string:
        raise ValueError(f"'{value_string}' does not contain subtring '{substring}'.")
    return value


def validate_not_in(iterable: Iterable[str], element: str) -> Iterable[str]:
    """Checks that the element is not in the iterable.

    Args:
        element (str): The element to check for.
        iterable (Iterable): The iterable to check.

    Raises:
        ValueError: If the element is in the iterable.

    Returns:
        Iterable: The iterable passed in.
    """
    if element in iterable:
        raise ValueError(f"'{element}' is in {iterable}.")
    return iterable
