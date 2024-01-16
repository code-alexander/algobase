"""Pydantic models for Algorand Standard Asset (ASA) NFTs."""

import math
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from humblepy.types.annotated import AsaFractionalNftTotal, Uint64


class NftType(StrEnum):
    """An enumeration of Algorand Standard Asset (ASA) NFT types."""

    pure = "pure"
    fractional = "fractional"


class PureNft(BaseModel):
    """A Pydantic model for Algorand Standard Asset (ASA) pure NFTs.

    An ASA is said to be a pure NFT if and only if it has the following properties:
    - Total Number of Units (t) MUST be 1.
    - Number of Digits after the Decimal Point (dc) MUST be 0.
    """

    nft_type: Literal[NftType.pure] = Field(
        default=NftType.pure,
        description="The type of NFT. Must be 'pure' for a pure NFT.",
        exclude=True,
        frozen=True,
    )
    total: Literal[1] = Field(
        default=1,
        description="Total number of units must be 1 for a pure NFT.",
        frozen=True,
    )
    decimals: Literal[0] = Field(
        default=0,
        description="Number of digits after the decimal point must be 0 for a pure NFT.",
        frozen=True,
    )


class FractionalNft(BaseModel):
    """A Pydantic model for Algorand Standard Asset (ASA) fractional NFTs.

    An ASA is said to be a fractional NFT if and only if it has the following properties:
    - Total Number of Units (t) MUST be a power of 10 larger than 1: 10, 100, 1000, …
    - Number of Digits after the Decimal Point (dc) MUST be equal to the logarithm in base 10 of total number of units.
    """

    nft_type: Literal[NftType.fractional] = Field(
        default=NftType.fractional,
        description="The type of NFT. Must be 'fractional' for a fractional NFT.",
        exclude=True,
        frozen=True,
    )
    total: AsaFractionalNftTotal = Field(
        description="Total number of units must be a power of 10 greater than 1, for a fractional NFT.",
        frozen=True,
    )
    decimals: Uint64 = Field(
        description="Number of digits after the decimal point must be equal to the logarithm in base 10 of total number of units, for a fractional NFT.",
        frozen=True,
    )

    @model_validator(mode="after")
    def check_decimal_places(self) -> "FractionalNft":
        """Checks that the number of digits after the decimal point is equal to the logarithm in base 10 of total number of units.

        Raises:
            ValueError: If the the number of digits after the decimal point is not equal to the logarithm in base 10 of total number of units.

        Returns:
            FractionalNft: The class instance.
        """
        if not self.decimals == (log := math.log10(self.total)):
            raise ValueError(
                f"""Number of digits after the decimal point must be equal to the logarithm in base 10 of total number of units. In other words, the total supply of the ASA must be exactly 1.
                    Hint: If the total number of units is {self.total}, then the number of digits after the decimal point must be {int(log)}.
                """
            )
        return self
