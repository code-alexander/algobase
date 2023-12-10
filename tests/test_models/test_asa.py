"""Unit tests for the ASA pydantic model."""

import pytest
from pydantic import ValidationError

from humblepy.models.asa import Asa
from humblepy.types.annotated import (
    AlgorandAddress,
    AlgorandHash,
    AsaAssetName,
    AsaDecimals,
    AsaUnitName,
    AsaUrl,
    Uint64,
)


def test_total_is_mandatory():
    """Test that `total` is mandatory."""
    with pytest.raises(ValidationError):
        Asa()  # type: ignore


def test_total_is_uint64():
    """Test that `total` is `Uint64`."""
    assert Asa.model_fields["total"].rebuild_annotation() == Uint64


def test_total_strict():
    """Test that `total` raises an error in strict mode if passed a float or a string."""
    with pytest.raises(ValidationError):
        Asa.model_validate({"total": 1.0}, strict=True)
    with pytest.raises(ValidationError):
        Asa.model_validate({"total": "1"}, strict=True)


def test_total_non_strict():
    """Test that `total` does not raise an error in non-strict mode if passed a float or a string."""
    assert Asa.model_validate({"total": 1.0}, strict=False) == Asa(total=1)
    assert Asa.model_validate({"total": "1"}, strict=False) == Asa(total=1)


def test_decimals_default_is_zero():
    """Test that `decimals` defaults to zero."""
    assert Asa(total=1).decimals == 0


def test_decimals_is_asa_decimals():
    """Test that `decimals` `AsaDecimals`."""
    assert Asa.model_fields["decimals"].rebuild_annotation() == AsaDecimals


def test_default_frozen_default_is_false():
    """Test that `default_frozen` defaults to `False`."""
    assert Asa(total=1).default_frozen is False


def test_default_frozen_strict():
    """Test that `default_frozen` raises an error in strict mode if passed a non-boolean type."""
    with pytest.raises(ValidationError):
        Asa.model_validate({"total": 1, "default_frozen": 1}, strict=True)
    with pytest.raises(ValidationError):
        Asa.model_validate({"total": 1, "default_frozen": 1.0}, strict=True)
    with pytest.raises(ValidationError):
        Asa.model_validate({"total": 1, "default_frozen": "True"}, strict=True)
    with pytest.raises(ValidationError):
        Asa.model_validate({"total": 1, "default_frozen": "true"}, strict=True)


def test_default_frozen_non_strict():
    """Test that `default_frozen` does not raise an error in non-strict mode if passed a valid non-boolean type value."""
    assert Asa.model_validate({"total": 1, "default_frozen": 1}, strict=False) == Asa(
        total=1, default_frozen=True
    )
    assert Asa.model_validate({"total": 1, "default_frozen": 1.0}, strict=False) == Asa(
        total=1, default_frozen=True
    )
    assert Asa.model_validate(
        {"total": 1, "default_frozen": "True"}, strict=False
    ) == Asa(total=1, default_frozen=True)
    assert Asa.model_validate(
        {"total": 1, "default_frozen": "true"}, strict=False
    ) == Asa(total=1, default_frozen=True)


def test_unit_name_default_is_none():
    """Test that `unit_name` defaults to `None`."""
    assert Asa(total=1).unit_name is None


def test_unit_name_is_asa_unit_name_or_none():
    """Test that `unit_name` is `AsaUnitName` or `None`."""
    assert Asa.model_fields["unit_name"].rebuild_annotation() == AsaUnitName | None


def test_asset_name_default_is_none():
    """Test that `asset_name` defaults to `None`."""
    assert Asa(total=1).asset_name is None


def test_asset_name_is_asa_asset_name_or_none():
    """Test that `asset_name` is `AsaAssetName` or `None`."""
    assert Asa.model_fields["asset_name"].rebuild_annotation() == AsaAssetName | None


def test_url_default_is_none():
    """Test that `url` defaults to `None`."""
    assert Asa(total=1).url is None


def test_url_is_asa_url_or_none():
    """Test that `url` is `AsaUrl` or `None`."""
    assert Asa.model_fields["url"].rebuild_annotation() == AsaUrl | None


def test_metadata_hash_default_is_none():
    """Test that `metadata_hash` defaults to `None`."""
    assert Asa(total=1).metadata_hash is None


def test_metadata_hash_is_algorand_hash_or_none():
    """Test that `metadata_hash` is `AlgorandHash` or `None`."""
    assert Asa.model_fields["metadata_hash"].rebuild_annotation() == AlgorandHash | None


def test_manager_default_is_none():
    """Test that `manager` defaults to `None`."""
    assert Asa(total=1).manager is None


def test_manager_is_algorand_address_or_none():
    """Test that `manager` is `AlgorandAddress` or `None`."""
    assert Asa.model_fields["manager"].rebuild_annotation() == AlgorandAddress | None


def test_reserve_default_is_none():
    """Test that `reserve` defaults to `None`."""
    assert Asa(total=1).reserve is None


def test_reserve_is_algorand_address_or_none():
    """Test that `reserve` is `AlgorandAddress` or `None`."""
    assert Asa.model_fields["reserve"].rebuild_annotation() == AlgorandAddress | None


def test_freeze_default_is_none():
    """Test that `freeze` defaults to `None`."""
    assert Asa(total=1).freeze is None


def test_freeze_is_algorand_address_or_none():
    """Test that `freeze` is `AlgorandAddress` or `None`."""
    assert Asa.model_fields["freeze"].rebuild_annotation() == AlgorandAddress | None


def test_clawback_default_is_none():
    """Test that `clawback` defaults to `None`."""
    assert Asa(total=1).clawback is None


def test_clawback_is_algorand_address_or_none():
    """Test that `clawback` is `AlgorandAddress` or `None`."""
    assert Asa.model_fields["clawback"].rebuild_annotation() == AlgorandAddress | None
