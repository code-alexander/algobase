"""Unit tests for the algobase.utils.validate functions."""

from collections.abc import Iterable

import pydantic
import pytest
from pydantic import ValidationError
from pydantic_core import Url

from algobase.utils.validate import (
    is_valid,
    validate_address,
    validate_arc3_sri,
    validate_arc19_asset_url,
    validate_base64,
    validate_contains_substring,
    validate_encoded_length,
    validate_hex,
    validate_is_power_of_10,
    validate_locale,
    validate_mime_type,
    validate_not_in,
    validate_not_ipfs_gateway,
    validate_sri,
    validate_type_compatibility,
)


class TestIsValid:
    """Tests the is_valid() function."""

    @staticmethod
    def dummy_function(n: int) -> int:
        """Dummy function for testing.

        Args:
            n (int): Integer to test.

        Raises:
            ValueError: If n > 1.

        Returns:
            int: The integer passed in.
        """
        if n > 1:
            raise ValueError("n > 1")
        return n

    def test_is_valid_true(self) -> None:
        """Test that is_valid() returns True when passed a valid function and arguments."""
        assert is_valid(self.dummy_function, 1) is True

    def test_is_valid_false(self) -> None:
        """Test that is_valid() returns False when passed an invalid function and arguments."""
        assert is_valid(self.dummy_function, 2) is False


class TestValidateAddress:
    """Tests the validate_address() function."""

    @pytest.mark.parametrize(
        "x", ["VCMJKWOY5P5P7SKMZFFOCEROPJCZOTIJMNIYNUCKH7LRO45JMJP6UYBIJA"]
    )
    def test_valid(self, x: str) -> None:
        """Test that validate_address() returns the original string when passed a address."""
        assert validate_address(x) == x

    @pytest.mark.parametrize(
        "x", ["AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" "12345"]
    )
    def test_invalid(self, x: str) -> None:
        """Test that validate_address() raises a ValueError when passed an invalid address."""
        with pytest.raises(ValueError):
            validate_address(x)


class TestValidateEncodedLength:
    """Tests the validate_encoded_length() function."""

    def test_valid_str(self) -> None:
        """Test that validate_encoded_length() returns the original string when passed a string."""
        assert validate_encoded_length("hello", 10) == "hello"

    def test_invalid_str(self) -> None:
        """Test that validate_encoded_length() raises a ValueError when passed a string that is too long when encoded in UTF-8."""
        with pytest.raises(ValueError):
            validate_encoded_length("Café", 4)

    def test_valid_url(self) -> None:
        """Test that validate_encoded_length() returns the original URL when passed a URL."""
        url = pydantic.AnyUrl("https://example.com")
        assert validate_encoded_length(url, 100) == url

    def test_invalid_url(self) -> None:
        """Test that validate_encoded_length() returns the original URL when passed a URL that is too long when encoded in UTF-8."""
        url = pydantic.AnyUrl("https://example.com")
        with pytest.raises(ValueError):
            validate_encoded_length(url, 10)


class TestValidateNotIpfsGateway:
    """Tests the validate_not_ipfs_gateway() function."""

    def test_valid_url(self) -> None:
        """Test that validate_not_ipfs_gateway() returns the original URL when passed a URL that is not a known public IPFS gateway."""
        url = "ipfs://bafybeihkoviema7g3gxyt6la7vd5ho32ictqbilu3wnlo3rs7ewhnp7lly/"
        assert validate_not_ipfs_gateway(url) == url

    def test_invalid_url(self) -> None:
        """Test that validate_not_ipfs_gateway() raises a ValueError when passed a URL that is a known public IPFS gateway."""
        url = "https://ipfs.io/ipfs/bafybeihkoviema7g3gxyt6la7vd5ho32ictqbilu3wnlo3rs7ewhnp7lly/"
        with pytest.raises(ValueError):
            validate_not_ipfs_gateway(url)


class TestValidateSri:
    """Tests the validate_sri() function."""

    def test_invalid_hash_algorithm(self) -> None:
        """Test that validate_sri() raises an error when passed an SRI specifying an invalid hash algorithm."""
        with pytest.raises(ValueError):
            validate_sri(
                "md5-LwArA6xMdnFF3bvQjwODpeTG/RVn61weQSuoRyynA1I="
            ) == "md5-LwArA6xMdnFF3bvQjwODpeTG/RVn61weQSuoRyynA1I="

    def test_missing_hash_algorithm(self) -> None:
        """Test that validate_sri() raises an error when passed an SRI where the hash algorithm name is missing."""
        with pytest.raises(ValueError):
            validate_sri(
                "m3HSJL1i83hdltRq0+o9czGb+8KJDKra4t/3JRlnPKcjI8PZm6XBHXx6zG4UuMXaDEZjR1wuXDre9G9zvN7AQw=="
            ) == "m3HSJL1i83hdltRq0+o9czGb+8KJDKra4t/3JRlnPKcjI8PZm6XBHXx6zG4UuMXaDEZjR1wuXDre9G9zvN7AQw=="

    def test_invalid_hash_digest_encoding(self) -> None:
        """Test that validate_sri() raises an error when passed an SRI where the hash digest is not valid base64."""
        with pytest.raises(ValueError):
            validate_sri("sha512-foo") == "sha512-foo"

    def test_invalid_hash_digest_length(self) -> None:
        """Test that validate_sri() raises an error when passed an SRI where the hash digest is the wrong length."""
        with pytest.raises(ValueError):
            validate_sri(
                "sha512-Li9vy3DqF8tnTXuiaAJuML3ky+er10rcgNR/VqsVpcw+ThHmYcwiB1pbOxEb"
            ) == "sha512-Li9vy3DqF8tnTXuiaAJuML3ky+er10rcgNR/VqsVpcw+ThHmYcwiB1pbOxEb"

    def test_valid(self) -> None:
        """Test that validate_sri() returns the original string when passed a valid SRI."""
        assert (
            validate_sri(
                "sha512-m3HSJL1i83hdltRq0+o9czGb+8KJDKra4t/3JRlnPKcjI8PZm6XBHXx6zG4UuMXaDEZjR1wuXDre9G9zvN7AQw=="
            )
            == "sha512-m3HSJL1i83hdltRq0+o9czGb+8KJDKra4t/3JRlnPKcjI8PZm6XBHXx6zG4UuMXaDEZjR1wuXDre9G9zvN7AQw=="
        )


class TestValidateArc3Sri:
    """Tests the validate_arc3_sri() function."""

    def test_invalid_hash_algorithm(self) -> None:
        """Test that validate_arc3_sri() raises an error when passed an SRI specifying an invalid hash algorithm."""
        with pytest.raises(ValueError):
            validate_arc3_sri(
                "sha512-LwArA6xMdnFF3bvQjwODpeTG/RVn61weQSuoRyynA1I="
            ) == "sha512-LwArA6xMdnFF3bvQjwODpeTG/RVn61weQSuoRyynA1I="

    def test_nvalid_hash_digest_encoding(self) -> None:
        """Test that validate_arc3_sri() raises an error when passed an SRI where the hash digest is not valid base64."""
        with pytest.raises(ValueError):
            validate_arc3_sri("sha256-foo") == "sha256-foo"

    def test_invalid_hash_digest_length(self) -> None:
        """Test that validate_arc3_sri() raises an error when passed an SRI where the hash digest is the wrong length."""
        with pytest.raises(ValueError):
            validate_arc3_sri(
                "sha256-Li9vy3DqF8tnTXuiaAJuML3ky+er10rcgNR/VqsVpcw+ThHmYcwiB1pbOxEb"
            ) == "sha256-Li9vy3DqF8tnTXuiaAJuML3ky+er10rcgNR/VqsVpcw+ThHmYcwiB1pbOxEb"

    def test_valid(self) -> None:
        """Test that validate_arc3_sri() returns the original string when passed a valid SRI."""
        assert (
            validate_arc3_sri("sha256-LwArA6xMdnFF3bvQjwODpeTG/RVn61weQSuoRyynA1I=")
            == "sha256-LwArA6xMdnFF3bvQjwODpeTG/RVn61weQSuoRyynA1I="
        )


class TestValidateMimeType:
    """tests the validate_mime_type() function."""

    @pytest.mark.parametrize("x", ["", "img/png"])
    def test_no_primary_type_invalid(self, x: str) -> None:
        """Test that validate_mime_type() raises a ValueError when passed an invalid MIME type with no primary type."""
        with pytest.raises(ValueError):
            validate_mime_type(x)

    @pytest.mark.parametrize(
        "x, primary_type",
        [
            ("image/png", "foo"),
            ("image/png", "text"),
            ("video/mp4", "image"),
        ],
    )
    def test_primary_type_invalid(self, x: str, primary_type: str) -> None:
        """Test that validate_mime_type() raises a ValueError when passed an MIME type with an invalid or conflicting primary type."""
        with pytest.raises(ValueError):
            validate_mime_type(x, primary_type)

    @pytest.mark.parametrize("x", ["image/png", "video/mp4", "audio/mpeg"])
    def test_no_primary_type_valid(self, x: str) -> None:
        """Test that validate_mime_type() returns the original string when passed a valid MIME type with no primary type specified."""
        assert validate_mime_type(x) == x

    @pytest.mark.parametrize(
        "x, primary_type",
        [
            ("image/png", "image"),
            ("audio/mpeg", "audio"),
            ("video/mp4", "video"),
        ],
    )
    def test_validate_mime_type_primary_type_valid(
        self, x: str, primary_type: str
    ) -> None:
        """Test that validate_mime_type() returns the original string when passed a valid MIME type with a primary type specified."""
        assert validate_mime_type(x, primary_type) == x


def test_validate_hex_invalid() -> None:
    """Test that validate_hex() raises a ValueError when passed an invalid hexadecimal string."""
    with pytest.raises(ValueError):
        validate_hex("0x0123456789abcdefABCDEFg")


def test_validate_hex_valid() -> None:
    """Test that validate_hex() returns the original string when passed a valid hexadecimal string."""
    assert validate_hex("0123456789abcdefABCDEF") == "0123456789abcdefABCDEF"


def test_validate_locale_invalid_identifier() -> None:
    """Test that validate_locale() raises a ValueError when passed a locale identifier that is empty or contains invalid characters."""
    with pytest.raises(ValueError):
        validate_locale("")
    with pytest.raises(ValueError):
        validate_locale("12")
    with pytest.raises(ValueError):
        validate_locale("en_USA.UTF-8")


def test_validate_locale_invalid_locale() -> None:
    """Test that validate_locale() raises a ValueError when passed a locale identifier containing valid characters, but for an invalid/unknown locale."""
    with pytest.raises(ValueError):
        validate_locale("en_UA")


def test_validate_locale_valid() -> None:
    """Test that validate_locale() returns the original string when passed a valid locale."""
    assert validate_locale("en") == "en"
    assert validate_locale("en_US") == "en_US"


def test_validate_contains_substring_invalid() -> None:
    """Test that validate_contains_substring() raises a ValueError when passed a string that does not contain the specified substring."""
    with pytest.raises(ValueError):
        validate_contains_substring("hello", "world")


def test_validate_contains_substring_valid() -> None:
    """Test that validate_contains_substring() returns the original string when passed a string that contains the specified substring."""
    assert validate_contains_substring("hello", "hello") == "hello"
    assert validate_contains_substring("hello", "hell") == "hello"
    assert validate_contains_substring("hello", "he") == "hello"
    assert validate_contains_substring("hello", "llo") == "hello"
    assert validate_contains_substring("hello", "lo") == "hello"
    assert validate_contains_substring("hello", "o") == "hello"


@pytest.mark.parametrize(
    "iterable, element",
    [
        (["hello", "world"], "hello"),
        ([1, 2, 3], 1),
        ({True, False}, True),
        ((None, False), None),
        (
            {
                "creator": "Tim Smith",
                "created_at": "January 2, 2022",
                "traits": {
                    "background": "red",
                    "shirt_color": "blue",
                    "glasses": "none",
                    "tattoos": 4,
                },
            },
            "traits",
        ),
    ],
)
def test_validate_not_in_invalid(iterable: Iterable[str], element: str) -> None:
    """Test that validate_not_in() raises a ValueError when passed an element that is in the iterable."""
    with pytest.raises(ValueError):
        validate_not_in(iterable, element)


@pytest.mark.parametrize(
    "iterable, element",
    [
        (["hello", "world"], "foo"),
        ([1, 2, 3], 0),
        ({True, False}, None),
        ((None, False), True),
        (
            {
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
            },
            "traits",
        ),
    ],
)
def test_validate_not_in_valid(iterable: Iterable[str], element: str) -> None:
    """Test that validate_not_in() raises a ValueError when passed an element that is in the iterable."""
    assert validate_not_in(iterable, element) == iterable


@pytest.mark.parametrize("x", ["SGVsbG8=", "d29ybGQ=", "SGVsbG8gd29ybGQ=", "dHJ1ZQ=="])
def test_validate_base64_valid(x: str) -> None:
    """Test that validate_base64() returns the original value when passed a valid string."""
    assert validate_base64(x) == x


@pytest.mark.parametrize("x", ["SGVsbG8", "d29ybGQ", "SGVsbG8gd29ybGQ", "dHJ1ZQ"])
def test_validate_base64_invalid(x: str) -> None:
    """Tests that validate_base64() raise a ValueError when passed an invalid string."""
    with pytest.raises(ValueError):
        validate_base64(x)


@pytest.mark.parametrize(
    "n", [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000]
)
def test_validate_is_power_of_10_valid(n: int) -> None:
    """Test that validate_is_power_of_10() returns the original value when passed a valid power of 10."""
    assert validate_is_power_of_10(n) == n


@pytest.mark.parametrize("n", [-10, 0, 5, 15])
def test_validate_is_power_of_10_invalid(n: int) -> None:
    """Test that validate_is_power_of_10() raises a ValueError when passed an invalid power of 10."""
    with pytest.raises(ValueError):
        validate_is_power_of_10(n)


@pytest.mark.parametrize("value, _type", [("https://www.google.com", Url)])
def test_validate_type_compatibility_valid(value: str, _type: type) -> None:
    """Test that validate_type_compatibility() returns the original value when passed a value that is compatible with the specified type."""
    assert validate_type_compatibility(value, _type) == value


@pytest.mark.parametrize("value, _type", [("www.google.com", Url)])
def test_validate_type_compatibility_invalid(value: str, _type: type) -> None:
    """Test that validate_type_compatibility() raises an error when passed a value that is incompatible with the specified type."""
    with pytest.raises(ValidationError):
        validate_type_compatibility(value, _type)


@pytest.mark.parametrize(
    "url",
    [
        "template-ipfs://{ipfscid:0:dag-pb:reserve:sha2-256}/arc3.json",
        "template-ipfs://{ipfscid:1:raw:reserve:sha2-256}",
        "template-ipfs://{ipfscid:1:dag-pb:reserve:sha2-256}/metadata.json",
    ],
)
def test_validate_arc19_asset_url_valid(url: str) -> None:
    """Test that validate_arc19_asset_url() returns the original value when passed a valid URL for Algorand ARC-19."""
    assert validate_arc19_asset_url(url) == url


@pytest.mark.parametrize(
    "url",
    [
        "template-ipfs://{ipfscid:0:raw:reserve:sha2-256}/arc3.json",
        "template-ipfs://{ipfscid:v1:raw:reserve:sha2-256}",
        "https://example.com",
    ],
)
def test_validate_arc19_url_invalid(url: str) -> None:
    """Test that validate_arc19_url() raises an error when passed an invalid URL for Algorand ARC-19."""
    with pytest.raises(ValueError):
        validate_arc19_asset_url(url) == url
