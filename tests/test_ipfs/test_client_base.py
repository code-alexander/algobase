"""Tests the IpfsClient abstract base class."""

from dataclasses import dataclass

import pytest
from _pytest.monkeypatch import MonkeyPatch
from decouple import UndefinedValueError

from algobase.choices import IpfsProvider, IpfsProviderChoice
from algobase.ipfs.client_base import IpfsClient


class TestIpfsClient:
    """Tests the IpfsClient abstract base class."""

    @dataclass
    class Client(IpfsClient):
        """Concrete implementation of the IpfsClient abstract base class."""

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
            return "some_cid"

    @pytest.mark.parametrize(
        "attribute, value",
        [
            ("api_version", "1.0"),
            ("base_url", "https://api.nft.storage"),
            ("is_api_key_required", True),
            ("ipfs_provider_name", IpfsProvider.NFT_STORAGE),
            ("api_key_name", "NFT_STORAGE_API_KEY"),
        ],
    )
    def test_properties(
        self,
        monkeypatch: MonkeyPatch,
        attribute: str,
        value: str | bool | IpfsProviderChoice,
    ) -> None:
        """Test that the client has the required abstract properties."""
        monkeypatch.setenv("NFT_STORAGE_API_KEY", "SOME_API_KEY")
        client = self.Client()
        assert getattr(client, attribute) == value

    def test_api_key_missing(self, monkeypatch: MonkeyPatch) -> None:
        """Test that the client raises an error if the API key is missing."""
        monkeypatch.delenv("NFT_STORAGE_API_KEY", raising=False)
        with pytest.raises(UndefinedValueError):
            self.Client()
