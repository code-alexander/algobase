"""Algorand TestNet dispenser client."""

from dataclasses import dataclass, field
from typing import Literal, Self

import httpx

from algobase.choices import AlgorandAsset
from algobase.models.dispenser import DispenserFundResponse
from algobase.settings import Settings


@dataclass(frozen=True, slots=True)
class Dispenser:
    """Algorand TestNet dispenser client."""

    _access_token: str = field(repr=False)

    def __post_init__(self):
        """Check that the access token is not None or an empty string.

        Raises:
            ValueError: If the access token is None or an empty string.
        """
        if not self._access_token:
            raise ValueError("Access token is required.")

    @classmethod
    def from_settings(cls, settings: Settings) -> Self:
        """Create an instance of the IPFS client from the settings object.

        Args:
            settings (Settings): The settings object.

        Raises:
            ValueError: If the dispenser access token is None.

        Returns:
            Self: An instance of the Dispenser client.
        """
        if settings.testnet_dispenser_access_token is None:
            raise ValueError("Dispenser access token must not be None.")
        return cls(_access_token=settings.testnet_dispenser_access_token)

    @property
    def base_url(self) -> httpx.URL:
        """The base URL of the dispenser API."""
        return httpx.URL("https://api.dispenser.algorandfoundation.tools")

    @property
    def access_token(self) -> str:
        """The OAauth access token."""
        return self._access_token

    @property
    def headers(self) -> dict[str, str]:
        """The headers to use for the HTTP requests."""
        return {"Authorization": f"Bearer {self.access_token}"}

    def fund(
        self, address: str, amount: int, asset_id: Literal[AlgorandAsset.ALGO]
    ) -> DispenserFundResponse:
        """Funds an account from the TestNet dispenser.

        Args:
            address (str): The address of the account to fund.
            amount (int): The amount to fund the account with.
            asset_id (Literal[AlgorandAsset.ALGO]): The asset ID.

        Raises:
            httpx.HTTPError: If the request was unsuccessful.

        Returns:
            DispenserFundResponse: The transaction ID and amount funded.
        """
        with httpx.Client() as client:
            response = client.post(
                url=self.base_url.join(f"fund/{asset_id}"),
                json={"receiver": address, "amount": amount, "assetID": asset_id},
                headers=self.headers,
                timeout=15,
            )
            data = response.json()
            if response.status_code == httpx.codes.OK:
                return DispenserFundResponse.model_validate(data)
            else:
                raise httpx.HTTPError(
                    f"HTTP {response.status_code} error: Failed to fund account {address} with amount {amount} of asset {asset_id}.",
                )
