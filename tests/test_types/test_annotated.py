"""Unit tests for the annotated types."""

import pytest
from algosdk.constants import HASH_LEN, MAX_ASSET_DECIMALS
from pydantic import TypeAdapter, ValidationError
from pydantic_core import Url

from humblepy.types.annotated import (
    AlgorandAddress,
    AlgorandHash,
    Arc3Color,
    Arc3LocalizedUrl,
    Arc3NonTraitProperties,
    Arc3Sri,
    Arc3Url,
    Arc16Traits,
    AsaAssetName,
    AsaDecimals,
    AsaUnitName,
    AsaUrl,
    Base64Str,
    ImageMimeType,
    MimeType,
    Uint32,
    Uint64,
    UnicodeLocale,
)


class TestUint32:
    """Test the `Uint32` type."""

    ta = TypeAdapter(Uint32)

    @pytest.mark.parametrize("n", [-1, 2**32])
    def test_uint32_out_of_bounds(self, n: int) -> None:
        """Test that `Uint32` raises an error if the value is out of bounds."""
        with pytest.raises(ValidationError):
            self.ta.validate_python(n)

    @pytest.mark.parametrize("n", [0, 1, 2**32 - 1])
    def test_uint32_in_bounds(self, n: int) -> None:
        """Test that `Uint32` returns the original value  if the value is in bounds."""
        assert self.ta.validate_python(n) == n


class TestUint64:
    """Test the `Uint64` type."""

    ta = TypeAdapter(Uint64)

    @pytest.mark.parametrize("n", [-1, 2**64])
    def test_uint64_out_of_bounds(self, n: int) -> None:
        """Test that `Uint64` raises an error if the value is out of bounds."""
        with pytest.raises(ValidationError):
            self.ta.validate_python(n)

    @pytest.mark.parametrize("n", [0, 1, 2**64 - 1])
    def test_uint64_in_bounds(self, n: int) -> None:
        """Test that `Uint64` returns the original value  if the value is in bounds."""
        assert self.ta.validate_python(n) == n


class TestAlgorandHash:
    """Test the `AlgorandHash` type."""

    ta = TypeAdapter(AlgorandHash)

    @pytest.mark.parametrize(
        "x", [b"", b"\x00" * (HASH_LEN - 1), b"\x00" * (HASH_LEN + 1)]
    )
    def test_algorand_hash_length_invalid(self, x: bytes) -> None:
        """Test that `AlgorandHash` raises an error if the length of the value is not 32 bytes."""
        with pytest.raises(ValidationError):
            self.ta.validate_python(x)

    def test_algorand_hash_length_valid(self) -> None:
        """Test that `AlgorandHash` returns the original value if the length of the value is 32 bytes."""
        assert self.ta.validate_python(b"\x00" * HASH_LEN) == b"\x00" * HASH_LEN


class TestBase64Str:
    """Test the `Base64Str` type."""

    ta = TypeAdapter(Base64Str)

    @pytest.mark.parametrize(
        "x",
        [
            "Hello World!",
            "1234567890",
            "SGVsbG8g\nWorld!",
        ],
    )
    def test_base64str_invalid(self, x: str) -> None:
        """Test that `Base64Str` raises an error if the value is invalid."""
        with pytest.raises(ValidationError):
            self.ta.validate_python(x)

    def test_base64str_valid(self):
        """Test that `Base64Str` returns the original value  if the value is valid."""
        assert (
            self.ta.validate_python("iHcUslDaL/jEM/oTxqEX++4CS8o3+IZp7/V5Rgchqwc=")
            == "iHcUslDaL/jEM/oTxqEX++4CS8o3+IZp7/V5Rgchqwc="
        )


class TestAlgorandAddress:
    """Test the `AlgorandAddress` type."""

    ta = TypeAdapter(AlgorandAddress)

    @pytest.mark.parametrize(
        "x", ["", "1234567890123456789012345678901234567890123456789012345678901234"]
    )
    def test_algorand_address_invalid(self, x: str) -> None:
        """Test that `AlgorandAddress` raises an error if the value is invalid."""
        with pytest.raises(ValidationError):
            self.ta.validate_python(x)

    def test_algorand_address_valid(self) -> None:
        """Test that `AlgorandAddress` returns the original value  if the value is valid."""
        assert (
            self.ta.validate_python(
                "VCMJKWOY5P5P7SKMZFFOCEROPJCZOTIJMNIYNUCKH7LRO45JMJP6UYBIJA"
            )
            == "VCMJKWOY5P5P7SKMZFFOCEROPJCZOTIJMNIYNUCKH7LRO45JMJP6UYBIJA"
        )


class TestAsaDecimals:
    """Test the `AsaDecimals` type."""

    ta = TypeAdapter(AsaDecimals)

    @pytest.mark.parametrize("n", [-1, 20])
    def test_asa_decimals_out_of_bounds(self, n: int) -> None:
        """Test that `AsaDecimals` raises an error if the value is out of bounds."""
        with pytest.raises(ValidationError):
            self.ta.validate_python(n)

    @pytest.mark.parametrize("n", [0, 1, MAX_ASSET_DECIMALS])
    def test_asa_decimals_in_bounds(self, n: int) -> None:
        """Test that `AsaDecimals` does not raise an error if the value is in bounds."""
        assert self.ta.validate_python(n) == n


class TestUrlSubtypes:
    """Test `AsaUrl`, `Arc3Url`, and `Arc3LocalizedUrl`."""

    @pytest.mark.parametrize(
        "subtype, x",
        [
            (AsaUrl, "https://www.example.com/"),
            (Arc3Url, "https://www.example.com/"),
            (Arc3LocalizedUrl, "https://www.example.com/{locale}/"),
        ],
    )
    def test_url_is_string(self, subtype: Url, x: str) -> None:
        """Test that the subtype returns a string when passed a valid URL."""
        ta = TypeAdapter(subtype)
        assert isinstance(ta.validate_python(x), str)

    @pytest.mark.parametrize("subtype", [AsaUrl, Arc3Url, Arc3LocalizedUrl])
    def test_asa_url_invalid(self, subtype: Url) -> None:
        """Test that subtype raises an error if the value is not a valid URL."""
        ta = TypeAdapter(subtype)
        with pytest.raises(ValidationError):
            ta.validate_python("example.com")

    @pytest.mark.parametrize("subtype", [AsaUrl, Arc3Url, Arc3LocalizedUrl])
    def test_url_encoded_length_out_of_bounds(self, subtype: Url) -> None:
        """Test that the subtype raises an error if the encoded length of the value > 96 bytes."""
        ta = TypeAdapter(subtype)
        with pytest.raises(ValidationError):
            ta.validate_python(
                "https://www.example.com/1234567890123456789012345678901234567890123456789012345678901234567890123"
            )

    @pytest.mark.parametrize("subtype", [Arc3Url, Arc3LocalizedUrl])
    def test_url_invalid_scheme(self, subtype: Url) -> None:
        """Test that the subtype raises an error when passed a URL with a scheme that is not 'https' or 'ipfs'."""
        ta = TypeAdapter(subtype)
        with pytest.raises(ValidationError):
            ta.validate_python("http://example.com/")

    @pytest.mark.parametrize("subtype", [Arc3Url, Arc3LocalizedUrl])
    def test_url_invalid_gateway(self, subtype: Url) -> None:
        """Test that subtype raises a ValidationError when passed a URL that is a known public IPFS gateway."""
        ta = TypeAdapter(subtype)
        with pytest.raises(ValidationError):
            ta.validate_python(
                "https://ipfs.io/ipfs/bafybeihkoviema7g3gxyt6la7vd5ho32ictqbilu3wnlo3rs7ewhnp7lly/"
            )

    @pytest.mark.parametrize("subtype", [AsaUrl, Arc3Url])
    @pytest.mark.parametrize(
        "x",
        [
            "https://www.example.com/",
            "https://mysongs.com/song/mysong/",
            "https://s3.amazonaws.com/your-bucket/song/full/mysong.ogg",
            "ipfs://QmWS1VAdMD353A6SDk9wNyvkT14kyCiZrNDYAad4w1tKqT/metadata.json",
            "https://s3.amazonaws.com/your-bucket/images/{id}.png",
        ],
    )
    def test_url_valid(self, subtype: Url, x: str) -> None:
        """Test that subtype returns the original value if the the value is a valid URL and its encoded length is in bounds."""
        ta = TypeAdapter(subtype)
        assert str(ta.validate_python(x)) == x

    @pytest.mark.parametrize(
        "x",
        [
            "ipfs://QmWS1VAdMD353A6SDk9wNyvkT14kyCiZrNDYAad4w1tKqT/{locale}.json",
            "https://s3.amazonaws.com/your-bucket/images/{locale}/{id}.png",
        ],
    )
    def test_localized_url_valid(self, x: str) -> None:
        """Test that `Arc3LocalizedUrl` returns the original value if the URL is valid and contains the substring '{locale}'."""
        ta = TypeAdapter(Arc3LocalizedUrl)
        assert str(ta.validate_python(x)) == x

    @pytest.mark.parametrize(
        "x",
        [
            "https://www.example.com/",
            "ipfs://QmWS1VAdMD353A6SDk9wNyvkT14kyCiZrNDYAad4w1tKqT/metadata.json",
        ],
    )
    def test_arc3_localized_url_invalid(self, x: str) -> None:
        """Test that `Arc3LocalizedUrl` raises an error if URL does not contain the substring '{locale}'."""
        ta = TypeAdapter(Arc3LocalizedUrl)
        with pytest.raises(ValidationError):
            ta.validate_python(x)


class TestAsaUnitName:
    """Test the `AsaUnitName` type."""

    ta = TypeAdapter(AsaUnitName)

    @pytest.mark.parametrize("x", ["A" * 9])
    def test_asa_unit_name_encoded_length_out_of_bounds(self, x: str) -> None:
        """Test that `AsaUnitName` raises an error if the encoded length of the value is > 8 bytes."""
        with pytest.raises(ValidationError):
            self.ta.validate_python(x)

    @pytest.mark.parametrize("x", ["", "A", "A" * 8, "USDC"])
    def test_asa_unit_name_valid(self, x: str) -> None:
        """Test that `AsaUnitName` returns the original value if the encoded length of the value is <= 8 bytes."""
        assert self.ta.validate_python(x) == x


class TestAsaAssetName:
    """Test the `AsaAssetName` type."""

    ta = TypeAdapter(AsaAssetName)

    @pytest.mark.parametrize("x", ["A" * 33])
    def test_asa_asset_name_encoded_length_out_of_bounds(self, x: str) -> None:
        """Test that `AsaAssetName` raises an error if the encoded length of the value is > 32 bytes."""
        with pytest.raises(ValidationError):
            self.ta.validate_python(x)

    @pytest.mark.parametrize("x", ["", "A", "A" * 32, "USD Coin"])
    def test_asa_asset_name_valid(self, x: str) -> None:
        """Test that `AsaAssetName` returns the original value if the encoded length of the value is <= 32 bytes."""
        assert self.ta.validate_python(x) == x


class TestArc3Sri:
    """Test the `Arc3Sri` type."""

    ta = TypeAdapter(Arc3Sri)

    def test_arc3_sri_invalid_hash_algorithm(self) -> None:
        """Test that `Arc3Sri` raises an error when passed an ARC-3 SRI specifying an invalid hash algorithm."""
        with pytest.raises(ValidationError):
            self.ta.validate_python(
                "sha512-2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
            )

    def test_arc3_sri_missing_hash_algorithm(self) -> None:
        """Test that `Arc3Sri` returns the original string when passed an ARC-3 SRI where the hash algorithm name is missing."""
        with pytest.raises(ValidationError):
            self.ta.validate_python(
                "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
            )

    def test_arc3_sri_invalid_hash_digest_encoding(self) -> None:
        """Test that `Arc3Sri` raises an error when passed an SRI where the hash digest is not valid base64."""
        with pytest.raises(ValidationError):
            self.ta.validate_python("sha256-foo")

    def test_arc3_sri_invalid_hash_digest_length(self) -> None:
        """Test that `Arc3Sri` raises an error when passed an SRI where the hash digest is the wrong length."""
        with pytest.raises(ValidationError):
            self.ta.validate_python(
                "sha256-Li9vy3DqF8tnTXuiaAJuML3ky+er10rcgNR/VqsVpcw+ThHmYcwiB1pbOxEb"
            )

    def test_arc3_sri_valid(self):
        """Test that `Arc3Sri` returns the original string when passed a valid ARC-3 SRI."""
        assert (
            self.ta.validate_python(
                "sha256-LwArA6xMdnFF3bvQjwODpeTG/RVn61weQSuoRyynA1I="
            )
            == "sha256-LwArA6xMdnFF3bvQjwODpeTG/RVn61weQSuoRyynA1I="
        )


class TestMimeType:
    """Test the `MimeType` and `ImageMimeType` types."""

    @pytest.mark.parametrize("subtype", [MimeType, ImageMimeType])
    @pytest.mark.parametrize("x", ["", "img/png", "image/jpg"])
    def test_mime_type_invalid(self, subtype: MimeType | ImageMimeType, x: str) -> None:
        """Test that type raises a ValidationError when passed an invalid MIME type."""
        ta = TypeAdapter(subtype)
        with pytest.raises(ValidationError):
            ta.validate_python(x)

    @pytest.mark.parametrize(
        "x", ["image/png", "video/mp4", "audio/mpeg", "audio/ogg", "text/html"]
    )
    def test_mime_type_valid(self, x: str) -> None:
        """Test that `MimeType` returns the original string when passed a valid MIME type."""
        ta = TypeAdapter(MimeType)
        assert ta.validate_python(x) == x

    def test_image_mime_type_primary_type_mismatch(self) -> None:
        """Test that `ImageMimeType` raises a ValidationError when passed an invalid MIME type with an invalid primary type."""
        ta = TypeAdapter(ImageMimeType)
        with pytest.raises(ValidationError):
            ta.validate_python("video/png")

    @pytest.mark.parametrize("x", ["image/png", "image/jpeg", "image/gif"])
    def test_image_mime_type_valid(self, x: str) -> None:
        """Test that `ImageMimeType` returns the original string when passed a valid MIME type with a primary type specified."""
        ta = TypeAdapter(ImageMimeType)
        assert ta.validate_python(x) == x


class TestArc3Color:
    """Test the `Arc3Color` type."""

    ta = TypeAdapter(Arc3Color)

    @pytest.mark.parametrize("x", ["", "01234", "0123456"])
    def test_arc3_color_invalid_length(self, x: str) -> None:
        """Test that `Arc3Color` raises a ValidationError when passed a hexadecimal string that is not 6 characters long."""
        with pytest.raises(ValidationError):
            self.ta.validate_python(x)

    @pytest.mark.parametrize("x", ["0x1234", "#FF5733", "#9cb2e3", "abcdeg"])
    def test_arc3_color_invalid_characters(self, x: str) -> None:
        """Test that `Arc3Color` raises a ValidationError when passed a string containing non-hexadecimal characters."""
        with pytest.raises(ValidationError):
            self.ta.validate_python(x)

    @pytest.mark.parametrize("x", ["FF5733", "9cb2e3", "374f70"])
    def test_arc3_color_valid(self, x: str) -> None:
        """Test that `Arc3Color` returns the original string when passed a 6 character hexadecimal string."""
        assert self.ta.validate_python(x) == x


class TestLocaleString:
    """Test the `UnicodeLocale` type."""

    ta = TypeAdapter(UnicodeLocale)

    @pytest.mark.parametrize("x", ["", "12", "en_USA.UTF-8"])
    def test_locale_invalid_string(self, x: str) -> None:
        """Test that `UnicodeLocale` raises a ValidationError when passed a locale string that is empty or contains invalid characters."""
        with pytest.raises(ValidationError):
            self.ta.validate_python(x)

    @pytest.mark.parametrize("x", ["en_USA", "es_FR"])
    def test_locale_unknown_locale(self, x: str) -> None:
        """Test that `UnicodeLocale` raises a ValidationError when passed an valid locale."""
        with pytest.raises(ValidationError):
            self.ta.validate_python(x)

    @pytest.mark.parametrize("x", ["en", "en_US"])
    def test_locale_valid(self, x: str) -> None:
        """Test that `UnicodeLocale` returns the original string when passed a valid Unicode CLDR locale."""
        assert self.ta.validate_python(x) == x


class TestArc16Traits:
    """Test the `Arc16Traits` type."""

    ta = TypeAdapter(Arc16Traits)

    valid_dict = {
        "background": "red",
        "shirt_color": "blue",
        "glasses": "none",
        "tattoos": 4,
    }

    def test_arc16_traits_valid(self) -> None:
        """Test that validation succeeds when passed a valid dictionary."""
        assert self.ta.validate_python(self.valid_dict)

    @pytest.mark.parametrize(
        "x",
        [
            # Test invalid key type
            {1: "bar"},
            # Test invalid value types
            {"foo": set()},
            {"foo": list()},
            {"foo": tuple()},
        ],
    )
    def test_arc16_traits_invalid_non_strict(
        self, x: dict[int | str, str | set[int] | list[int] | tuple[int]]
    ) -> None:
        """Test that `Arc16Traits` raises a ValidationError when passed a dict with invalid types that can't be coerced."""
        with pytest.raises(ValidationError):
            self.ta.validate_python(x)

    @pytest.mark.parametrize(
        "x",
        [
            # Test invalid key type
            {1: "bar"},
            # Test invalid value types
            {"foo": True},
            {"foo": 1.0},
        ],
    )
    def test_arc16_traits_invalid_strict(
        self, x: dict[int | str, str | bool | float]
    ) -> None:
        """Test that `Arc16Traits` raises a ValidationError when passed a dict with invalid types in strict mode."""
        with pytest.raises(ValidationError):
            self.ta.validate_python(x, strict=True)

    @pytest.mark.parametrize("x, expected", [(True, 1), (1.0, 1)])
    def test_arc16_traits_valid_non_strict_coerced(
        self, x: bool | float, expected: int
    ) -> None:
        """Test that `Arc16Traits` returns the original value coerced to a string or int, where possible."""
        assert self.ta.validate_python({"foo": x})["foo"] == expected

    @pytest.mark.parametrize("x", ["True", "1"])
    def test_arc16_traits_valid_non_strict(self, x: str | int) -> None:
        """Test that `Arc16Traits` returns the original value when passed a string or int."""
        assert self.ta.validate_python({"foo": x})["foo"] == x


class TestArc3NonTraitProperties:
    """Test the `Arc3NonTraitProperties` type."""

    ta = TypeAdapter(Arc3NonTraitProperties)

    valid_dict = {
        "creator": "Tim Smith",
        "created_at": "January 2, 2022",
        "rich_property": {
            "string": "Name",
            "int": 1,
            "float": 3.14,
            "list": ["a", "b", "c"],
            "css": {
                "color": "#ffffff",
                "font-weight": "bold",
                "text-decoration": "underline",
            },
        },
    }

    def test_valid_dict(self) -> None:
        """Test that validation succeeds when passed a valid dictionary."""
        assert self.ta.validate_python(self.valid_dict)

    def test_traits_not_allowed(self) -> None:
        """Test that `Arc3NonTraitProperties` raises a ValidationError when passed a dictionary containing the key 'traits'."""
        test_dict = self.valid_dict.copy()
        test_dict["traits"] = {
            "background": "red",
            "shirt_color": "blue",
            "glasses": "none",
            "tattoos": 4,
        }
        with pytest.raises(ValidationError):
            self.ta.validate_python(test_dict)

    @pytest.mark.parametrize(
        "x, strict",
        [
            # Test invalid key type
            ({1: "bar"}, False),
            ({1: "bar"}, True),
            # Test invalid value types
            ({"foo": set()}, True),
            ({"foo": tuple()}, True),
            ({"foo": True}, True),
        ],
    )
    def test_invalid_types(
        self, x: dict[int | str, str | set[int] | tuple[int] | bool], strict: bool
    ) -> None:
        """Test that `Arc3NonTraitProperties` raises a ValidationError when passed a dictionary containing invalid types."""
        with pytest.raises(ValidationError):
            self.ta.validate_python(x, strict=strict)

    @pytest.mark.parametrize(
        "x, expected",
        [
            ({"foo": {0, 1, 2}}, [0, 1, 2]),
            ({"foo": (0, 1, 2)}, [0, 1, 2]),
            ({"foo": True}, 1),
        ],
    )
    def test_valid_types_not_strict_coerced(
        self, x: dict[str, set[int] | tuple[int] | bool], expected: list[int] | int
    ) -> None:
        """Test that `Arc3NonTraitProperties` raises a ValidationError when passed a dictionary containing invalid types."""
        assert self.ta.validate_python(x)["foo"] == expected
