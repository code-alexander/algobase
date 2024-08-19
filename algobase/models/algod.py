"""Pydantic models for the Algod API (v2).

Mostly auto-generated using datamodel-codegen.
Spec: https://github.com/algorand/go-algorand/blob/master/daemon/algod/api/algod.oas3.yml
"""


from enum import StrEnum, auto
from typing import Annotated, Any

from pydantic import BaseModel, Field, RootModel


class SigType(StrEnum):
    """Enumeration for signature types."""

    SIG = auto()
    MISG = auto()
    LSIG = auto()


class AccountParticipation(BaseModel):
    """Account participation information."""

    selection_participation_key: str = Field(
        ...,
        alias="selection-participation-key",
        description="[sel] Selection public key (if any) currently registered for this round.",
    )
    state_proof_key: str | None = Field(
        None,
        alias="state-proof-key",
        description="[stprf] Root of the state proof key (if any)",
    )
    vote_first_valid: int = Field(
        ...,
        alias="vote-first-valid",
        description="[voteFst] First round for which this participation is valid.",
    )
    vote_key_dilution: int = Field(
        ...,
        alias="vote-key-dilution",
        description="[voteKD] Number of subkeys in each batch of participation keys.",
    )
    vote_last_valid: int = Field(
        ...,
        alias="vote-last-valid",
        description="[voteLst] Last round for which this participation is valid.",
    )
    vote_participation_key: str = Field(
        ...,
        alias="vote-participation-key",
        description="[vote] root participation public key (if any) currently registered for this round.",
    )


class TealValue(BaseModel):
    """Teal value."""

    bytes: str = Field(..., description="[tb] bytes value.")
    type: int = Field(
        ...,
        description="[tt] value type. Value `1` refers to **bytes**, value `2` refers to **uint**",
    )
    uint: int = Field(..., description="[ui] uint value.")


class TealKeyValue(BaseModel):
    """Teal key-value pair."""

    key: str
    value: TealValue


TealKeyValueStore = RootModel[list[TealKeyValue]]


class ApplicationStateSchema(BaseModel):
    """Application state schema."""

    num_byte_slice: int = Field(
        ..., alias="num-byte-slice", description="[nbs] num of byte slices."
    )
    num_uint: int = Field(..., alias="num-uint", description="[nui] num of uints.")


class ApplicationLocalState(BaseModel):
    """Application local state."""

    id: int = Field(..., description="The application which this local state is for.")
    key_value: TealKeyValueStore | None = Field(None, alias="key-value")
    schema_: ApplicationStateSchema = Field(..., alias="schema")


class ApplicationParams(BaseModel):
    """Application parameters."""

    approval_program: str = Field(
        ..., alias="approval-program", description="[approv] approval program."
    )
    clear_state_program: str = Field(
        ..., alias="clear-state-program", description="[clearp] approval program."
    )
    creator: str = Field(
        ...,
        description="The address that created this application. This is the address where the parameters and global state for this application can be found.",
    )
    extra_program_pages: int | None = Field(
        None,
        alias="extra-program-pages",
        description="[epp] the amount of extra program pages available to this app.",
    )
    global_state: TealKeyValueStore | None = Field(None, alias="global-state")
    global_state_schema: ApplicationStateSchema | None = Field(
        None, alias="global-state-schema"
    )
    local_state_schema: ApplicationStateSchema | None = Field(
        None, alias="local-state-schema"
    )


class Application(BaseModel):
    """Application information."""

    id: int = Field(..., description="[appidx] application index.")
    params: ApplicationParams


class AssetHolding(BaseModel):
    """Asset holding information."""

    amount: int = Field(..., description="[a] number of units held.")
    asset_id: int = Field(..., alias="asset-id", description="Asset ID of the holding.")
    is_frozen: bool = Field(
        ...,
        alias="is-frozen",
        description="[f] whether or not the holding is frozen.",
    )


class AssetParams(BaseModel):
    """Asset parameters."""

    clawback: str | None = Field(
        None,
        description="[c] Address of account used to clawback holdings of this asset.  If empty, clawback is not permitted.",
    )
    creator: str = Field(
        ...,
        description="The address that created this asset. This is the address where the parameters for this asset can be found, and also the address where unwanted asset units can be sent in the worst case.",
    )
    decimals: Annotated[int, Field(strict=True, ge=0, le=19)] = Field(
        ...,
        description="[dc] The number of digits to use after the decimal point when displaying this asset. If 0, the asset is not divisible. If 1, the base unit of the asset is in tenths. If 2, the base unit of the asset is in hundredths, and so on. This value must be between 0 and 19 (inclusive).",
    )
    default_frozen: bool | None = Field(
        None,
        alias="default-frozen",
        description="[df] Whether holdings of this asset are frozen by default.",
    )
    freeze: str | None = Field(
        None,
        description="[f] Address of account used to freeze holdings of this asset.  If empty, freezing is not permitted.",
    )
    manager: str | None = Field(
        None,
        description="[m] Address of account used to manage the keys of this asset and to destroy it.",
    )
    metadata_hash: str | None = Field(
        None,
        alias="metadata-hash",
        description="[am] A commitment to some unspecified asset metadata. The format of this metadata is up to the application.",
    )
    asset_name: str | None = Field(
        None,
        alias="name",
        description="[an] Name of this asset, as supplied by the creator. Included only when the asset name is composed of printable utf-8 characters.",
    )
    name_b64: str | None = Field(
        None,
        alias="name-b64",
        description="Base64 encoded name of this asset, as supplied by the creator.",
    )
    reserve: str | None = Field(
        None,
        description="[r] Address of account holding reserve (non-minted) units of this asset.",
    )
    total: int = Field(..., description="[t] The total number of units of this asset.")
    unit_name: str | None = Field(
        None,
        alias="unit-name",
        description="[un] Name of a unit of this asset, as supplied by the creator. Included only when the name of a unit of this asset is composed of printable utf-8 characters.",
    )
    unit_name_b64: str | None = Field(
        None,
        alias="unit-name-b64",
        description="Base64 encoded name of a unit of this asset, as supplied by the creator.",
    )
    url: str | None = Field(
        None,
        description="[au] URL where more information about the asset can be retrieved. Included only when the URL is composed of printable utf-8 characters.",
    )
    url_b64: str | None = Field(
        None,
        alias="url-b64",
        description="Base64 encoded URL where more information about the asset can be retrieved.",
    )


class Asset(BaseModel):
    """Asset information."""

    index: int = Field(..., description="unique asset identifier")
    params: AssetParams


class Account(BaseModel):
    """Account information."""

    address: str = Field(..., description="the account public key")
    amount: int = Field(
        ..., description="[algo] total number of MicroAlgos in the account"
    )
    amount_without_pending_rewards: int = Field(
        ...,
        alias="amount-without-pending-rewards",
        description="specifies the amount of MicroAlgos in the account, without the pending rewards.",
    )
    apps_local_state: list[ApplicationLocalState] | None = Field(
        None,
        alias="apps-local-state",
        description="[appl] applications local data stored in this account.\n\nNote the raw object uses `map[int] -> AppLocalState` for this type.",
    )
    apps_total_extra_pages: int | None = Field(
        None,
        alias="apps-total-extra-pages",
        description="[teap] the sum of all extra application program pages for this account.",
    )
    apps_total_schema: ApplicationStateSchema | None = Field(
        None, alias="apps-total-schema"
    )
    assets: list[AssetHolding] | None = Field(
        None,
        description="[asset] assets held by this account.\n\nNote the raw object uses `map[int] -> AssetHolding` for this type.",
    )
    auth_addr: str | None = Field(
        None,
        alias="auth-addr",
        description="[spend] the address against which signing should be checked. If empty, the address of the current account is used. This field can be updated in any transaction by setting the RekeyTo field.",
    )
    created_apps: list[Application] | None = Field(
        None,
        alias="created-apps",
        description="[appp] parameters of applications created by this account including app global data.\n\nNote: the raw account uses `map[int] -> AppParams` for this type.",
    )
    created_assets: list[Asset] | None = Field(
        None,
        alias="created-assets",
        description="[apar] parameters of assets created by this account.\n\nNote: the raw account uses `map[int] -> Asset` for this type.",
    )
    min_balance: int = Field(
        ...,
        alias="min-balance",
        description="MicroAlgo balance required by the account.\n\nThe requirement grows based on asset and application usage.",
    )
    participation: AccountParticipation | None = None
    pending_rewards: int = Field(
        ...,
        alias="pending-rewards",
        description="amount of MicroAlgos of pending rewards in this account.",
    )
    reward_base: int | None = Field(
        None,
        alias="reward-base",
        description="[ebase] used as part of the rewards computation. Only applicable to accounts which are participating.",
    )
    rewards: int = Field(
        ...,
        description="[ern] total rewards of MicroAlgos the account has received, including pending rewards.",
    )
    round: int = Field(
        ..., description="The round for which this information is relevant."
    )
    sig_type: SigType | None = Field(
        None,
        alias="sig-type",
        description="Indicates what type of signature is used by this account, must be one of:\n* sig\n* msig\n* lsig",
    )
    status: str = Field(
        ...,
        description="[onl] delegation status of the account's MicroAlgos\n* Offline - indicates that the associated account is delegated.\n*  Online  - indicates that the associated account used as part of the delegation pool.\n*   NotParticipating - indicates that the associated account is neither a delegator nor a delegate.",
    )
    total_apps_opted_in: int = Field(
        ...,
        alias="total-apps-opted-in",
        description="The count of all applications that have been opted in, equivalent to the count of application local data (AppLocalState objects) stored in this account.",
    )
    total_assets_opted_in: int = Field(
        ...,
        alias="total-assets-opted-in",
        description="The count of all assets that have been opted in, equivalent to the count of AssetHolding objects held by this account.",
    )
    total_box_bytes: int | None = Field(
        None,
        alias="total-box-bytes",
        description="\\[tbxb\\] The total number of bytes used by this account's app's box keys and values.",
    )
    total_boxes: int | None = Field(
        None,
        alias="total-boxes",
        description="\\[tbx\\] The number of existing boxes created by this account's app.",
    )
    total_created_apps: int = Field(
        ...,
        alias="total-created-apps",
        description="The count of all apps (AppParams objects) created by this account.",
    )
    total_created_assets: int = Field(
        ...,
        alias="total-created-assets",
        description="The count of all assets (AssetParams objects) created by this account.",
    )


class EvalDelta(BaseModel):
    """EvalDelta."""

    action: int = Field(..., description="\\[at\\] delta action.")
    bytes: str | None = Field(None, description="\\[bs\\] bytes value.")
    uint: int | None = Field(None, description="\\[ui\\] uint value.")


class EvalDeltaKeyValue(BaseModel):
    """EvalDeltaKeyValue."""

    key: str
    value: EvalDelta


# Application state delta
StateDelta = RootModel[list[EvalDeltaKeyValue]]


class AccountStateDelta(BaseModel):
    """AccountStateDelta."""

    address: str
    delta: StateDelta


class PendingTransactionResponse(BaseModel):
    """PendingTransactionResponse."""

    application_index: int | None = Field(
        None,
        alias="application-index",
        description="The application index if the transaction was found and it created an application.",
    )
    asset_closing_amount: int | None = Field(
        None,
        alias="asset-closing-amount",
        description="The number of the asset's unit that were transferred to the close-to address.",
    )
    asset_index: int | None = Field(
        None,
        alias="asset-index",
        description="The asset index if the transaction was found and it created an asset.",
    )
    close_rewards: int | None = Field(
        None,
        alias="close-rewards",
        description="Rewards in microalgos applied to the close remainder to account.",
    )
    closing_amount: int | None = Field(
        None, alias="closing-amount", description="Closing amount for the transaction."
    )
    confirmed_round: int | None = Field(
        None,
        alias="confirmed-round",
        description="The round where this transaction was confirmed, if present.",
    )
    global_state_delta: StateDelta | None = Field(None, alias="global-state-delta")
    inner_txns: list["PendingTransactionResponse"] | None = Field(
        None,
        alias="inner-txns",
        description="Inner transactions produced by application execution.",
    )
    local_state_delta: list[AccountStateDelta] | None = Field(
        None,
        alias="local-state-delta",
        description="Local state key/value changes for the application being executed by this transaction.",
    )
    logs: list[str] | None = Field(
        None, description="Logs for the application being executed by this transaction."
    )
    pool_error: str = Field(
        ...,
        alias="pool-error",
        description="Indicates that the transaction was kicked out of this node's transaction pool (and specifies why that happened).  An empty string indicates the transaction wasn't kicked out of this node's txpool due to an error.\n",
    )
    receiver_rewards: int | None = Field(
        None,
        alias="receiver-rewards",
        description="Rewards in microalgos applied to the receiver account.",
    )
    sender_rewards: int | None = Field(
        None,
        alias="sender-rewards",
        description="Rewards in microalgos applied to the sender account.",
    )
    txn: dict[str, Any] = Field(..., description="The raw signed transaction.")
