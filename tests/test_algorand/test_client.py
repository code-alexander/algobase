"""Test the Algorand client."""
from importlib import reload

import pytest
from _pytest.monkeypatch import MonkeyPatch

import algobase.algorand.client as client
import algobase.config as config


class TestAlgorandClient:
    """Test the AlgorandClient class."""

    @pytest.mark.parametrize("network", ["localnet", "testnet", "mainnet"])
    def test_network(self, monkeypatch: MonkeyPatch, network: str) -> None:
        """Test that the network is set correctly."""
        monkeypatch.setenv("AB_ALGORAND_NETWORK", network)
        reload(config)
        reload(client)
        test_client = client.AlgorandClient()
        assert test_client.network == network
