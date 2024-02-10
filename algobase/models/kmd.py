"""Pydantic models for the KMD API (v1).

Mostly auto-generated using datamodel-codegen.
Spec: https://github.com/algorand/go-algorand/blob/master/daemon/kmd/api/swagger.json
"""

from typing import TypeAlias

from pydantic import BaseModel

TxType: TypeAlias = str


class APIV1Wallet(BaseModel):
    """A KMD wallet."""

    driver_name: str | None
    driver_version: int | None
    id: str | None
    mnemonic_ux: bool | None
    name: str | None
    supported_txs: list[TxType] | None


class APIV1GETWalletsResponse(BaseModel):
    """The response from the `GET /v1/wallets` endpoint."""

    error: bool | None
    message: str | None
    wallets: list[APIV1Wallet] | None
