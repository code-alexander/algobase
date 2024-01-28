"""Unit tests for the hash functions."""

import pytest

from algobase.utils.hash import sha256, sha512_256


@pytest.mark.parametrize(
    "data, expected_digest",
    [
        (
            b"hello",
            b",\xf2M\xba_\xb0\xa3\x0e&\xe8;*\xc5\xb9\xe2\x9e\x1b\x16\x1e\\\x1f\xa7B^s\x043b\x93\x8b\x98$",
        ),
        (
            b"world",
            b"Hn\xa4b$\xd1\xbbO\xb6\x80\xf3O|\x9a\xd9j\x8f$\xec\x88\xbes\xea\x8eZle&\x0e\x9c\xb8\xa7",
        ),
    ],
)
def test_sha256(data: bytes, expected_digest: bytes) -> None:
    """Test that sha256() returns the correct hash digest."""
    assert sha256(data) == expected_digest


@pytest.mark.parametrize(
    "data, expected_digest",
    [
        (
            b"hello",
            b"\xe3\r\x87\xcf\xa2\xa7]\xb5E\xea\xc4\xd6\x1b\xaf\x97\x03f\xa85|\x7fr\xfa\x95\xb5-\n\xcc\xb6\x98\xf1:",
        ),
        (
            b"world",
            b"\xb8\x00\x7f\xc6@\xbe\xf3\xe2\xf1\x0e\xa7\xad\x96\x81\xf6\xfd\xbd\x13(\x87@i`\xf3eE+\xa0\xa1^e\xe2",
        ),
    ],
)
def test_sha512_256(data: bytes, expected_digest: bytes) -> None:
    """Test that sha512_256() returns the correct hash digest."""
    assert sha512_256(data) == expected_digest
