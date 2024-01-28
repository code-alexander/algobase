"""Unit tests for the ARC-3 Pydantic models."""

import pytest
from pydantic import ValidationError

from algobase.models.arc3 import Arc3Localization, Arc3Metadata, Arc3Properties
from algobase.types.annotated import (
    Arc3Color,
    Arc3LocalizedUrl,
    Arc3Sri,
    Arc3Url,
    Arc16Traits,
    AsaDecimals,
    Base64Str,
    ImageMimeType,
    MimeType,
    UnicodeLocale,
)


class TestArc3Localization:
    """Tests the `Arc3Localization` Pydantic model."""

    valid_dict = {
        "uri": "ipfs://QmWS1VAdMD353A6SDk9wNyvkT14kyCiZrNDYAad4w1tKqT/{locale}.json",
        "default": "en",
        "locales": ["en", "es", "fr"],
        "integrity": {
            "es": "sha256-T0UofLOqdamWQDLok4vy/OcetEFzD8dRLig4229138Y=",
            "fr": "sha256-UUM89QQlXRlerdzVfatUzvNrEI/gwsgsN/lGkR13CKw=",
        },
    }

    def test_valid_dict(self) -> None:
        """Test that validation succeeds when passed a valid dictionary."""
        assert Arc3Localization.model_validate(self.valid_dict)

    @pytest.mark.parametrize(
        "field, expected_type",
        [
            ("uri", Arc3LocalizedUrl),
            ("default", UnicodeLocale),
            ("locales", list[UnicodeLocale]),
            ("integrity", dict[UnicodeLocale, Arc3Sri] | None),
        ],
    )
    def test_annotated_types(self, field: str, expected_type: type) -> None:
        """Test that annotated types are correct."""
        assert (
            Arc3Localization.model_fields[field].rebuild_annotation() == expected_type
        )

    @pytest.mark.parametrize("field", ["uri", "default", "locales"])
    def test_mandatory_fields(self, field: str) -> None:
        """Test that validation fails if a mandatory field is missing."""
        test_dict = self.valid_dict.copy()
        test_dict.pop(field)
        with pytest.raises(ValidationError):
            Arc3Localization.model_validate(test_dict)

    @pytest.mark.parametrize(
        "field, expected",
        [
            ("integrity", None),
        ],
    )
    def test_default_values(self, field: str, expected: int | bool | None) -> None:
        """Test that non-mandatory fields have the correct default values."""
        test_dict = self.valid_dict.copy()
        test_dict.pop(field)
        assert getattr(Arc3Localization.model_validate(test_dict), field) == expected


class TestArc3Properties:
    """Tests the `Arc3Properties` Pydantic model."""

    valid_dict = {
        "creator": "Tim Smith",
        "created_at": "January 2, 2022",
        "rich_property": {
            "name": "Name",
            "value": "123",
            "display_value": "123 Example Value",
            "class": "emphasis",
            "css": {
                "color": "#ffffff",
                "font-weight": "bold",
                "text-decoration": "underline",
            },
        },
        "traits": {
            "background": "red",
            "shirt_color": "blue",
            "glasses": "none",
            "tattoos": 4,
        },
    }

    def test_valid_dict(self) -> None:
        """Test that validation succeeds when passed a valid dictionary."""
        assert Arc3Properties.model_validate(self.valid_dict)

    @pytest.mark.parametrize(
        "field, expected_type",
        [
            ("traits", Arc16Traits | None),
        ],
    )
    def test_annotated_types(self, field: str, expected_type: type) -> None:
        """Test that annotated types are correct."""
        assert Arc3Properties.model_fields[field].rebuild_annotation() == expected_type

    @pytest.mark.parametrize(
        "field, expected",
        [
            ("traits", None),
        ],
    )
    def test_default_values(self, field: str, expected: int | bool | None) -> None:
        """Test that non-mandatory fields have the correct default values."""
        test_dict = self.valid_dict.copy()
        test_dict.pop(field)
        assert getattr(Arc3Properties.model_validate(test_dict), field) == expected


class TestArc3Metadata:
    """Tests the `Arc3Metadata` Pydantic model."""

    valid_dict = {
        "name": "My Song",
        "decimals": 1,
        "description": "My first and best song!",
        "image": "https://s3.amazonaws.com/your-bucket/song/cover/mysong.png",
        "image_integrity": "sha256-47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=",
        "image_mimetype": "image/png",
        "background_color": "FFFFFF",
        "external_url": "https://mysongs.com/song/mysong",
        "external_url_integrity": "sha256-7IGatqxLhUYkruDsEva52Ku43up6774yAmf0k98MXnU=",
        "external_url_mimetype": "text/html",
        "animation_url": "https://s3.amazonaws.com/your-bucket/song/preview/mysong.ogg",
        "animation_url_integrity": "sha256-LwArA6xMdnFF3bvQjwODpeTG/RVn61weQSuoRyynA1I=",
        "animation_url_mimetype": "audio/ogg",
        "properties": {
            "simple_property": "example value",
            "rich_property": {
                "name": "Name",
                "value": "123",
                "display_value": "123 Example Value",
                "class": "emphasis",
                "css": {
                    "color": "#ffffff",
                    "font-weight": "bold",
                    "text-decoration": "underline",
                },
            },
            "valid_types": {
                "string": "Name",
                "int": 1,
                "float": 3.14,
                "list": ["a", "b", "c"],
            },
            "array_property": {
                "name": "Name",
                "value": [1, 2, 3, 4],
                "class": "emphasis",
            },
            "traits": {
                "background": "red",
                "shirt_color": "blue",
                "glasses": "none",
                "tattoos": 4,
            },
        },
        "extra_metadata": "iHcUslDaL/jEM/oTxqEX++4CS8o3+IZp7/V5Rgchqwc=",
        "localization": {
            "uri": "ipfs://QmWS1VAdMD353A6SDk9wNyvkT14kyCiZrNDYAad4w1tKqT/{locale}.json",
            "default": "en",
            "locales": ["en", "es", "fr"],
            "integrity": {
                "es": "sha256-T0UofLOqdamWQDLok4vy/OcetEFzD8dRLig4229138Y=",
                "fr": "sha256-UUM89QQlXRlerdzVfatUzvNrEI/gwsgsN/lGkR13CKw=",
            },
        },
    }

    def test_valid_dict(self):
        """Test that validation succeeds when passed a valid dictionary."""
        assert Arc3Metadata.model_validate(self.valid_dict)

    @pytest.mark.parametrize(
        "field, expected_type",
        [
            ("decimals", AsaDecimals | None),
            ("image", Arc3Url | None),
            ("image_integrity", Arc3Sri | None),
            ("image_mimetype", ImageMimeType | None),
            ("background_color", Arc3Color | None),
            ("external_url", Arc3Url | None),
            ("external_url_integrity", Arc3Sri | None),
            ("animation_url", Arc3Url | None),
            ("animation_url_integrity", Arc3Sri | None),
            ("animation_url_mimetype", MimeType | None),
            ("properties", Arc3Properties | None),
            ("extra_metadata", Base64Str | None),
            ("localization", Arc3Localization | None),
        ],
    )
    def test_annotated_types(self, field: str, expected_type: type) -> None:
        """Test that annotated types are correct."""
        assert Arc3Metadata.model_fields[field].rebuild_annotation() == expected_type

    @pytest.mark.parametrize(
        "field, expected",
        [
            ("name", None),
            ("decimals", None),
            ("description", None),
            ("image", None),
            ("image_integrity", None),
            ("image_mimetype", None),
            ("background_color", None),
            ("external_url", None),
            ("external_url_integrity", None),
            ("external_url_mimetype", None),
            ("animation_url", None),
            ("animation_url_integrity", None),
            ("animation_url_mimetype", None),
            ("properties", None),
            ("extra_metadata", None),
            ("localization", None),
        ],
    )
    def test_default_values(self, field: str, expected: int | bool | None) -> None:
        """Test that non-mandatory fields have the correct default values."""
        test_dict = self.valid_dict.copy()
        test_dict.pop(field)
        assert getattr(Arc3Metadata.model_validate(test_dict), field) == expected
