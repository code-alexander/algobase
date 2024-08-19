"""A Pydantic model for Algorand Standard Asset parameters."""

from typing import Self

from algosdk.v2client.algod import AlgodClient
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from algobase.models.algod import Asset
from algobase.types.annotated import (
    AlgorandAddress,
    AlgorandHash,
    AsaAssetName,
    AsaDecimals,
    AsaUnitName,
    AsaUrl,
    Uint64,
)


class AssetParams(BaseModel):
    """A Pydantic model for Algorand Standard Assets (ASAs)."""

    model_config = ConfigDict(frozen=True)

    total: Uint64 = Field(
        description="The total number of base units of the asset to create."
    )
    decimals: AsaDecimals = Field(
        default=0,
        description="The number of digits to use after the decimal point when displaying the asset. If 0, the asset is not divisible. If 1, the base unit of the asset is in tenths. Must be between 0 and 19, inclusive.",
    )
    default_frozen: bool = Field(
        default=False,
        description="Whether slots for this asset in user accounts are frozen by default.",
    )
    unit_name: AsaUnitName | None = Field(
        default=None,
        description="The name of a unit of this asset. Max size is 8 bytes. Example: 'USDT'.",
    )
    asset_name: AsaAssetName | None = Field(
        default=None,
        description="The name of the asset. Max size is 32 bytes. Example: 'Tether'.",
    )
    url: AsaUrl | None = Field(
        default=None,
        description="Specifies a URL where more information about the asset can be retrieved. Max size is 96 bytes.",
    )
    metadata_hash: AlgorandHash | None = Field(
        default=None,
        description="This field is intended to be a 32-byte hash of some metadata that is relevant to your asset and/or asset holders.",
    )
    manager: AlgorandAddress | None = Field(
        default=None,
        description="The address of the account that can manage the configuration of the asset and destroy it.",
    )
    reserve: AlgorandAddress | None = Field(
        default=None,
        description="The address of the account that holds the reserve (non-minted) units of the asset.",
    )
    freeze: AlgorandAddress | None = Field(
        default=None,
        description="The address of the account used to freeze holdings of this asset. If empty, freezing is not permitted.",
    )
    clawback: AlgorandAddress | None = Field(
        default=None,
        description="The address of the account that can clawback holdings of this asset. If empty, clawback is not permitted.",
    )

    @classmethod
    def from_algod(cls, algod_client: AlgodClient, asset_id: Uint64) -> Self:
        """Constructs an instance by fetching asset params from Algod.

        Args:
            algod_client (AlgodClient): The Algod client.
            asset_id (Uint64): The asset ID to search for.

        Returns:
            Self: The `AssetParams` instance.
        """
        if asset_id:
            asset = Asset.model_validate(algod_client.asset_info(asset_id))
            return cls.model_validate(asset.params.model_dump())
        return cls(
            total=10_000_000_000,
            decimals=6,
            default_frozen=False,
            unit_name="ALGO",
            asset_name="ALGO",
            url="https://www.algorand.foundation",
            metadata_hash=None,
            manager=None,
            reserve=None,
            freeze=None,
            clawback=None,
        )
