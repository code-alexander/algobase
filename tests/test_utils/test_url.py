"""Tests for the URL utility functions."""

import pytest

from algobase.utils.url import decode_url_braces


@pytest.mark.parametrize(
    "x, expected",
    [
        ("https://example.com/%7Bid%7D", "https://example.com/{id}"),
        (
            "ipfs://QmWS1VAdMD353A6SDk9wNyvkT14kyCiZrNDYAad4w1tKqT/%7Blocale%7D.json",
            "ipfs://QmWS1VAdMD353A6SDk9wNyvkT14kyCiZrNDYAad4w1tKqT/{locale}.json",
        ),
        ("https://example.com/", "https://example.com/"),
    ],
)
def test_decode_url_braces(x: str, expected: str) -> None:
    """Test that decode_url_braces() decodes braces in a URL."""
    assert decode_url_braces(x) == expected
