"""Test configuration settings."""

from importlib import reload

import pytest
from _pytest.monkeypatch import MonkeyPatch

import algobase.config as config
from algobase.choices import AlgorandNetwork, AlgorandNetworkChoice


@pytest.mark.parametrize(
    "env, config_name, default",
    [
        ("", "algorand_network", AlgorandNetwork.LOCALNET),
        ("dev", "algorand_network", AlgorandNetwork.LOCALNET),
        ("test", "algorand_network", AlgorandNetwork.TESTNET),
        ("prod", "algorand_network", AlgorandNetwork.MAINNET),
        ("", "algod_token", "a" * 64),
        ("dev", "algod_token", "a" * 64),
        ("test", "algod_token", None),
        ("prod", "algod_token", None),
    ],
)
def test_env_defaults(
    monkeypatch: MonkeyPatch,
    env: str,
    config_name: str,
    default: str | AlgorandNetworkChoice | None,
) -> None:
    """Test config value defaults for each environment."""
    monkeypatch.setenv("AB_ENV", env)
    monkeypatch.delenv(f"AB_{config_name.upper()}", raising=False)
    reload(config)
    if default is not None:
        assert config.settings[config_name] == default
    else:
        with pytest.raises(KeyError):
            config.settings[config_name]
