"""Pydantic models for Algorand ARC-3 metadata.

Reference: https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0003.md
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from algobase.choices import Arc
from algobase.types.annotated import (
    Arc3Color,
    Arc3LocalizedUrl,
    Arc3Sri,
    Arc3Url,
    Arc16Traits,
    AsaDecimals,
    Base64Str,
    ImageMimeType,
    MimeType,
    UnicodeLocale,
)


class Arc3Localization(BaseModel):
    """A Pydantic model for Algorand ARC-3 localization."""

    model_config = ConfigDict(frozen=True)

    uri: Arc3LocalizedUrl = Field(
        description="The URI pattern to fetch localized data from. This URI should contain the substring `{locale}` which will be replaced with the appropriate locale value before sending the request."
    )
    default: UnicodeLocale = Field(
        description="The locale of the default data within the base JSON."
    )
    locales: list[UnicodeLocale] = Field(
        description="The list of locales for which data is available. These locales should conform to those defined in the Unicode Common UnicodeLocale Data Repository (http://cldr.unicode.org/)."
    )
    integrity: dict[UnicodeLocale, Arc3Sri] | None = Field(
        default=None,
        description="The SHA-256 digests of the localized JSON files (except the default one). The field name is the locale. The field value is a single SHA-256 integrity metadata as defined in the W3C subresource integrity specification (https://w3c.github.io/webappsec-subresource-integrity).",
    )


class Arc3Properties(BaseModel):
    """A Pydantic model for Algorand ARC-3 properties.

    If the `traits` property is present, it must comply with ARC-16: https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0016.md
    """

    model_config = ConfigDict(frozen=True, extra="allow")

    # Struggling to get recursive type definition working here.
    # Have defined `Arc3NonTraitProperties` in algobase/types/annotated.py
    # but it doesn't work as an annotation for __pydantic_extra__.
    __pydantic_extra__: dict[str, str | int | float | dict | list]  # type: ignore

    traits: Arc16Traits | None = Field(
        default=None,
        description="Traits (attributes) that can be used to calculate things like rarity. Values may be strings or numbers.",
    )


class Arc3Metadata(BaseModel):
    """A Pydantic model for Algorand ARC-3 metadata."""

    model_config = ConfigDict(frozen=True)

    arc: Literal[Arc.ARC3] = Field(
        default=Arc.ARC3,
        description="Name of the Algorand ARC standard that the NFT metadata adheres to.",
        exclude=True,
    )

    @property
    def json_str(self) -> str:
        """Returns the model JSON as a string."""
        return self.model_dump_json(exclude_none=True, indent=4)

    @property
    def json_bytes(self, encoding: Literal["utf-8"] = "utf-8") -> bytes:
        """Returns the model JSON encoded as bytes.

        Currently only officially supports UTF-8 encoding.
        """
        return self.json_str.encode(encoding)

    name: str | None = Field(
        default=None, description="Identifies the asset to which this token represents."
    )
    decimals: AsaDecimals | None = Field(
        default=None,
        description="The number of decimal places that the token amount should display - e.g. 18, means to divide the token amount by 1000000000000000000 to get its user representation.",
    )
    description: str | None = Field(
        default=None, description="Describes the asset to which this token represents."
    )
    image: Arc3Url | None = Field(
        default=None,
        description="A URI pointing to a file with MIME type image/* representing the asset to which this token represents. Consider making any images at a width between 320 and 1080 pixels and aspect ratio between 1.91:1 and 4:5 inclusive.",
    )
    image_integrity: Arc3Sri | None = Field(
        default=None,
        description="The SHA-256 digest of the file pointed by the URI image. The field value is a single SHA-256 integrity metadata as defined in the W3C subresource integrity specification (https://w3c.github.io/webappsec-subresource-integrity).",
    )
    image_mimetype: ImageMimeType | None = Field(
        default=None,
        description="The MIME type of the file pointed by the URI image. MUST be of the form 'image/*'.",
    )
    background_color: Arc3Color | None = Field(
        default=None,
        description="Background color do display the asset. MUST be a six-character hexadecimal without a pre-pended #.",
    )
    external_url: Arc3Url | None = Field(
        default=None,
        description="A URI pointing to an external website presenting the asset.",
    )
    external_url_integrity: Arc3Sri | None = Field(
        default=None,
        description="The SHA-256 digest of the file pointed by the URI external_url. The field value is a single SHA-256 integrity metadata as defined in the W3C subresource integrity specification (https://w3c.github.io/webappsec-subresource-integrity).",
    )
    external_url_mimetype: Literal["text/html"] | None = Field(
        default=None,
        description="The MIME type of the file pointed by the URI external_url. It is expected to be 'text/html' in almost all cases.",
    )
    animation_url: Arc3Url | None = Field(
        default=None,
        description="A URI pointing to a multi-media file representing the asset.",
    )
    animation_url_integrity: Arc3Sri | None = Field(
        default=None,
        description="The SHA-256 digest of the file pointed by the URI external_url. The field value is a single SHA-256 integrity metadata as defined in the W3C subresource integrity specification (https://w3c.github.io/webappsec-subresource-integrity).",
    )
    animation_url_mimetype: MimeType | None = Field(
        default=None,
        description="The MIME type of the file pointed by the URI animation_url. If the MIME type is not specified, clients MAY guess the MIME type from the file extension or MAY decide not to display the asset at all. It is STRONGLY RECOMMENDED to include the MIME type.",
    )
    properties: Arc3Properties | None = Field(
        default=None,
        description="Arbitrary properties (also called attributes). Values may be strings, numbers, object or arrays.",
    )
    extra_metadata: Base64Str | None = Field(
        default=None,
        description="Extra metadata in base64. If the field is specified (even if it is an empty string) the asset metadata (am) of the ASA is computed differently than if it is not specified.",
    )
    localization: Arc3Localization | None = Field(
        default=None,
        description="A sub-object that may be used to provide localized values for fields that need it.",
    )
