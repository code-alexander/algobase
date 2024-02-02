"""Test the Algorand client."""
from importlib import reload

import pytest
from _pytest.monkeypatch import MonkeyPatch

import algobase.algorand.client as client


class TestAlgorandClient:
    """Test the AlgorandClient class."""

    @pytest.mark.parametrize("network", ["localnet", "testnet", "mainnet"])
    def test_network(self, monkeypatch: MonkeyPatch, network: str) -> None:
        """Test that the network is set correctly."""
        monkeypatch.setattr("algobase.config.settings.algorand_network", network)
        reload(client)
        test_client = client.AlgorandClient()
        assert test_client.network == network
