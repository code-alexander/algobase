"""Utility functions for hashing data."""

import hashlib


def sha256(data: bytes) -> bytes:
    """Returns a SHA-256 hash digest of the input data.

    Args:
        data (bytes): The data to hash.

    Returns:
        bytes: The hash digest.
    """
    return hashlib.sha256(data).digest()


def sha512_256(data: bytes) -> bytes:
    """Returns a SHA-512/256 hash digest of the input data.

    Args:
        data (bytes): The data to hash.

    Returns:
        bytes: The hash digest.
    """
    return hashlib.new("sha512_256", data).digest()
