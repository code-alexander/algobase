"""Unit tests for the humblepy.utils.read functions."""


from humblepy.utils.read import read_ipfs_gateways


def test_read_ipfs_gateways():
    """Test that read_ipfs_gateways() returns a list of IPFS gateways."""
    gateways = read_ipfs_gateways()
    assert gateways and isinstance(gateways, list)
    assert all(isinstance(gateway, str) for gateway in gateways)
    assert "https://ipfs.io" in gateways
