"""Classes and functions to configure and create Algorand API clients."""

from dataclasses import dataclass

from algosdk.kmd import KMDClient
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from algobase.choices import AlgorandApi, AlgorandApiChoice
from algobase.functional import pipe


@dataclass(frozen=True, slots=True)
class ClientConfig:
    """Configuration for an Algorand API client."""

    url: str
    credential: str
    headers: dict[str, str] | None = None


def create_algod_client(config: ClientConfig) -> AlgodClient:
    """Create an AlgodClient instance from the given configuration.

    Args:
        config (ClientConfig): The configuration to use.

    Returns:
        AlgodClient: The AlgodClient instance.
    """
    return AlgodClient(
        algod_token=config.credential, algod_address=config.url, headers=config.headers
    )


def create_indexer_client(config: ClientConfig) -> IndexerClient:
    """Create an IndexerClient instance from the given configuration.

    Args:
        config (ClientConfig): The configuration to use.

    Returns:
        IndexerClient: The IndexerClient instance.
    """
    return IndexerClient(
        indexer_token=config.credential,
        indexer_address=config.url,
        headers=config.headers,
    )


def create_kmd_client(config: ClientConfig) -> KMDClient:
    """Create a KMDClient instance from the given configuration.

    Args:
        config (ClientConfig): The configuration to use.

    Returns:
        KMDClient: The KMDClient instance.
    """
    return KMDClient(kmd_token=config.credential, kmd_address=config.url)


def create_localnet_default_config(api: AlgorandApiChoice) -> ClientConfig:
    """Create a default configuration for the localnet.

    Args:
        api (AlgorandApiChoice): The API to configure.

    Returns:
        ClientConfig: The default configuration.
    """
    port = {AlgorandApi.ALGOD: 4001, AlgorandApi.INDEXER: 8980, AlgorandApi.KMD: 7833}[
        api
    ]
    return ClientConfig(url=f"http://localhost:{port}", credential="a" * 64)


def create_localnet_algod_client() -> AlgodClient:
    """Create an AlgodClient instance for the localnet.

    Returns:
        AlgodClient: The AlgodClient instance.
    """
    return pipe(AlgorandApi.ALGOD, create_localnet_default_config, create_algod_client)


def create_localnet_indexer_client() -> IndexerClient:
    """Create an IndexerClient instance for the localnet.

    Returns:
        IndexerClient: The IndexerClient instance.
    """
    return pipe(
        AlgorandApi.INDEXER, create_localnet_default_config, create_indexer_client
    )


def create_localnet_kmd_client() -> KMDClient:
    """Create a KMDClient instance for the localnet.

    Returns:
        KMDClient: The KMDClient instance.
    """
    return pipe(AlgorandApi.KMD, create_localnet_default_config, create_kmd_client)
