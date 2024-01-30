"""IPFS client for nft.storage."""

from dataclasses import dataclass
from urllib.parse import urljoin

import httpx

from algobase.choices import (
    IpfsPinStatus,
    IpfsPinStatusChoice,
    IpfsProvider,
    IpfsProviderChoice,
)
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
            response = client.post(url=urljoin(self.base_url, "upload"), json=json)
            data = response.json()
            if response.status_code == httpx.codes.OK:
                if (
                    data.get("ok") is True
                    and (cid := data.get("value").get("cid")) is not None
                ):
                    return str(cid)
                else:
                    raise httpx.HTTPError(
                        f"HTTP Exception for {response.request.url}: Failed to store JSON in IPFS using {self.ipfs_provider_name}."
                    )
            else:
                raise httpx.HTTPError(
                    f"HTTP Exception for {response.request.url}: {response.status_code} {data.get('error').get('message')}"
                )

    def fetch_pin_status(self, cid: str) -> IpfsPinStatusChoice | None:
        """Returns the pinning status of a file, by CID.

        Args:
            cid (str): The CID of the file to check.

        Returns:
            IpfsPinStatusChoice | None: The pin status of the CID, or None if the status could not be retrieved.
        """
        with httpx.Client() as client:
            response = client.get(
                url=urljoin(self.base_url, "check"),
                params={"cid": cid},
            )
            data = response.json()
            if response.status_code == httpx.codes.OK:
                pin_status = data.get("value").get("pin").get("status")
                if (
                    data.get("ok") is True
                    and pin_status is not None
                    and hasattr(IpfsPinStatus, str(pin_status).upper())
                ):
                    return IpfsPinStatus(pin_status)
                else:
                    raise httpx.HTTPError(
                        f"HTTP Exception for {response.request.url}: {pin_status} is not a valid pin status."
                    )
            else:
                raise httpx.HTTPError(
                    f"HTTP Exception for {response.request.url}: {response.status_code} {data.get('error').get('message')}"
                )
