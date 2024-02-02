"""Algorand API providers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property
from typing import Literal

import httpx

from algobase.choices import (
    AlgorandApiProvider,
    AlgorandApiProviderChoice,
)
from algobase.config import settings


class AlgorandProvider(ABC):
    """Abstract base class for Algorand API providers."""

    @property
    @abstractmethod
    def provider_name(self) -> AlgorandApiProviderChoice:
        """The name of the Algorand API provider."""
        ...  # pragma: no cover

    @property
    @abstractmethod
    def api_version(self) -> str:
        """The version of the API."""
        ...  # pragma: no cover

    @property
    @abstractmethod
    def credential(self) -> str:
        """The API credential (key or token)."""
        ...  # pragma: no cover

    @property
    @abstractmethod
    def base_url(self) -> httpx.URL:
        """The base URL of the API."""
        ...  # pragma: no cover

    @property
    @abstractmethod
    def algod_url(self) -> httpx.URL:
        """The Algod API base URL."""
        ...  # pragma: no cover

    @property
    @abstractmethod
    def indexer_url(self) -> httpx.URL:
        """The Indexer API base URL."""
        ...  # pragma: no cover

    @property
    @abstractmethod
    def kmd_url(self) -> httpx.URL:
        """The KMD API base URL."""
        ...  # pragma: no cover


@dataclass
class Localhost(AlgorandProvider):
    """Localhost provider."""

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
        """The API credential (key or token)."""
        return str(settings.algod_token)

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
