"""Pydantic models for Algorand Standard Assets (ASAs)."""

import math
import warnings
from base64 import b64decode

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    model_validator,
)

from algobase.choices import Arc, AsaType, AsaTypeChoice
from algobase.models.arc3 import Arc3Metadata
from algobase.models.asset_params import AssetParams
from algobase.types.annotated import AlgorandHash, AsaAssetName
from algobase.utils.hash import sha256, sha512_256
from algobase.utils.validate import is_valid, validate_type_compatibility


class Asa(BaseModel):
    """A Pydantic model for Algorand Standard Assets (ASAs)."""

    model_config = ConfigDict(frozen=True)

    asa_type: AsaTypeChoice | None = Field(
        default=None, description="The type of the ASA."
    )
    asset_params: AssetParams = Field(description="AssetParams Pydantic model.")
    metadata: Arc3Metadata | None = Field(
        default=None, description="Arc3Metadata Pydantic model."
    )

    @property
    def derived_asa_type(self) -> AsaTypeChoice:
        """The derived type of the ASA."""
        match self.asset_params:
            case asa if asa.total == 1 and asa.decimals == 0:
                return AsaType.NON_FUNGIBLE_PURE
            # Means the total supply is 1
            case asa if asa.decimals == math.log10(asa.total):
                return AsaType.NON_FUNGIBLE_FRACTIONAL
            case _:
                return AsaType.FUNGIBLE

    @computed_field  # type: ignore[misc]
    @property
    def metadata_hash(self) -> AlgorandHash | None:
        """The hash of the JSON metadata."""
        if self.metadata is not None:
            # Currently only ARC3 is supported
            if self.metadata.arc == Arc.ARC3:
                if self.metadata.extra_metadata is None:
                    return sha256(self.metadata.json_bytes)
                else:
                    # am = SHA-512/256("arc0003/am" || SHA-512/256("arc0003/amj" || content of JSON Metadata file) || e)
                    base_hash = sha512_256(b"arc0003/amj" + self.metadata.json_bytes)
                    extra_metadata_bytes = b64decode(self.metadata.extra_metadata)
                    return sha512_256(b"arc0003/am" + base_hash + extra_metadata_bytes)
        return None

    @model_validator(mode="after")
    def check_asa_type_constraints(self) -> "Asa":
        """Validate the ASA type against the relevant constraints."""
        if self.asa_type is not None and self.asa_type != self.derived_asa_type:
            match self.asa_type:
                case AsaType.NON_FUNGIBLE_PURE:
                    raise ValueError(
                        "Total number of units must be 1 and number of digits after the decimal point must be 0 for a pure NFT."
                    )
                case AsaType.NON_FUNGIBLE_FRACTIONAL:
                    raise ValueError(
                        "Number of digits after the decimal point must be equal to the logarithm in base 10 of total number of units. In other words, the total supply of the ASA must be exactly 1."
                    )
                case AsaType.FUNGIBLE:
                    raise ValueError(
                        "Total supply of the ASA must be greater than 1, for a fungible asset."
                    )
        return self

    @model_validator(mode="after")
    def check_arc_constraints(self) -> "Asa":
        """Validate fields against ARC constraints, if applicable."""
        if self.metadata is not None:
            # Currently only ARC3 is supported
            match self.metadata.arc:
                case Arc.ARC3:
                    self.check_arc3_constraints()
        return self

    def check_arc3_decimals(self) -> "Asa":
        """Raise an error if the decimals in the asset parameters doesn't match the deimals in the metadata."""
        if (
            self.metadata is not None
            and self.metadata.decimals is not None
            and self.metadata.decimals != self.asset_params.decimals
        ):
            raise ValueError(
                f"Decimals in the asset parameters ({self.asset_params.decimals}) must match the decimals in the metadata ({self.metadata.decimals})."
            )
        return self

    def check_arc3_unit_name(self) -> "Asa":
        """Raise a warning if the metadata 'name' property is not related to the asset unit name.

        This is currently a naive check to see if the asset unit name is a substring of the metadata name.
        It could be improved using difflib in the future.
        """
        if (
            self.asset_params.unit_name is not None
            and self.metadata is not None
            and self.metadata.name is not None
            and self.asset_params.unit_name.lower() not in self.metadata.name.lower()
        ):
            warnings.warn(
                UserWarning(
                    "Asset unit name should be related to the name in the ARC-3 JSON metadata."
                )
            )
        return self

    def check_arc3_asset_url(self) -> "Asa":
        """Checks that the asset URL is valid for ARC-3 ASAs."""
        if self.asset_params.url is None:
            raise ValueError("Asset URL must not be `None`.")
        elif not self.asset_params.url.endswith("#arc3"):
            raise ValueError(
                f"Asset URL must end with '#arc3' if asset name is '{self.asset_params.asset_name}'."
            )
        return self

    def check_arc3_constraints(self) -> "Asa":
        """Validate fields against ARC constraints, if applicable.

        Raises warnings for values/formats that are allowed but not recommended in ARC specs.
        Raises errors for values/formats that are not allowed in ARC specs.
        """
        if self.metadata is not None:
            # Currently only ARC3 is supported
            if self.metadata.arc == Arc.ARC3:
                self.check_arc3_unit_name()
                self.check_arc3_decimals()

                # Asset name constraints
                match self.asset_params.asset_name:
                    case None:
                        raise ValueError(
                            "Asset name must not be `None` for ARC-3 ASAs."
                        )
                    case "arc3":
                        warnings.warn(
                            UserWarning(
                                "Asset name 'arc3' is not recommended for ARC-3 ASAs."
                            )
                        )
                    case x if x.endswith("@arc3"):
                        warnings.warn(
                            UserWarning(
                                "Asset name format <name>@arc3 is not recommended for ARC-3 ASAs."
                            )
                        )
                    # Constraints on combination of asset name and metadata name
                    case _:
                        match self.metadata.name:
                            case None:
                                raise ValueError(
                                    f"Metadata name must not be `None` if asset name is '{self.asset_params.asset_name}'."
                                )
                            case x if x != self.asset_params.asset_name:
                                if is_valid(
                                    validate_type_compatibility,
                                    self.metadata.name,
                                    AsaAssetName,
                                ):
                                    raise ValueError(
                                        f"Asset name '{self.asset_params.asset_name}' must match the metadata name '{x}'."
                                    )
                                elif not self.metadata.name.startswith(
                                    self.asset_params.asset_name
                                ):
                                    raise ValueError(
                                        f"Asset name must be a shortened version of the metadata name '{self.metadata.name}'."
                                    )
                        # Constraints on combination of asset name and asset URL
                        self.check_arc3_asset_url()
        return self
