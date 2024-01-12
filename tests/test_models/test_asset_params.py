"""Unit tests for the AssetParams Pydantic model."""


import pytest
from pydantic import ValidationError

from humblepy.models.asset_params import AssetParams
from humblepy.types.annotated import (
    AlgorandAddress,
    AlgorandHash,
    AsaAssetName,
    AsaDecimals,
    AsaUnitName,
    AsaUrl,
    Uint64,
)


class TestAssetParams:
    """Tests the `AssetParams` Pydantic model."""

    valid_dict = {
        "total": 1,
        "decimals": 0,
        "default_frozen": False,
        "unit_name": "USDT",
        "asset_name": "Tether",
        "url": "https://tether.to/",
        "metadata_hash": b"fACPO4nRgO55j1ndAK3W6Sgc4APkcyFh",
        "manager": "7ZUECA7HFLZTXENRV24SHLU4AVPUTMTTDUFUBNBD64C73F3UHRTHAIOF6Q",
        "reserve": "7ZUECA7HFLZTXENRV24SHLU4AVPUTMTTDUFUBNBD64C73F3UHRTHAIOF6Q",
        "freeze": "7ZUECA7HFLZTXENRV24SHLU4AVPUTMTTDUFUBNBD64C73F3UHRTHAIOF6Q",
        "clawback": "7ZUECA7HFLZTXENRV24SHLU4AVPUTMTTDUFUBNBD64C73F3UHRTHAIOF6Q",
    }

    def test_valid_dict(self):
        """Test that validation succeeds when passed a valid dictionary."""
        assert AssetParams.model_validate(self.valid_dict)

    @pytest.mark.parametrize(
        "field, expected_type",
        [
            ("total", Uint64),
            ("decimals", AsaDecimals),
            ("unit_name", AsaUnitName | None),
            ("asset_name", AsaAssetName | None),
            ("url", AsaUrl | None),
            ("metadata_hash", AlgorandHash | None),
            ("manager", AlgorandAddress | None),
            ("reserve", AlgorandAddress | None),
            ("freeze", AlgorandAddress | None),
            ("clawback", AlgorandAddress | None),
        ],
    )
    def test_annotated_types(self, field: str, expected_type: type):
        """Test that annotated types are correct."""
        assert AssetParams.model_fields[field].rebuild_annotation() == expected_type

    @pytest.mark.parametrize("field", ["total"])
    def test_mandatory_fields(self, field: str):
        """Test that validation fails if a mandatory field is missing."""
        test_dict = self.valid_dict.copy()
        test_dict.pop(field)
        with pytest.raises(ValidationError):
            AssetParams.model_validate(test_dict)

    @pytest.mark.parametrize(
        "field, expected",
        [
            ("decimals", 0),
            ("default_frozen", False),
            ("unit_name", None),
            ("asset_name", None),
            ("url", None),
            ("metadata_hash", None),
            ("manager", None),
            ("reserve", None),
            ("freeze", None),
            ("clawback", None),
        ],
    )
    def test_default_values(self, field: str, expected: int | bool | None):
        """Test that non-mandatory fields have the correct default values."""
        test_dict = self.valid_dict.copy()
        test_dict.pop(field)
        assert getattr(AssetParams.model_validate(test_dict), field) == expected

    @pytest.mark.parametrize("x", [1.0, "1"])
    def test_total_invalid_strict(self, x: float | str):
        """Test that `total` raises an error in strict mode if passed a float or a string."""
        test_dict = self.valid_dict.copy()
        test_dict["total"] = x
        with pytest.raises(ValidationError):
            AssetParams.model_validate(test_dict, strict=True)

    @pytest.mark.parametrize("x, expected", [(1.0, 1), ("1", 1)])
    def test_total_valid_non_strict_coerced(self, x: float | str, expected: int):
        """Test that `total` does not raise an error in non-strict mode if passed a float or a string."""
        test_dict = self.valid_dict.copy()
        test_dict["total"] = x
        assert AssetParams.model_validate(test_dict, strict=False).total == expected

    @pytest.mark.parametrize("x", [1, 1.0, "True", "true"])
    def test_default_frozen_invalid_strict(self, x: int | float | str):
        """Test that `default_frozen` raises an error in strict mode if passed a non-boolean type."""
        test_dict = self.valid_dict.copy()
        test_dict["default_frozen"] = x
        with pytest.raises(ValidationError):
            AssetParams.model_validate(test_dict, strict=True)

    @pytest.mark.parametrize(
        "x, expected",
        [
            (1, True),
            (1.0, True),
            ("True", True),
            ("true", True),
            (0, False),
            (0.0, False),
            ("False", False),
            ("false", False),
        ],
    )
    def test_default_frozen_non_strict(self, x: int | float | str, expected: bool):
        """Test that `default_frozen` does not raise an error in non-strict mode if passed a valid non-boolean type value."""
        test_dict = self.valid_dict.copy()
        test_dict["default_frozen"] = x
        assert (
            AssetParams.model_validate(test_dict, strict=False).default_frozen
            == expected
        )
