"""Utilities for minting assets on Algorand with sensible defaults."""

from typing import TypeAlias

from algosdk.transaction import AssetConfigTxn, wait_for_confirmation
from algosdk.v2client.algod import AlgodClient
from returns.pipeline import flow

from algobase.algorand.account import Account
from algobase.choices import Arc
from algobase.functional import maybe_apply
from algobase.models.algod import PendingTransactionResponse
from algobase.models.arc3 import Arc3Metadata, Arc3Properties
from algobase.models.arc19 import Arc19Metadata
from algobase.models.asa import Asa
from algobase.models.asset_params import AssetParams

Arc3NonTraitProperties: TypeAlias = dict[
    str,
    str
    | int
    | float
    | dict[str, "Arc3NonTraitProperties"]
    | list["Arc3NonTraitProperties"],
]


def create_metadata(
    description: str | None = None, properties: Arc3NonTraitProperties | None = None
) -> Arc3Metadata:
    """Create ARC-3 metadata for an NFT.

    Args:
        description (str | None, optional): Description of the NFT. Defaults to None.
        properties (Arc3NonTraitProperties | None, optional): Additional non-trait properties. Defaults to None.

    Returns:
        Arc3Metadata: The ARC-3 metadata.
    """
    return Arc3Metadata(
        arc=Arc.ARC3,
        name="NFT",
        decimals=0,
        description=description,
        properties=maybe_apply(properties, Arc3Properties.model_validate),
    )


def create_metadata_arc19(
    description: str | None = None, properties: Arc3NonTraitProperties | None = None
) -> Arc19Metadata:
    """Create ARC-19 metadata for an NFT.

    Args:
        description (str | None, optional): Description of the NFT. Defaults to None.
        properties (Arc3NonTraitProperties | None, optional): Additional non-trait properties. Defaults to None.

    Returns:
        Arc19Metadata: The ARC-3 metadata.
    """
    return Arc19Metadata(
        arc=Arc.ARC19,
        arc3_metadata=Arc3Metadata(
            arc=Arc.ARC3,
            name="NFT",
            decimals=0,
            description=description,
            properties=maybe_apply(properties, Arc3Properties.model_validate),
        ),
    )


def create_asa(metadata: Arc3Metadata | Arc19Metadata, cid: str) -> Asa:
    """Creates an instance of the `Asa` model.

    Args:
        metadata (Arc3Metadata | Arc19Metadata): The ARC-3 or ARC-19 metadata.
        cid (str): The IPFS CID for the metadata.

    Returns:
        Asa: The `Asa` instance.
    """
    return Asa(
        asset_params=AssetParams(
            total=1,
            decimals=0,
            unit_name="NFT",
            asset_name="NFT",
            url=f"ipfs://{cid}/#arc3",
        ),
        metadata=metadata,
    )


def create_asset_config_txn(
    algod_client: AlgodClient, account: Account, asa: Asa
) -> AssetConfigTxn:
    """Create an AssetConfigTxn for the given account and ASA.

    Args:
        algod_client (AlgodClient): The AlgodClient instance.
        account (Account): The account to use.
        asa (Asa): The ASA to mint.

    Returns:
        AssetConfigTxn: The AssetConfigTxn instance.
    """
    return AssetConfigTxn(
        sender=account.address,
        sp=algod_client.suggested_params(),
        index=None,
        total=asa.asset_params.total,
        default_frozen=False,
        unit_name=asa.asset_params.unit_name,
        asset_name=asa.asset_params.asset_name,
        manager=account.address,
        reserve=account.address,
        freeze=None,
        clawback=None,
        url=asa.asset_params.url,
        metadata_hash=asa.metadata_hash,
        note=None,
        lease=None,
        strict_empty_address_check=False,
        decimals=asa.asset_params.decimals,
        rekey_to=None,
    )


def mint(
    algod_client: AlgodClient, account: Account, metadata: Arc3Metadata, cid: str
) -> int | None:
    """Mint an NFT on Algorand.

    Args:
        algod_client (AlgodClient): The Algod client.
        account (Account): The account to use.
        metadata (Arc3Metadata): The ARC-3 metadata.
        cid (str): The IPFS CID for the metadata.

    Returns:
        int | None: The asset ID if minted, else None.
    """
    return flow(
        create_asa(metadata, cid),
        lambda asa: create_asset_config_txn(algod_client, account, asa).sign(
            account.private_key
        ),
        algod_client.send_transaction,
        lambda txid: wait_for_confirmation(algod_client, txid, 4),
        PendingTransactionResponse.model_validate,
        lambda response: response.asset_index,
    )
