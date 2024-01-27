"""Unit tests for the Algorand Standard Asset (ASA) Pydantic models."""


import pytest

from humblepy.choices import AsaType, AsaTypeChoice
from humblepy.models.arc3 import Arc3Metadata
from humblepy.models.asa import Asa
from humblepy.models.asset_params import AssetParams
from tests.types import FixtureDict


@pytest.mark.filterwarnings("ignore::UserWarning")
class TestAsa:
    """Tests the `Asa` Pydantic model."""

    def test_valid_dict(self, asa_nft_fixture: FixtureDict) -> None:
        """Test that validation succeeds when passed a valid dictionary."""
        assert Asa.model_validate(asa_nft_fixture)

    @pytest.mark.parametrize(
        "field, expected_type",
        [
            ("asa_type", AsaTypeChoice | None),
        ],
    )
    def test_annotated_types(self, field: str, expected_type: type) -> None:
        """Test that annotated types are correct."""
        assert Asa.model_fields[field].rebuild_annotation() == expected_type

    def test_asset_params_model(self, asa_nft_fixture: FixtureDict) -> None:
        """Test that the `asset_params` field is an `AssetParams` model."""
        assert isinstance(Asa.model_validate(asa_nft_fixture).asset_params, AssetParams)

    def test_metadata_model(self, asa_nft_fixture: FixtureDict) -> None:
        """Test that the `metadata` field is an `Arc3Metadata` model."""
        assert isinstance(Asa.model_validate(asa_nft_fixture).metadata, Arc3Metadata)

    def test_metadata_hash_none(self, asa_nft_fixture: FixtureDict) -> None:
        """Test that the metadata hash is None when passed a dict with no metadata."""
        test_dict = asa_nft_fixture.copy()
        del test_dict["metadata"]
        assert Asa.model_validate(test_dict).metadata_hash is None

    def test_metadata_hash_no_extra_metadata(
        self, asa_nft_fixture: FixtureDict
    ) -> None:
        """Test that the metadata hash is correct."""
        test_dict = asa_nft_fixture.copy()
        del test_dict["metadata"]["extra_metadata"]
        assert (
            Asa.model_validate(test_dict).metadata_hash
            == b"\xac\xba\xc8\x0c\xe91\t\xc6\x1b\xab\x11\x94\xb5\x08a\xff:\x91\xfc\xaa(\x813\x9e\xd7m\x90u\xf3\xc74\n"
        )

    def test_metadata_hash_with_extra_metadata(
        self, asa_nft_extra_metadata_fixture: FixtureDict
    ) -> None:
        """Test that the metadata hash is correct when passed a dict with the 'extra_metadata' property."""
        test_dict = asa_nft_extra_metadata_fixture.copy()
        assert (
            Asa.model_validate(test_dict).metadata_hash
            == b'\xc6\xc9\x99\xa7\xa9F[\xd9-M`-\xdbb\x9a\xba\xd3\xc4\xa8\t\xa2_\x1a0\xfe".&Te\x1c\x88'
        )

    def test_asset_unit_name_warning(self) -> None:
        """Test that a warning is raised if the asset unit name is not related to the metadata name."""
        with pytest.warns(UserWarning):
            Asa.model_validate(
                {
                    "asset_params": {
                        "total": 1,
                        "decimals": 0,
                        "unit_name": "test",
                        "asset_name": "unrelated",
                        "url": "https://tether.to/#arc3",
                    },
                    "metadata": {
                        "name": "unrelated",
                    },
                }
            )

    def test_asset_name_missing(self, asa_nft_fixture: FixtureDict) -> None:
        """Test that an error is raised if metadata is present but asset name is missing."""
        test_dict = asa_nft_fixture.copy()
        test_dict["asset_params"].pop("asset_name")
        with pytest.raises(ValueError):
            Asa.model_validate(test_dict)

    @pytest.mark.parametrize("asset_name", ["arc3", "foo@arc3"])
    def test_asset_name_not_recommended(
        self, asa_nft_fixture: FixtureDict, asset_name: str
    ) -> None:
        """Test that a warning is raised if the asset name format is allowed not recommended."""
        test_dict = asa_nft_fixture.copy()
        test_dict["asset_params"]["asset_name"] = asset_name
        with pytest.warns(UserWarning):
            Asa.model_validate(test_dict)

    def test_asset_name_metadata_name_missing(
        self, asa_nft_fixture: FixtureDict
    ) -> None:
        """Test that an error is raised if metadata is present but metadata name is missing."""
        test_dict = asa_nft_fixture.copy()
        test_dict["metadata"].pop("name")
        with pytest.raises(ValueError):
            Asa.model_validate(test_dict)

    def test_asset_name_metadata_name_mismatch(
        self, asa_nft_fixture: FixtureDict
    ) -> None:
        """Test that an error is raised if the metadata name could fit in the asset name field, but the two don't match."""
        test_dict = asa_nft_fixture.copy()
        test_dict["asset_params"]["asset_name"] = "foo"
        test_dict["metadata"]["name"] = "bar"
        with pytest.raises(ValueError):
            Asa.model_validate(test_dict)

    def test_asset_name_metadata_name_not_shortened(
        self, asa_nft_fixture: FixtureDict
    ) -> None:
        """Test that an error is raised if the metadata name could not fit in the asset name field, and the asset name isn't a shortened version of the metadata name."""
        test_dict = asa_nft_fixture.copy()
        test_dict["asset_params"]["asset_name"] = "foo"
        test_dict["metadata"]["name"] = "This Name Is More Than 32 Bytes Encoded"
        with pytest.raises(ValueError):
            Asa.model_validate(test_dict)

    def test_asset_url_not_none(self, asa_nft_fixture: FixtureDict) -> None:
        """Test that an error is raised if the asset URL is None and the metadata is ARC-3."""
        test_dict = asa_nft_fixture.copy()
        print(test_dict)
        test_dict["asset_params"].pop("url")
        with pytest.raises(ValueError):
            Asa.model_validate(test_dict)

    def test_asset_url_suffix(self, asa_nft_fixture: FixtureDict) -> None:
        """Test that an error is raised if the asset URL does not end with '#arc3'.

        Should only raise if the asset name is not 'arc3' or of the format <name>@arc3.
        """
        test_dict = asa_nft_fixture.copy()
        test_dict["asset_params"]["url"] = "https://tether.to/"
        with pytest.raises(ValueError):
            Asa.model_validate(test_dict)

    def test_decimals_mismatch(self, asa_nft_fixture: FixtureDict) -> None:
        """Test that an error is raised if the number of decimals in the metadata does not match the number of decimals in the asset params."""
        test_dict = asa_nft_fixture.copy()
        test_dict["asset_params"]["decimals"] = 1
        test_dict["metadata"]["decimals"] = 0
        with pytest.raises(ValueError):
            Asa.model_validate(test_dict)

    @pytest.mark.parametrize(
        "total, decimals, asa_type",
        [
            # Should only be valid for AsaType.NON_FUNGIBLE_PURE
            (1, 0, AsaType.NON_FUNGIBLE_FRACTIONAL),
            (1, 0, AsaType.FUNGIBLE),
            # Should only be valid for AsaType.NON_FUNGIBLE_FRACTIONAL
            (10, 1, AsaType.NON_FUNGIBLE_PURE),
            (100, 2, AsaType.NON_FUNGIBLE_PURE),
            (1000, 3, AsaType.NON_FUNGIBLE_PURE),
            (10, 1, AsaType.FUNGIBLE),
            (100, 2, AsaType.FUNGIBLE),
            (1000, 3, AsaType.FUNGIBLE),
            # Should only be valid for AsaType.FUNGIBLE
            (1, 1, AsaType.NON_FUNGIBLE_FRACTIONAL),
            (1, 2, AsaType.NON_FUNGIBLE_FRACTIONAL),
            (2, 0, AsaType.NON_FUNGIBLE_FRACTIONAL),
            (2, 10, AsaType.NON_FUNGIBLE_FRACTIONAL),
            (1, 1, AsaType.NON_FUNGIBLE_PURE),
            (1, 2, AsaType.NON_FUNGIBLE_PURE),
            (2, 0, AsaType.NON_FUNGIBLE_PURE),
            (2, 10, AsaType.NON_FUNGIBLE_PURE),
        ],
    )
    def test_asa_type_constraints_invalid(
        self,
        asa_nft_fixture: FixtureDict,
        total: int,
        decimals: int,
        asa_type: AsaTypeChoice,
    ) -> None:
        """Test that the ASA type is correct."""
        test_dict = asa_nft_fixture.copy()
        test_dict["asset_params"]["total"] = total
        test_dict["asset_params"]["decimals"] = decimals
        test_dict["metadata"][
            "decimals"
        ] = decimals  # To avoid throwing a different validation error
        test_dict["asa_type"] = asa_type
        with pytest.raises(ValueError):
            Asa.model_validate(test_dict)

    @pytest.mark.parametrize(
        "total, decimals, asa_type",
        [
            (1, 0, AsaType.NON_FUNGIBLE_PURE),
            (10, 1, AsaType.NON_FUNGIBLE_FRACTIONAL),
            (100, 2, AsaType.NON_FUNGIBLE_FRACTIONAL),
            (1000, 3, AsaType.NON_FUNGIBLE_FRACTIONAL),
            (1, 1, AsaType.FUNGIBLE),
            (1, 2, AsaType.FUNGIBLE),
            (2, 0, AsaType.FUNGIBLE),
            (2, 10, AsaType.FUNGIBLE),
        ],
    )
    def test_asa_type_constraints_valid(
        self,
        asa_nft_fixture: FixtureDict,
        total: int,
        decimals: int,
        asa_type: AsaTypeChoice,
    ) -> None:
        """Test that the ASA type is correct."""
        test_dict = asa_nft_fixture.copy()
        test_dict["asset_params"]["total"] = total
        test_dict["asset_params"]["decimals"] = decimals
        test_dict["metadata"][
            "decimals"
        ] = decimals  # To avoid throwing a different validation error
        test_dict["asa_type"] = asa_type
        assert Asa.model_validate(test_dict).derived_asa_type == asa_type
