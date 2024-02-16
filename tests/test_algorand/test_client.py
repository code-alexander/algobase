"""Test the Algorand client classes and functions."""

from types import SimpleNamespace

import pytest
from algosdk.kmd import KMDClient
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from algobase.algorand.account import Account
from algobase.algorand.client import (
    ClientConfig,
    create_algod_client,
    create_indexer_client,
    create_kmd_client,
    create_localnet_algod_client,
    create_localnet_default_config,
    create_localnet_indexer_client,
    create_localnet_kmd_client,
    find_wallet_id,
    get_default_account,
    is_default_account,
    is_localnet,
    match_account,
)
from algobase.choices import AlgorandApi, AlgorandApiChoice
from algobase.models import algod


def test_client_config() -> None:
    """Test the ClientConfig class."""
    config = ClientConfig(url="http://localhost:4001", credential="a" * 64)
    assert config.url == "http://localhost:4001"
    assert config.credential == "a" * 64
    assert config.headers is None


def test_create_algod_client() -> None:
    """Test the create_algod_client() function."""
    config = ClientConfig(url="http://localhost:4001", credential="a" * 64)
    client = create_algod_client(config)
    assert isinstance(client, AlgodClient)


def test_create_indexer_client() -> None:
    """Test the create_indexer_client() function."""
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
        (AlgorandApi.KMD, 4002),
    ],
)
def test_create_localnet_default_config(api: AlgorandApiChoice, port: int) -> None:
    """Test the create_localnet_default_config() function."""
    config = create_localnet_default_config(api)
    assert config.url == f"http://localhost:{port}"
    assert config.credential == "a" * 64
    assert config.headers is None


def test_create_localnet_algod_client() -> None:
    """Test the create_localnet_algod_client() function."""
    client = create_localnet_algod_client()
    assert isinstance(client, AlgodClient)


def test_create_localnet_indexer_client() -> None:
    """Test the create_localnet_indexer_client() function."""
    client = create_localnet_indexer_client()
    assert isinstance(client, IndexerClient)


def test_create_localnet_kmd_client() -> None:
    """Test the create_localnet_kmd_client() function."""
    client = create_localnet_kmd_client()
    assert isinstance(client, KMDClient)


def test_find_wallet_id() -> None:
    """Test the find_wallet_id() function."""

    class MockClient:
        def list_wallets(self):
            return [
                {
                    "driver_name": "sqlite",
                    "driver_version": 1,
                    "id": "test-id",
                    "mnemonic_ux": False,
                    "name": "unencrypted-default-wallet",
                    "supported_txs": ["pay", "keyreg"],
                },
                {
                    "driver_name": "sqlite",
                    "driver_version": 1,
                    "id": "other-id",
                    "mnemonic_ux": False,
                    "name": "other-wallet",
                    "supported_txs": ["pay", "keyreg"],
                },
            ]

    kmd_client = MockClient()
    assert find_wallet_id(kmd_client, "unencrypted-default-wallet") == "test-id"  # type: ignore[arg-type]


def test_is_default_account_true() -> None:
    """Test the is_default_account() function with an account object that should return True."""
    account = algod.Account.model_validate(
        {
            "address": "UYAUCPT2B475MESZAIA4BULTWIQM23VBPHQOLKKOPD7JRFB5QS4L3BOFUM",
            "amount": 2000000000000000,
            "amount-without-pending-rewards": 2000000000000000,
            "apps-local-state": [],
            "apps-total-schema": {"num-byte-slice": 0, "num-uint": 0},
            "assets": [],
            "created-apps": [],
            "created-assets": [],
            "min-balance": 100000,
            "participation": {
                "selection-participation-key": "IcW570qnseLIpLZz+s//F29KxIynBc2A1a8g1r12Q3Q=",
                "state-proof-key": "sDR9sBBWSSks/yYVFGTT1X6imLL12DF6+x+4l2hX7ji+EC+xUI8Paxpbo+tSC6o2BAv+QIRPF2zO3cvKn3N3Pg==",
                "vote-first-valid": 0,
                "vote-key-dilution": 100,
                "vote-last-valid": 30000,
                "vote-participation-key": "pD8DpT4PlIFXcOpXz3UoOUTbfIVQztQ2SAtUwqeLsu0=",
            },
            "pending-rewards": 0,
            "reward-base": 0,
            "rewards": 0,
            "round": 0,
            "status": "Online",
            "total-apps-opted-in": 0,
            "total-assets-opted-in": 0,
            "total-created-apps": 0,
            "total-created-assets": 0,
        }
    )
    assert is_default_account(account) is True


def test_is_default_account_false() -> None:
    """Test the is_default_account() function with an account object that should return False."""
    account = algod.Account.model_validate(
        {
            "address": "UYAUCPT2B475MESZAIA4BULTWIQM23VBPHQOLKKOPD7JRFB5QS4L3BOFUM",
            "amount": 1000000000,
            "amount-without-pending-rewards": 1000000000,
            "apps-local-state": [],
            "apps-total-schema": {"num-byte-slice": 0, "num-uint": 0},
            "assets": [],
            "created-apps": [],
            "created-assets": [],
            "min-balance": 100000,
            "participation": {
                "selection-participation-key": "IcW570qnseLIpLZz+s//F29KxIynBc2A1a8g1r12Q3Q=",
                "state-proof-key": "sDR9sBBWSSks/yYVFGTT1X6imLL12DF6+x+4l2hX7ji+EC+xUI8Paxpbo+tSC6o2BAv+QIRPF2zO3cvKn3N3Pg==",
                "vote-first-valid": 0,
                "vote-key-dilution": 100,
                "vote-last-valid": 30000,
                "vote-participation-key": "pD8DpT4PlIFXcOpXz3UoOUTbfIVQztQ2SAtUwqeLsu0=",
            },
            "pending-rewards": 0,
            "reward-base": 0,
            "rewards": 0,
            "round": 0,
            "status": "Offline",
            "total-apps-opted-in": 0,
            "total-assets-opted-in": 0,
            "total-created-apps": 0,
            "total-created-assets": 0,
        }
    )
    assert is_default_account(account) is False


def test_match_account() -> None:
    """Test the match_account() function."""

    class MockAlgodClient:
        def account_info(self, address: str) -> dict[str, object]:
            return {
                "address": address,
                "amount": 2000000000000000,
                "amount-without-pending-rewards": 2000000000000000,
                "apps-local-state": [],
                "apps-total-schema": {"num-byte-slice": 0, "num-uint": 0},
                "assets": [],
                "created-apps": [],
                "created-assets": [],
                "min-balance": 100000,
                "participation": {
                    "selection-participation-key": "IcW570qnseLIpLZz+s//F29KxIynBc2A1a8g1r12Q3Q=",
                    "state-proof-key": "sDR9sBBWSSks/yYVFGTT1X6imLL12DF6+x+4l2hX7ji+EC+xUI8Paxpbo+tSC6o2BAv+QIRPF2zO3cvKn3N3Pg==",
                    "vote-first-valid": 0,
                    "vote-key-dilution": 100,
                    "vote-last-valid": 30000,
                    "vote-participation-key": "pD8DpT4PlIFXcOpXz3UoOUTbfIVQztQ2SAtUwqeLsu0=",
                },
                "pending-rewards": 0,
                "reward-base": 0,
                "rewards": 0,
                "round": 0,
                "status": "Online",
                "total-apps-opted-in": 0,
                "total-assets-opted-in": 0,
                "total-created-apps": 0,
                "total-created-assets": 0,
            }

    algod_client = MockAlgodClient()

    address = "UYAUCPT2B475MESZAIA4BULTWIQM23VBPHQOLKKOPD7JRFB5QS4L3BOFUM"
    assert match_account(algod_client, [address], is_default_account) == address  # type: ignore[arg-type]

    with pytest.raises(ValueError):
        match_account(algod_client, [address], lambda x: x.amount == 0)  # type: ignore[arg-type]


def test_get_default_account() -> None:
    """Test the get_default_account() function."""

    class MockAlgodClient:
        """Mock AlgodClient class."""

        def account_info(self, address: str) -> dict[str, object]:
            return {
                "address": address,
                "amount": 2000000000000000,
                "amount-without-pending-rewards": 2000000000000000,
                "apps-local-state": [],
                "apps-total-schema": {"num-byte-slice": 0, "num-uint": 0},
                "assets": [],
                "created-apps": [],
                "created-assets": [],
                "min-balance": 100000,
                "participation": {
                    "selection-participation-key": "IcW570qnseLIpLZz+s//F29KxIynBc2A1a8g1r12Q3Q=",
                    "state-proof-key": "sDR9sBBWSSks/yYVFGTT1X6imLL12DF6+x+4l2hX7ji+EC+xUI8Paxpbo+tSC6o2BAv+QIRPF2zO3cvKn3N3Pg==",
                    "vote-first-valid": 0,
                    "vote-key-dilution": 100,
                    "vote-last-valid": 30000,
                    "vote-participation-key": "pD8DpT4PlIFXcOpXz3UoOUTbfIVQztQ2SAtUwqeLsu0=",
                },
                "pending-rewards": 0,
                "reward-base": 0,
                "rewards": 0,
                "round": 0,
                "status": "Online",
                "total-apps-opted-in": 0,
                "total-assets-opted-in": 0,
                "total-created-apps": 0,
                "total-created-assets": 0,
            }

        def suggested_params(self) -> SimpleNamespace:
            return SimpleNamespace(gen="dockernet-v1")

    class MockKmdClient:
        def list_wallets(self) -> list[dict[str, object]]:
            return [
                {
                    "driver_name": "sqlite",
                    "driver_version": 1,
                    "id": "test-id",
                    "mnemonic_ux": False,
                    "name": "unencrypted-default-wallet",
                    "supported_txs": ["pay", "keyreg"],
                },
                {
                    "driver_name": "sqlite",
                    "driver_version": 1,
                    "id": "other-id",
                    "mnemonic_ux": False,
                    "name": "other-wallet",
                    "supported_txs": ["pay", "keyreg"],
                },
            ]

        def init_wallet_handle(self, wallet_id: str, password: str) -> str:
            return "test-handle"

        def list_keys(self, wallet_handle: str) -> list[str]:
            return ["UYAUCPT2B475MESZAIA4BULTWIQM23VBPHQOLKKOPD7JRFB5QS4L3BOFUM"]

        def export_key(self, wallet_handle: str, password: str, address: str) -> str:
            return "OQNrVpF6MkzrMIz7HpC7nh9Nn6peCaBPTQTKMlcRqxGmAUE+eg8/1hJZAgHA0XOyIM1uoXng5alOeP6YlD2EuA=="

    algod_client = MockAlgodClient()
    kmd_client = MockKmdClient()

    account = get_default_account(algod_client, kmd_client)  # type: ignore[arg-type]
    assert isinstance(account, Account)
    assert (
        account.private_key
        == "OQNrVpF6MkzrMIz7HpC7nh9Nn6peCaBPTQTKMlcRqxGmAUE+eg8/1hJZAgHA0XOyIM1uoXng5alOeP6YlD2EuA=="
    )
    assert (
        account.address == "UYAUCPT2B475MESZAIA4BULTWIQM23VBPHQOLKKOPD7JRFB5QS4L3BOFUM"
    )

    # Test that a ValueError is raised if the Algod client isn't connected to a localnet.
    class MockMainnetClient(MockAlgodClient):
        def suggested_params(self) -> SimpleNamespace:
            return SimpleNamespace(gen="mainnet-v1")

    algod_client = MockMainnetClient()

    with pytest.raises(ValueError):
        get_default_account(algod_client, kmd_client)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "gen, expected",
    [
        ("mainnet-v1", False),
        ("testnet-v1", False),
        ("betanet-v1", False),
        ("devnet-v1", True),
        ("sandnet-v1", True),
        ("dockernet-v1", True),
        (None, False),
    ],
)
def test_is_localnet_true(gen: str | None, expected: bool) -> None:
    """Test the is_localnet() function."""

    class MockAlgodClient:
        """Mock AlgodClient class."""

        def suggested_params(self) -> SimpleNamespace:
            return SimpleNamespace(gen=gen)

    assert is_localnet(MockAlgodClient()) is expected  # type: ignore[arg-type]
