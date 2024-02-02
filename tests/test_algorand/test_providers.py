"""Test the Algorand API providers."""

from dataclasses import dataclass
from functools import cached_property
from typing import Literal

import httpx
import pytest

from algobase.algorand.providers import AlgorandProvider, Localhost
from algobase.choices import (
    AlgorandApiProvider,
    AlgorandApiProviderChoice,
)


class TestAlgorandProvider:
    """Test the AlgorandProvider abstract base class."""

    @dataclass
    class Provider(AlgorandProvider):
        """Concrete implementation of the AlgorandProvider abstract base class."""

        @property
        def provider_name(self) -> Literal[AlgorandApiProvider.LOCALHOST]:
            """The name of the Algorand API provider."""
            return AlgorandApiProvider.LOCALHOST

        @property
        def api_version(self) -> str:
            """The version of the API."""
            return "0"

        @property
        def credential(self) -> str:
            """The API credential."""
            return "a" * 64

        @property
        def base_url(self) -> httpx.URL:
            """The base URL of the API."""
            return httpx.URL("http://localhost")

        @cached_property
        def algod_url(self) -> httpx.URL:
            """The Algod API base URL."""
            return self.base_url.copy_with(port=4001)

        @cached_property
        def indexer_url(self) -> httpx.URL:
            """The Indexer API base URL."""
            return self.base_url.copy_with(port=8980)

        @cached_property
        def kmd_url(self) -> httpx.URL:
            """The KMD API base URL."""
            return self.base_url.copy_with(port=4002)

    @pytest.mark.parametrize(
        "attribute, value",
        [
            ("provider_name", "localhost"),
            ("api_version", "0"),
            ("credential", "a" * 64),
            ("base_url", httpx.URL("http://localhost")),
            ("algod_url", httpx.URL("http://localhost:4001")),
            ("indexer_url", httpx.URL("http://localhost:8980")),
            ("kmd_url", httpx.URL("http://localhost:4002")),
        ],
    )
    def test_properties(
        self,
        attribute: str,
        value: str | bool | AlgorandApiProviderChoice,
    ) -> None:
        """Test that the provider has the required abstract properties."""
        provider = self.Provider()
        assert getattr(provider, attribute) == value


class TestLocalhost:
    """Tests the Localhost provider."""

    provider = Localhost()

    @pytest.mark.parametrize(
        "attribute, value",
        [
            ("provider_name", "localhost"),
            ("api_version", "0"),
            ("credential", "a" * 64),
            ("base_url", httpx.URL("http://localhost")),
            ("algod_url", httpx.URL("http://localhost:4001")),
            ("indexer_url", httpx.URL("http://localhost:8980")),
            ("kmd_url", httpx.URL("http://localhost:4002")),
        ],
    )
    def test_properties(
        self,
        attribute: str,
        value: str | bool | AlgorandApiProviderChoice,
    ) -> None:
        """Test that the provider has the required abstract properties."""
        assert getattr(self.provider, attribute) == value
