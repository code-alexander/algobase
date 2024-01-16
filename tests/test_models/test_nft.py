"""Unit tests for the Algorand Standard Asset (ASA) NFT Pydantic models."""

from typing import Literal

import pytest
from pydantic import ValidationError

from humblepy.models.nft import FractionalNft, NftType, PureNft


class TestNftType:
    """Tests the `NftType` enum."""

    @pytest.mark.parametrize("x", ["pure", "fractional"])
    def test_valid_values(self, x: str) -> None:
        """Test that valid values are accepted."""
        assert getattr(NftType, x) == x

    @pytest.mark.parametrize("x", ["impure", "other"])
    def test_invalid_values(self, x: str) -> None:
        """Test that an invalid value raises an error."""
        with pytest.raises(AttributeError):
            getattr(NftType, x)


class TestPureNft:
    """Tests the `PureNft` Pydantic model."""

    valid_dict = {
        "nft_type": "pure",
        "total": 1,
        "decimals": 0,
    }

    def test_valid_dict(self) -> None:
        """Test that validation succeeds when passed a valid dictionary."""
        assert PureNft.model_validate(self.valid_dict)

    @pytest.mark.parametrize(
        "field, expected",
        [
            ("nft_type", "pure"),
            ("total", 1),
            ("decimals", 0),
        ],
    )
    def test_default_values(
        self,
        field: str,
        expected: Literal["pure"] | Literal[1] | Literal[0],
    ) -> None:
        """Test that the default values are correct."""
        assert getattr(PureNft(), field) == expected

    @pytest.mark.parametrize(
        "field, x",
        [
            ("nft_type", "fractional"),
            ("nft_type", "other"),
            ("total", -1),
            ("total", 0),
            ("total", 2),
            ("total", 10),
            ("decimals", -1),
            ("decimals", 1),
            ("decimals", 2),
            ("decimals", 10),
        ],
    )
    def test_invalid_values(
        self,
        field: str,
        x: str | int,
    ) -> None:
        """Test that an error is raised if passed a dictionary with an invalid value."""
        test_dict = self.valid_dict.copy()
        test_dict[field] = x
        with pytest.raises(ValidationError):
            PureNft.model_validate(test_dict)


class TestFractionalNft:
    """Tests the `FractionalNft` Pydantic model."""

    valid_dict = {
        "nft_type": "fractional",
        "total": 10,
        "decimals": 1,
    }

    def test_valid_dict(self) -> None:
        """Test that validation succeeds when passed a valid dictionary."""
        assert FractionalNft.model_validate(self.valid_dict)

    @pytest.mark.parametrize(
        "field, expected",
        [
            ("nft_type", "fractional"),
        ],
    )
    def test_default_values(
        self,
        field: str,
        expected: Literal["fractional"],
    ) -> None:
        """Test that the default values are correct."""
        test_dict = self.valid_dict.copy()
        test_dict.pop(field)
        assert getattr(FractionalNft.model_validate(test_dict), field) == expected

    @pytest.mark.parametrize(
        "field, x",
        [
            ("nft_type", "pure"),
            ("nft_type", "other"),
            ("total", -1),
            ("total", 0),
            ("total", 2),
            ("total", 10),
            ("decimals", -1),
            ("decimals", 0),
            ("decimals", 2),
            ("decimals", 10),
        ],
    )
    def test_invalid_values(
        self,
        field: str,
        x: str | int,
    ) -> None:
        """Test that an error is raised if passed a dictionary with an invalid value."""
        test_dict = self.valid_dict.copy()
        test_dict[field] = x
        with pytest.raises(ValidationError):
            PureNft.model_validate(test_dict)
