"""IPFS client for nft.storage."""

from dataclasses import dataclass
from urllib.parse import urljoin

import httpx

from algobase.choices import IpfsProvider, IpfsProviderChoice
from algobase.ipfs.client_base import IpfsClient


@dataclass
class NftStorage(IpfsClient):
    """IPFS client for nft.storage."""

    @property
    def ipfs_provider_name(self) -> IpfsProviderChoice:
        """The name of the IPFS provider."""
        return IpfsProvider.NFT_STORAGE

    @property
    def api_version(self) -> str:
        """The version of the IPFS provider's API."""
        return "1.0"

    @property
    def base_url(self) -> str:
        """The base URL of the IPFS provider's API."""
        return "https://api.nft.storage"

    @property
    def is_api_key_required(self) -> bool:
        """Whether the IPFS provider requires an API key."""
        return True

    def store_json(self, json: str) -> str | None:
        """Stores JSON data in IPFS.

        Args:
            json (str): The JSON to store.

        Returns:
            str | None: The IPFS CID of the stored data, or None if the data could not be stored.
        """
        with httpx.Client() as client:
            try:
                response = client.post(url=urljoin(self.base_url, "upload"), json=json)
                data = response.json()
                response.raise_for_status()
                if (
                    data.get("ok") is True
                    and (cid := data.get("value").get("cid")) is not None
                ):
                    return str(cid)
            except httpx.HTTPError as e:
                raise httpx.HTTPError(
                    f"HTTP Exception for {e.request.url}: {e}. Provider error: {data.get('error').get('message')}"
                )
            else:
                raise httpx.HTTPError(
                    f"Failed to store JSON in IPFS using {self.ipfs_provider_name}."
                )
