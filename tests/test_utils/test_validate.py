"""Unit tests for the humblepy.utils.validate functions."""

import pydantic
import pytest

from humblepy.utils.validate import (
    validate_address,
    validate_encoded_length,
    validate_not_ipfs_gateway,
)


def test_validate_address_valid():
    """Test that validate_address() returns the original string when passed a address."""
    assert (
        validate_address("VCMJKWOY5P5P7SKMZFFOCEROPJCZOTIJMNIYNUCKH7LRO45JMJP6UYBIJA")
        == "VCMJKWOY5P5P7SKMZFFOCEROPJCZOTIJMNIYNUCKH7LRO45JMJP6UYBIJA"
    )


def test_validate_address_invalid():
    """Test that validate_address() raises a ValueError when passed an invalid address."""
    with pytest.raises(ValueError):
        validate_address("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")


def test_validate_encoded_length_valid_str():
    """Test that validate_encoded_length() returns the original string when passed a string."""
    assert validate_encoded_length("hello", 10) == "hello"


def test_validate_encoded_length_invalid_str():
    """Test that validate_encoded_length() raises a ValueError when passed a string that is too long when encoded in UTF-8."""
    with pytest.raises(ValueError):
        validate_encoded_length("Café", 4)


def test_validate_encoded_length_valid_url():
    """Test that validate_encoded_length() returns the original URL when passed a URL."""
    url = pydantic.AnyUrl("https://example.com")
    assert validate_encoded_length(url, 100) == url


def test_validate_encoded_length_invalid_url():
    """Test that validate_encoded_length() returns the original URL when passed a URL that is too long when encoded in UTF-8."""
    url = pydantic.AnyUrl("https://example.com")
    with pytest.raises(ValueError):
        validate_encoded_length(url, 10)


def test_validate_not_ipfs_gateway_valid_url():
    """Test that validate_not_ipfs_gateway() returns the original URL when passed a URL that is not a known public IPFS gateway."""
    url = pydantic.AnyUrl(
        "ipfs://bafybeihkoviema7g3gxyt6la7vd5ho32ictqbilu3wnlo3rs7ewhnp7lly/"
    )
    assert validate_not_ipfs_gateway(url) == url


def test_validate_not_ipfs_gateway_invalid_url():
    """Test that validate_not_ipfs_gateway() raises a ValueError when passed a URL that is a known public IPFS gateway."""
    url = pydantic.AnyUrl(
        "https://ipfs.io/ipfs/bafybeihkoviema7g3gxyt6la7vd5ho32ictqbilu3wnlo3rs7ewhnp7lly/"
    )
    with pytest.raises(ValueError):
        validate_not_ipfs_gateway(url)
