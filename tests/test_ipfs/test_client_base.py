"""Tests the IpfsClient abstract base class."""

from dataclasses import dataclass
from typing import Self

import httpx
import pytest

from algobase.choices import (
    IpfsPinStatus,
    IpfsPinStatusChoice,
    IpfsProvider,
    IpfsProviderChoice,
)
from algobase.ipfs.client_base import IpfsClient
from algobase.settings import Settings


class TestIpfsClient:
    """Tests the IpfsClient abstract base class."""

    @dataclass
    class Client(IpfsClient):
        """Concrete implementation of the IpfsClient abstract base class."""

        @classmethod
        def from_settings(cls, settings: Settings) -> Self:
            """Create an instance of the IPFS client from a settings object."""
            return cls()

        @property
        def ipfs_provider_name(self) -> IpfsProviderChoice:
            """The name of the IPFS provider."""
            return IpfsProvider.NFT_STORAGE

        @property
        def api_version(self) -> str:
            """The version of the IPFS provider's API."""
            return "1.0"

        @property
        def base_url(self) -> httpx.URL:
            """The base URL of the IPFS provider's API."""
            return httpx.URL("https://api.nft.storage")

        @property
        def is_api_key_required(self) -> bool:
            """Whether the IPFS provider requires an API key."""
            return True

        @property
        def api_key(self) -> str | None:
            """The API key."""
            return "test_api_key"

        def store_json(self, json: str | bytes) -> str:
            """Stores JSON data in IPFS.

            Args:
                json (str | bytes): The JSON to store.

            Returns:
                str: The IPFS CID of the stored data.
            """
            return "some_cid"

        def fetch_pin_status(self, cid: str) -> IpfsPinStatusChoice:
            """Returns the pinning status of a file, by CID.

            Args:
                cid (str): The CID of the file to check.

            Returns:
                IpfsPinStatusChoice: The status of the CID.
            """
            return IpfsPinStatus.PINNED

    @pytest.mark.parametrize(
        "attribute, value",
        [
            ("api_version", "1.0"),
            ("base_url", "https://api.nft.storage"),
            ("is_api_key_required", True),
            ("ipfs_provider_name", IpfsProvider.NFT_STORAGE),
            ("api_key", "test_api_key"),
        ],
    )
    def test_properties(
        self,
        attribute: str,
        value: str | bool | IpfsProviderChoice,
    ) -> None:
        """Test that the client has the required abstract properties."""
        client = self.Client()
        assert getattr(client, attribute) == value

    def test_api_key_missing(self) -> None:
        """Test that the client raises an error if the API key is missing."""

        class Missing(self.Client):  # type: ignore
            api_key = None

        with pytest.raises(ValueError):
            Missing()
