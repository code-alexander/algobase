"""Algorand base client."""

from dataclasses import dataclass, field

from algosdk.v2client.algod import AlgodClient

from algobase.algorand.providers import AlgorandProvider, Localhost
from algobase.choices import AlgorandNetworkChoice
from algobase.config import settings


@dataclass
class AlgorandClient:
    """Algorand base client."""

    network: AlgorandNetworkChoice = settings.algorand_network

    provider: AlgorandProvider = field(default_factory=Localhost)

    def __post_init__(self) -> None:
        """Instantiate algosdk clients."""
        self.algod = AlgodClient(
            algod_token=self.provider.credential,
            algod_address=str(self.provider.algod_url),
        )
