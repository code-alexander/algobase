"""Algorand TestNet dispenser client."""

from dataclasses import dataclass, field
from typing import Literal

import httpx

from algobase.choices import AlgorandAsset
from algobase.models.dispenser import DispenserFundResponse


@dataclass
class Dispenser:
    """Algorand TestNet dispenser client."""

    _api_key: str = field(repr=False)

    @property
    def base_url(self) -> httpx.URL:
        """The base URL of the dispenser API."""
        return httpx.URL("https://api.dispenser.algorandfoundation.tools")

    @property
    def is_api_key_required(self) -> bool:
        """Whether the IPFS provider requires an API key."""
        return True

    @property
    def api_key(self) -> str:
        """The API key."""
        return self._api_key

    @property
    def headers(self) -> dict[str, str]:
        """The headers to use for the HTTP requests."""
        return {"Authorization": f"Bearer {self.api_key}"}

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
