"""Classes and functions to configure and create Algorand API clients."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from algosdk.kmd import KMDClient
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from returns.curry import partial
from returns.pipeline import flow

from algobase.algorand.account import Account
from algobase.choices import (
    AlgorandApi,
    AlgorandApiChoice,
    AlgorandNetwork,
)
from algobase.functional import first_true
from algobase.models import algod, kmd


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
    port = {AlgorandApi.ALGOD: 4001, AlgorandApi.INDEXER: 8980, AlgorandApi.KMD: 4002}[
        api
    ]
    return ClientConfig(url=f"http://localhost:{port}", credential="a" * 64)


def create_localnet_algod_client() -> AlgodClient:
    """Create an AlgodClient instance for the localnet.

    Returns:
        AlgodClient: The AlgodClient instance.
    """
    return flow(AlgorandApi.ALGOD, create_localnet_default_config, create_algod_client)


def create_localnet_indexer_client() -> IndexerClient:
    """Create an IndexerClient instance for the localnet.

    Returns:
        IndexerClient: The IndexerClient instance.
    """
    return flow(
        AlgorandApi.INDEXER, create_localnet_default_config, create_indexer_client
    )


def create_localnet_kmd_client() -> KMDClient:
    """Create a KMDClient instance for the localnet.

    Returns:
        KMDClient: The KMDClient instance.
    """
    return flow(AlgorandApi.KMD, create_localnet_default_config, create_kmd_client)


def find_wallet_id(kmd_client: KMDClient, wallet_name: str) -> str | None:
    """Get the ID of a wallet from the KMD client.

    Args:
        kmd_client (KMDClient): The KMD client.
        wallet_name (str): The name of the wallet.

    Returns:
        str | None: The ID of the wallet if found, else None.
    """
    return next(
        x.id
        for x in map(kmd.APIV1Wallet.model_validate, kmd_client.list_wallets())
        if x.name == wallet_name
    )


def is_default_account(account: algod.Account) -> bool:
    """Check if an account is the default account.

    Args:
        account (AlgodResponseType): The account info.

    Returns:
        bool: True if the account is the default account, else False.
    """
    return account.status != "Offline" and account.amount > 1_000_000_000


def match_account(
    algod_client: AlgodClient,
    addresses: list[str],
    predicate: Callable[[algod.Account], bool],
) -> str:
    """Find the first account that matches the predicate, given a list of addresses to lookup.

    Args:
        algod_client (AlgodClient): The Algod client.
        addresses (list[str]): The addresses to check.
        predicate (Callable[[algod.Account], bool]): The predicate function.

    Raises:
        ValueError: If no account is found where predicate(account) is True.

    Returns:
        str: The address of the matching account if found, else None.
    """
    matched = first_true(
        addresses,
        predicate=lambda x: flow(
            x, algod_client.account_info, algod.Account.model_validate, predicate
        ),
    )
    if matched is None:
        raise ValueError("No account found.")
    return matched


def get_default_account(
    algod_client: AlgodClient, kmd_client: KMDClient | None = None
) -> Account:
    """Return an Account instance for the default account.

    Args:
        algod_client (AlgodClient): The Algod client.
        kmd_client (KMDClient | None, optional): The KMD client. If None, a default instance will be created. Defaults to None.

    Raises:
        ValueError: If the Algod client instance isn't connected to a localnet network.

    Returns:
        Account: The default account.
    """
    if not is_localnet(algod_client):
        raise ValueError("Algod client must be connected to a localnet network.")

    kmd_client = kmd_client or create_localnet_kmd_client()

    wallet_handle = kmd_client.init_wallet_handle(
        find_wallet_id(kmd_client, "unencrypted-default-wallet"), ""
    )

    return flow(
        wallet_handle,
        kmd_client.list_keys,
        lambda keys: match_account(algod_client, keys, is_default_account),
        partial(kmd_client.export_key, wallet_handle, ""),
        Account.from_private_key,
    )


def is_localnet(algod_client: AlgodClient) -> bool:
    """Check if the AlgodClient is connected to a localnet.

    Args:
        algod_client (AlgodClient): The AlgodClient instance.

    Returns:
        bool: True if the client is connected to a localnet, else False.
    """
    return algod_client.suggested_params().gen in {
        "devnet-v1",
        "sandnet-v1",
        "dockernet-v1",
    }


def get_algonode_config(
    network: Literal[
        AlgorandNetwork.BETANET, AlgorandNetwork.TESTNET, AlgorandNetwork.MAINNET
    ],
    api: Literal[AlgorandApi.ALGOD, AlgorandApi.INDEXER],
) -> ClientConfig:
    """Get the client config for Algonode API.

    Args:
        network (AlgorandNetworkChoice): The Algorand network.
        api (Literal[AlgorandApi.ALGOD, AlgorandApi.INDEXER]): The Algorand API.

    Returns:
        ClientConfig: The client config object.
    """
    return ClientConfig(
        url=f"https://{network}-{('idx', 'api')[api == AlgorandApi.ALGOD]}.algonode.cloud",
        credential="",
    )
