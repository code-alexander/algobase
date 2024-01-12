"""Unit tests for the humblepy.utils.validate functions."""

from collections.abc import Iterable

import pydantic
import pytest

from humblepy.utils.validate import (
    validate_address,
    validate_arc3_sri,
    validate_base64,
    validate_contains_substring,
    validate_encoded_length,
    validate_hex,
    validate_locale,
    validate_mime_type,
    validate_not_in,
    validate_not_ipfs_gateway,
    validate_sri,
)


class TestValidateAddress:
    """Tests the validate_address() function."""

    @pytest.mark.parametrize(
        "x", ["VCMJKWOY5P5P7SKMZFFOCEROPJCZOTIJMNIYNUCKH7LRO45JMJP6UYBIJA"]
    )
    def test_valid(self, x: str):
        """Test that validate_address() returns the original string when passed a address."""
        assert validate_address(x) == x

    @pytest.mark.parametrize(
        "x", ["AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" "12345"]
    )
    def test_invalid(self, x: str):
        """Test that validate_address() raises a ValueError when passed an invalid address."""
        with pytest.raises(ValueError):
            validate_address(x)


class TestValidateEncodedLength:
    """Tests the validate_encoded_length() function."""

    def test_valid_str(self):
        """Test that validate_encoded_length() returns the original string when passed a string."""
        assert validate_encoded_length("hello", 10) == "hello"

    def test_invalid_str(self):
        """Test that validate_encoded_length() raises a ValueError when passed a string that is too long when encoded in UTF-8."""
        with pytest.raises(ValueError):
            validate_encoded_length("Café", 4)

    def test_valid_url(self):
        """Test that validate_encoded_length() returns the original URL when passed a URL."""
        url = pydantic.AnyUrl("https://example.com")
        assert validate_encoded_length(url, 100) == url

    def test_invalid_url(self):
        """Test that validate_encoded_length() returns the original URL when passed a URL that is too long when encoded in UTF-8."""
        url = pydantic.AnyUrl("https://example.com")
        with pytest.raises(ValueError):
            validate_encoded_length(url, 10)


class TestValidateNotIpfsGateway:
    """Tests the validate_not_ipfs_gateway() function."""

    def test_valid_url(self):
        """Test that validate_not_ipfs_gateway() returns the original URL when passed a URL that is not a known public IPFS gateway."""
        url = pydantic.AnyUrl(
            "ipfs://bafybeihkoviema7g3gxyt6la7vd5ho32ictqbilu3wnlo3rs7ewhnp7lly/"
        )
        assert validate_not_ipfs_gateway(url) == url

    def test_invalid_url(self):
        """Test that validate_not_ipfs_gateway() raises a ValueError when passed a URL that is a known public IPFS gateway."""
        url = pydantic.AnyUrl(
            "https://ipfs.io/ipfs/bafybeihkoviema7g3gxyt6la7vd5ho32ictqbilu3wnlo3rs7ewhnp7lly/"
        )
        with pytest.raises(ValueError):
            validate_not_ipfs_gateway(url)


class TestValidateSri:
    """Tests the validate_sri() function."""

    def test_invalid_hash_algorithm(self):
        """Test that validate_sri() raises an error when passed an SRI specifying an invalid hash algorithm."""
        with pytest.raises(ValueError):
            validate_sri(
                "md5-LwArA6xMdnFF3bvQjwODpeTG/RVn61weQSuoRyynA1I="
            ) == "md5-LwArA6xMdnFF3bvQjwODpeTG/RVn61weQSuoRyynA1I="

    def test_missing_hash_algorithm(self):
        """Test that validate_sri() raises an error when passed an SRI where the hash algorithm name is missing."""
        with pytest.raises(ValueError):
            validate_sri(
                "m3HSJL1i83hdltRq0+o9czGb+8KJDKra4t/3JRlnPKcjI8PZm6XBHXx6zG4UuMXaDEZjR1wuXDre9G9zvN7AQw=="
            ) == "m3HSJL1i83hdltRq0+o9czGb+8KJDKra4t/3JRlnPKcjI8PZm6XBHXx6zG4UuMXaDEZjR1wuXDre9G9zvN7AQw=="

    def test_invalid_hash_digest_encoding(self):
        """Test that validate_sri() raises an error when passed an SRI where the hash digest is not valid base64."""
        with pytest.raises(ValueError):
            validate_sri("sha512-foo") == "sha512-foo"

    def test_invalid_hash_digest_length(self):
        """Test that validate_sri() raises an error when passed an SRI where the hash digest is the wrong length."""
        with pytest.raises(ValueError):
            validate_sri(
                "sha512-Li9vy3DqF8tnTXuiaAJuML3ky+er10rcgNR/VqsVpcw+ThHmYcwiB1pbOxEb"
            ) == "sha512-Li9vy3DqF8tnTXuiaAJuML3ky+er10rcgNR/VqsVpcw+ThHmYcwiB1pbOxEb"

    def test_valid(self):
        """Test that validate_sri() returns the original string when passed a valid SRI."""
        assert (
            validate_sri(
                "sha512-m3HSJL1i83hdltRq0+o9czGb+8KJDKra4t/3JRlnPKcjI8PZm6XBHXx6zG4UuMXaDEZjR1wuXDre9G9zvN7AQw=="
            )
            == "sha512-m3HSJL1i83hdltRq0+o9czGb+8KJDKra4t/3JRlnPKcjI8PZm6XBHXx6zG4UuMXaDEZjR1wuXDre9G9zvN7AQw=="
        )


class TestValidateArc3Sri:
    """Tests the validate_arc3_sri() function."""

    def test_invalid_hash_algorithm(self):
        """Test that validate_arc3_sri() raises an error when passed an SRI specifying an invalid hash algorithm."""
        with pytest.raises(ValueError):
            validate_arc3_sri(
                "sha512-LwArA6xMdnFF3bvQjwODpeTG/RVn61weQSuoRyynA1I="
            ) == "sha512-LwArA6xMdnFF3bvQjwODpeTG/RVn61weQSuoRyynA1I="

    def test_nvalid_hash_digest_encoding(self):
        """Test that validate_arc3_sri() raises an error when passed an SRI where the hash digest is not valid base64."""
        with pytest.raises(ValueError):
            validate_arc3_sri("sha256-foo") == "sha256-foo"

    def test_invalid_hash_digest_length(self):
        """Test that validate_arc3_sri() raises an error when passed an SRI where the hash digest is the wrong length."""
        with pytest.raises(ValueError):
            validate_arc3_sri(
                "sha256-Li9vy3DqF8tnTXuiaAJuML3ky+er10rcgNR/VqsVpcw+ThHmYcwiB1pbOxEb"
            ) == "sha256-Li9vy3DqF8tnTXuiaAJuML3ky+er10rcgNR/VqsVpcw+ThHmYcwiB1pbOxEb"

    def test_valid(self):
        """Test that validate_arc3_sri() returns the original string when passed a valid SRI."""
        assert (
            validate_arc3_sri("sha256-LwArA6xMdnFF3bvQjwODpeTG/RVn61weQSuoRyynA1I=")
            == "sha256-LwArA6xMdnFF3bvQjwODpeTG/RVn61weQSuoRyynA1I="
        )


class TestValidateMimeType:
    """tests the validate_mime_type() function."""

    @pytest.mark.parametrize("x", ["", "img/png"])
    def test_no_primary_type_invalid(self, x: str):
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
    def test_primary_type_invalid(self, x: str, primary_type: str):
        """Test that validate_mime_type() raises a ValueError when passed an MIME type with an invalid or conflicting primary type."""
        with pytest.raises(ValueError):
            validate_mime_type(x, primary_type)

    @pytest.mark.parametrize("x", ["image/png", "video/mp4", "audio/mpeg"])
    def test_no_primary_type_valid(self, x: str):
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
    def test_validate_mime_type_primary_type_valid(self, x: str, primary_type: str):
        """Test that validate_mime_type() returns the original string when passed a valid MIME type with a primary type specified."""
        assert validate_mime_type(x, primary_type) == x


def test_validate_hex_invalid():
    """Test that validate_hex() raises a ValueError when passed an invalid hexadecimal string."""
    with pytest.raises(ValueError):
        validate_hex("0x0123456789abcdefABCDEFg")


def test_validate_hex_valid():
    """Test that validate_hex() returns the original string when passed a valid hexadecimal string."""
    assert validate_hex("0123456789abcdefABCDEF") == "0123456789abcdefABCDEF"


def test_validate_locale_invalid_identifier():
    """Test that validate_locale() raises a ValueError when passed a locale identifier that is empty or contains invalid characters."""
    with pytest.raises(ValueError):
        validate_locale("")
    with pytest.raises(ValueError):
        validate_locale("12")
    with pytest.raises(ValueError):
        validate_locale("en_USA.UTF-8")


def test_validate_locale_invalid_locale():
    """Test that validate_locale() raises a ValueError when passed a locale identifier containing valid characters, but for an invalid/unknown locale."""
    with pytest.raises(ValueError):
        validate_locale("en_UA")


def test_validate_locale_valid():
    """Test that validate_locale() returns the original string when passed a valid locale."""
    assert validate_locale("en") == "en"
    assert validate_locale("en_US") == "en_US"


def test_validate_contains_substring_invalid():
    """Test that validate_contains_substring() raises a ValueError when passed a string that does not contain the specified substring."""
    with pytest.raises(ValueError):
        validate_contains_substring("hello", "world")


def test_validate_contains_substring_valid():
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
def test_validate_not_in_invalid(iterable: Iterable, element: str):
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
def test_validate_not_in_valid(iterable: Iterable, element: str):
    """Test that validate_not_in() raises a ValueError when passed an element that is in the iterable."""
    assert validate_not_in(iterable, element) == iterable


@pytest.mark.parametrize("x", ["SGVsbG8=", "d29ybGQ=", "SGVsbG8gd29ybGQ=", "dHJ1ZQ=="])
def test_validate_base64_valid(x: str):
    """Test that validate_base64() returns the original value when passed a valid string."""
    assert validate_base64(x) == x


@pytest.mark.parametrize("x", ["SGVsbG8", "d29ybGQ", "SGVsbG8gd29ybGQ", "dHJ1ZQ"])
def test_validate_base64_invalid(x: str):
    """Tests that validate_base64() raise a ValueError when passed an invalid string."""
    with pytest.raises(ValueError):
        validate_base64(x)
