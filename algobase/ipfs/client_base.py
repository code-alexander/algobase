"""Abstract base class for IPFS clients."""

from abc import ABC, abstractmethod

from decouple import UndefinedValueError, config

from algobase.choices import IpfsPinStatusChoice, IpfsProviderChoice
from algobase.functional import maybe_bind


class IpfsClient(ABC):
    """Abstract base class for IPFS clients."""

    def __post_init__(self) -> None:
        """If an API key is required, check that it is present."""
        if self.is_api_key_required:
            self.check_api_key_is_present()

    @property
    @abstractmethod
    def ipfs_provider_name(self) -> IpfsProviderChoice:
        """The name of the IPFS provider."""
        ...  # pragma: no cover

    @property
    @abstractmethod
    def api_version(self) -> str:
        """The version of the IPFS provider's API."""
        ...  # pragma: no cover

    @property
    @abstractmethod
    def base_url(self) -> str:
        """The base URL of the IPFS provider's API."""
        ...  # pragma: no cover

    @property
    @abstractmethod
    def is_api_key_required(self) -> bool:
        """Whether the IPFS provider requires an API key."""
        ...  # pragma: no cover

    @property
    def api_key_name(self) -> str:
        """The name of the IPFS provider's API key."""
        return f"{self.ipfs_provider_name.upper()}_API_KEY"

    @property
    def api_key(self) -> str | None:
        """The IPFS provider's API key."""
        return maybe_bind(config(self.api_key_name, default=None), str)

    def check_api_key_is_present(self) -> None:
        """Checks that the IPFS provider's API key is present."""
        if self.is_api_key_required and self.api_key is None:
            raise UndefinedValueError(
                f"`{self.api_key_name}` must be defined in .env file."
            )

    @abstractmethod
    def store_json(self, json: str) -> str | None:
        """Stores JSON data in IPFS.

        Args:
            json (str): The JSON to store.

        Returns:
            str | None: The IPFS CID of the stored data, or None if the data could not be stored.
        """
        ...  # pragma: no cover

    @abstractmethod
    def fetch_pin_status(self, cid: str) -> IpfsPinStatusChoice | None:
        """Returns the pinning status of a file, by CID.

        Args:
            cid (str): The CID of the file to check.

        Returns:
            IpfsPinStatusChoice | None: The pin status of the CID, or None if the status could not be retrieved.
        """
        ...  # pragma: no cover
