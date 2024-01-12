"""Unit tests for the humblepy.utils.read functions."""
import pytest

from humblepy.utils.read import read_ipfs_gateways, read_mime_types


def test_read_ipfs_gateways():
    """Test that read_ipfs_gateways() returns a list of IPFS gateways."""
    gateways = read_ipfs_gateways()
    assert gateways and isinstance(gateways, list)
    assert all(isinstance(gateway, str) for gateway in gateways)
    assert "https://ipfs.io" in gateways


@pytest.mark.parametrize(
    "mime_type",
    [
        "application/json",
        "text/html",
        "image/jpeg",
        "video/mp4",
        "audio/mpeg",
    ],
)
def test_read_mime_types(mime_type: str):
    """Test that read_mime_types() returns a list of MIME types."""
    mime_types = read_mime_types()
    assert mime_types and isinstance(mime_types, list)
    assert mime_type in mime_types
