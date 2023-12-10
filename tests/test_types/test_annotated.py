"""Unit tests for the annotated types."""

import pytest
from algosdk.constants import HASH_LEN, MAX_ASSET_DECIMALS
from pydantic import TypeAdapter, ValidationError

from humblepy.types.annotated import (
    AlgorandAddress,
    AlgorandHash,
    AsaAssetName,
    AsaDecimals,
    AsaUnitName,
    AsaUrl,
    Uint32,
    Uint64,
)


def test_uint32_out_of_bounds():
    """Test that `Uint32` raises an error if the value is out of bounds."""
    ta = TypeAdapter(Uint32)
    with pytest.raises(ValidationError):
        ta.validate_python(-1)
    with pytest.raises(ValidationError):
        ta.validate_python(2**32)


def test_uint32_in_bounds():
    """Test that `Uint32` does not raise an error if the value is in bounds."""
    ta = TypeAdapter(Uint32)
    assert ta.validate_python(0) == 0
    assert ta.validate_python(1) == 1
    assert ta.validate_python(2**32 - 1) == 2**32 - 1


def test_uint64_out_of_bounds():
    """Test that `Uint64` raises an error if the value is out of bounds."""
    ta = TypeAdapter(Uint64)
    with pytest.raises(ValidationError):
        ta.validate_python(-1)
    with pytest.raises(ValidationError):
        ta.validate_python(2**64)


def test_uint64_in_bounds():
    """Test that `Uint64` does not raise an error if the value is in bounds."""
    ta = TypeAdapter(Uint64)
    assert ta.validate_python(0) == 0
    assert ta.validate_python(1) == 1
    assert ta.validate_python(2**64 - 1) == 2**64 - 1


def test_algorand_hash_length_out_of_bounds():
    """Test that `AlgorandHash` raises an error if the value is out of bounds."""
    ta = TypeAdapter(AlgorandHash)
    with pytest.raises(ValidationError):
        ta.validate_python(b"")
    with pytest.raises(ValidationError):
        ta.validate_python(b"\x00" * (HASH_LEN - 1))
    with pytest.raises(ValidationError):
        ta.validate_python(b"\x00" * (HASH_LEN + 1))


def test_algorand_hash_length_in_bounds():
    """Test that `AlgorandHash` does not raise an error if the value is in bounds."""
    ta = TypeAdapter(AlgorandHash)
    assert ta.validate_python(b"\x00" * HASH_LEN) == b"\x00" * HASH_LEN


def test_algorand_address_invalid():
    """Test that `AlgorandAddress` raises an error if the value is invalid."""
    ta = TypeAdapter(AlgorandAddress)
    with pytest.raises(ValidationError):
        ta.validate_python("")
    with pytest.raises(ValidationError):
        ta.validate_python(
            "1234567890123456789012345678901234567890123456789012345678901234"
        )


def test_algorand_address_valid():
    """Test that `AlgorandAddress` does not raise an error if the value is valid."""
    ta = TypeAdapter(AlgorandAddress)
    assert (
        ta.validate_python("VCMJKWOY5P5P7SKMZFFOCEROPJCZOTIJMNIYNUCKH7LRO45JMJP6UYBIJA")
        == "VCMJKWOY5P5P7SKMZFFOCEROPJCZOTIJMNIYNUCKH7LRO45JMJP6UYBIJA"
    )


def test_asa_decimals_out_of_bounds():
    """Test that `AsaDecimals` raises an error if the value is out of bounds."""
    ta = TypeAdapter(AsaDecimals)
    with pytest.raises(ValidationError):
        ta.validate_python(-1)
    with pytest.raises(ValidationError):
        ta.validate_python(20)


def test_asa_decimals_in_bounds():
    """Test that `AsaDecimals` does not raise an error if the value is in bounds."""
    ta = TypeAdapter(AsaDecimals)
    assert ta.validate_python(0) == 0
    assert ta.validate_python(1) == 1
    assert ta.validate_python(MAX_ASSET_DECIMALS) == MAX_ASSET_DECIMALS


def test_asa_url_encoded_length_out_of_bounds():
    """Test that `AsaUrl` raises an error if the encoded length of the value is out of bounds."""
    ta = TypeAdapter(AsaUrl)
    with pytest.raises(ValidationError):
        ta.validate_python(
            "https://www.example.com/1234567890123456789012345678901234567890123456789012345678901234567890123"
        )


def test_asa_url_invalid():
    """Test that `AsaUrl` raises an error if the value is invalid."""
    ta = TypeAdapter(AsaUrl)
    with pytest.raises(ValidationError):
        ta.validate_python("example.com")


def test_asa_url_valid():
    """Test that `AsaUrl` does not raise an error if the the value is a valid URL and its encoded length is in bounds."""
    ta = TypeAdapter(AsaUrl)
    assert (
        ta.validate_python("https://www.example.com/").unicode_string()
        == "https://www.example.com/"
    )


def test_asa_unit_name_encoded_length_out_of_bounds():
    """Test that `AsaUnitName` raises an error if the encoded length of the value is out of bounds."""
    ta = TypeAdapter(AsaUnitName)
    with pytest.raises(ValidationError):
        ta.validate_python("A" * 9)


def test_asa_unit_name_valid():
    """Test that `AsaUnitName` does not raise an error if the encoded length of the value is in bounds."""
    ta = TypeAdapter(AsaUnitName)
    assert ta.validate_python("USDC") == "USDC"


def test_asa_asset_name_encoded_length_out_of_bounds():
    """Test that `AsaAssetName` raises an error if the encoded length of the value is out of bounds."""
    ta = TypeAdapter(AsaAssetName)
    with pytest.raises(ValidationError):
        ta.validate_python("A" * 33)


def test_asa_asset_name_valid():
    """Test that `AsaAssetName` does not raise an error if the encoded length of the value is in bounds."""
    ta = TypeAdapter(AsaAssetName)
    assert ta.validate_python("USD Coin") == "USD Coin"
