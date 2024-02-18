"""Pydantic models for the Algorand TestNet dispenser API."""

from pydantic import BaseModel, ConfigDict, Field


class DispenserFundResponse(BaseModel):
    """TestNet dispenser API 'fund' response."""

    model_config = ConfigDict(frozen=True)

    tx_id: str = Field(alias="txID")
    amount: int
