"""Test the Algorand client classes and functions."""

import pytest
from algosdk.kmd import KMDClient
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from algobase.algorand.client import (
    ClientConfig,
    create_algod_client,
    create_indexer_client,
    create_kmd_client,
    create_localnet_algod_client,
    create_localnet_default_config,
    create_localnet_indexer_client,
    create_localnet_kmd_client,
)
from algobase.choices import AlgorandApi, AlgorandApiChoice


def test_client_config() -> None:
    """Test the ClientConfig class."""
    config = ClientConfig(url="http://localhost:4001", credential="a" * 64)
    assert config.url == "http://localhost:4001"
    assert config.credential == "a" * 64
    assert config.headers is None


def test_create_algod_client() -> None:
    """Test the create_algod_client function."""
    config = ClientConfig(url="http://localhost:4001", credential="a" * 64)
    client = create_algod_client(config)
    assert isinstance(client, AlgodClient)


def test_create_indexer_client() -> None:
    """Test the create_indexer_client function."""
    config = ClientConfig(url="http://localhost:4001", credential="a" * 64)
    client = create_indexer_client(config)
    assert isinstance(client, IndexerClient)


def test_create_kmd_client() -> None:
    """Test the create_kmd_client function."""
    config = ClientConfig(url="http://localhost:4001", credential="a" * 64)
    client = create_kmd_client(config)
    assert isinstance(client, KMDClient)


@pytest.mark.parametrize(
    "api, port",
    [
        (AlgorandApi.ALGOD, 4001),
        (AlgorandApi.INDEXER, 8980),
        (AlgorandApi.KMD, 7833),
    ],
)
def test_create_localnet_default_config(api: AlgorandApiChoice, port: int) -> None:
    """Test the create_localnet_default_config function."""
    config = create_localnet_default_config(api)
    assert config.url == f"http://localhost:{port}"
    assert config.credential == "a" * 64
    assert config.headers is None


def test_create_localnet_algod_client() -> None:
    """Test the create_localnet_algod_client function."""
    client = create_localnet_algod_client()
    assert isinstance(client, AlgodClient)


def test_create_localnet_indexer_client() -> None:
    """Test the create_localnet_indexer_client function."""
    client = create_localnet_indexer_client()
    assert isinstance(client, IndexerClient)


def test_create_localnet_kmd_client() -> None:
    """Test the create_localnet_kmd_client function."""
    client = create_localnet_kmd_client()
    assert isinstance(client, KMDClient)
