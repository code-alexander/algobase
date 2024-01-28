"""Annotated types for Pydantic models."""

from functools import partial
from typing import Annotated, Union

from algosdk.constants import HASH_LEN, MAX_ASSET_DECIMALS
from annotated_types import Ge, Gt, Le, Len, Lt
from cytoolz import compose
from pydantic import AfterValidator, UrlConstraints
from pydantic_core import Url
from typing_extensions import TypeAliasType

from algobase.utils.url import decode_url_braces
from algobase.utils.validate import (
    validate_address,
    validate_arc3_sri,
    validate_base64,
    validate_contains_substring,
    validate_encoded_length,
    validate_hex,
    validate_is_power_of_10,
    validate_locale,
    validate_mime_type,
    validate_not_in,
    validate_not_ipfs_gateway,
    validate_type_compatibility,
)

# Generic types
Uint32 = Annotated[int, Ge(0), Lt(2**32)]
Uint64 = Annotated[int, Ge(0), Lt(2**64)]
Base64Str = Annotated[str, AfterValidator(validate_base64)]


# World Wide Web Consortium (W3C) types
MimeType = Annotated[
    str, AfterValidator(partial(validate_mime_type, primary_type=None))
]
ImageMimeType = Annotated[
    str, AfterValidator(partial(validate_mime_type, primary_type="image"))
]

# Unicode Common Locale Data Repository (CLDR) types
UnicodeLocale = Annotated[str, AfterValidator(validate_locale)]

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
    str,
    AfterValidator(
        compose(
            partial(validate_encoded_length, max_length=96),
            decode_url_braces,
            partial(validate_type_compatibility, _type=Url),
        )
    ),
]
AsaFractionalNftTotal = Annotated[
    Uint64, Gt(1), AfterValidator(validate_is_power_of_10)
]

# Algorand ARC-16 types
Arc16Traits = dict[str, str | int]

# Algorand ARC-3 types
Arc3Url = Annotated[
    str,
    AfterValidator(
        compose(
            partial(validate_encoded_length, max_length=96),
            decode_url_braces,
            validate_not_ipfs_gateway,
            partial(
                validate_type_compatibility,
                _type=Annotated[Url, UrlConstraints(allowed_schemes=["https", "ipfs"])],
            ),
        )
    ),
]
Arc3LocalizedUrl = Annotated[
    str,
    AfterValidator(
        compose(
            partial(validate_encoded_length, max_length=96),
            partial(validate_contains_substring, substring="{locale}"),
            decode_url_braces,
            validate_not_ipfs_gateway,
            partial(
                validate_type_compatibility,
                _type=Annotated[Url, UrlConstraints(allowed_schemes=["https", "ipfs"])],
            ),
        )
    ),
]
Arc3Sri = Annotated[str, AfterValidator(validate_arc3_sri)]
Arc3Color = Annotated[str, Len(6, 6), AfterValidator(validate_hex)]
Arc3NonTraitProperties = TypeAliasType(
    "Arc3NonTraitProperties",
    Annotated[
        dict[
            str,
            Union[
                str,
                int,
                float,
                list[Union[str, int, float, "Arc3NonTraitProperties"]],  # type: ignore
                "Arc3NonTraitProperties",  # type: ignore
            ],
        ],
        AfterValidator(partial(validate_not_in, element="traits")),
    ],
)
