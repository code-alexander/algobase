"""Annotated types for Pydantic models."""

from functools import partial
from typing import Annotated

from algosdk.constants import HASH_LEN, MAX_ASSET_DECIMALS
from annotated_types import Ge, Le, Len, Lt
from pydantic import AfterValidator
from pydantic_core import Url

from humblepy.utils.validate import (
    validate_address,
    validate_encoded_length,
)

# Generic types
Uint32 = Annotated[int, Ge(0), Lt(2**32)]
Uint64 = Annotated[int, Ge(0), Lt(2**64)]

# Algorand types
AlgorandHash = Annotated[bytes, Len(HASH_LEN, HASH_LEN)]  # 32 bytes
AlgorandAddress = Annotated[str, AfterValidator(validate_address)]

# Algorand Standard Asset (ASA) types
AsaDecimals = Annotated[Uint32, Ge(0), Le(MAX_ASSET_DECIMALS)]  # <= 19
AsaUnitName = Annotated[
    str, AfterValidator(partial(validate_encoded_length, max_length=8))
]
AsaAssetName = Annotated[
    str, AfterValidator(partial(validate_encoded_length, max_length=32))
]
AsaUrl = Annotated[
    Url,
    AfterValidator(partial(validate_encoded_length, max_length=96)),
]
