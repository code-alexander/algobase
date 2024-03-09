"""Pydantic models for Algorand ARC-19 metadata.

Reference: https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0019.md
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from algobase.choices import Arc
from algobase.models.arc3 import Arc3Metadata


class Arc19Metadata(BaseModel):
    """A Pydantic model for Algorand ARC-19 metadata."""

    model_config = ConfigDict(frozen=True)

    arc: Literal[Arc.ARC19] = Field(
        default=Arc.ARC19,
        description="Name of the Algorand ARC standard that the NFT metadata adheres to.",
        exclude=True,
    )

    arc3_metadata: Arc3Metadata | None = Field(
        default=None,
        description="Optional ARC-3 metadata model.",
    )

    @model_validator(mode="after")
    def validate_arc3_compliance(self) -> "Arc19Metadata":
        """If the ARC-3 metadata is present, ensure it complies with ARC-19.

        Raises:
            ValueError: If the ARC-3 metadata is present and does not comply with ARC-19.

        Returns:
            Arc19Metadata: The model instance.
        """
        if (
            self.arc3_metadata is not None
            and self.arc3_metadata.extra_metadata is not None
        ):
            raise ValueError("Extra metadata is not supported for ARC-19.")
        return self
