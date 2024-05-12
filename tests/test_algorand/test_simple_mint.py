"""Tests for the simple mint utility functions."""
from unittest.mock import MagicMock

from algosdk.transaction import AssetConfigTxn, SuggestedParams

from algobase.algorand.account import Account
from algobase.algorand.simple_mint import (
    create_asa,
    create_asset_config_txn,
    create_metadata,
    create_metadata_arc19,
    mint,
)
from algobase.choices import Arc
from algobase.models.arc3 import Arc3Metadata
from algobase.models.arc19 import Arc19Metadata
from algobase.models.asa import Asa


def test_create_metadata() -> None:
    """Test the create_metadata() function."""
    metadata = create_metadata(
        description="My first NFT!", properties={"creator": "test_address"}
    )
    assert isinstance(metadata, Arc3Metadata)
    assert metadata.arc == Arc.ARC3
    assert metadata.name == "NFT"
    assert metadata.decimals == 0
    assert metadata.description == "My first NFT!"
    assert getattr(metadata.properties, "creator") == "test_address"


def test_create_metadata_arc19() -> None:
    """Test the create_metadata_arc19() function."""
    metadata = create_metadata_arc19(
        description="My first NFT!", properties={"creator": "test_address"}
    )
    assert isinstance(metadata, Arc19Metadata)
    assert metadata.arc == Arc.ARC19
    assert hasattr(metadata, "arc3_metadata") and isinstance(
        metadata.arc3_metadata, Arc3Metadata
    )
    assert metadata.arc3_metadata.name == "NFT"
    assert metadata.arc3_metadata.decimals == 0
    assert metadata.arc3_metadata.description == "My first NFT!"
    assert getattr(metadata.arc3_metadata.properties, "creator") == "test_address"


def test_create_asa() -> None:
    """Test the create_asa() function for ARC-3 metadata."""
    metadata = create_metadata(
        description="My first NFT!", properties={"creator": "test_address"}
    )
    cid = "test_cid"
    asa = create_asa(metadata, cid)
    assert isinstance(asa, Asa)
    assert asa.asset_params.total == 1
    assert asa.asset_params.decimals == 0
    assert asa.asset_params.unit_name == "NFT"
    assert asa.asset_params.asset_name == "NFT"
    assert asa.asset_params.url == "ipfs://test_cid/#arc3"
    assert isinstance(asa.metadata, Arc3Metadata)
    assert asa.metadata == metadata


def test_create_asset_config_txn() -> None:
    """Test the create_asset_config_txn() function."""
    mock_algod = MagicMock()
    mock_algod.suggested_params.return_value = SuggestedParams(
        **{
            "first": 6,
            "last": 1006,
            "gh": "W+YiTIAibva56J3LrTHBIEQ//VUE/8eSZzBqJmykhWo=",
            "gen": "dockernet-v1",
            "fee": 0,
            "flat_fee": False,
            "consensus_version": "future",
            "min_fee": 1000,
        }
    )

    account = Account(
        "test_key", "UYAUCPT2B475MESZAIA4BULTWIQM23VBPHQOLKKOPD7JRFB5QS4L3BOFUM"
    )

    txn = create_asset_config_txn(
        mock_algod,
        account,
        create_asa(
            metadata=create_metadata(
                description="My first NFT!", properties={"creator": "test_address"}
            ),
            cid="test_cid",
        ),
    )

    assert isinstance(txn, AssetConfigTxn)


def test_mint() -> None:
    """Test the mint() function."""
    mock_algod = MagicMock()
    mock_algod.suggested_params.return_value = SuggestedParams(
        **{
            "first": 6,
            "last": 1006,
            "gh": "W+YiTIAibva56J3LrTHBIEQ//VUE/8eSZzBqJmykhWo=",
            "gen": "dockernet-v1",
            "fee": 0,
            "flat_fee": False,
            "consensus_version": "future",
            "min_fee": 1000,
        }
    )
    mock_algod.send_transaction.return_value = "test_txid"
    mock_algod.status.return_value = {"last-round": 0}
    mock_algod.pending_transaction_info.return_value = {
        "asset-index": 1007,
        "confirmed-round": 7,
        "pool-error": "",
        "txn": {
            "sig": "KCbvV1FV2xLbFUGI7MtIFfYCg2p59FX5SJJZsXUc3bsGXkm/wIK6ezHgC/Et5fc9k9UXtb/orbKzbHsFqj/9BQ==",
            "txn": {
                "apar": {
                    "am": "LvYRe05h02XZbUNAUTGu43QAvYRqyzpfrRKBlAh/wak=",
                    "an": "NFT",
                    "au": "ipfs://test_cid/#arc3",
                    "m": "UYAUCPT2B475MESZAIA4BULTWIQM23VBPHQOLKKOPD7JRFB5QS4L3BOFUM",
                    "r": "UYAUCPT2B475MESZAIA4BULTWIQM23VBPHQOLKKOPD7JRFB5QS4L3BOFUM",
                    "t": 1,
                    "un": "NFT",
                },
                "fee": 1000,
                "fv": 6,
                "gen": "dockernet-v1",
                "gh": "W+YiTIAibva56J3LrTHBIEQ//VUE/8eSZzBqJmykhWo=",
                "lv": 1006,
                "snd": "UYAUCPT2B475MESZAIA4BULTWIQM23VBPHQOLKKOPD7JRFB5QS4L3BOFUM",
                "type": "acfg",
            },
        },
    }

    account = Account(
        "sDR9sBBWSSks/yYVFGTT1X6imLL12DF6+x+4l2hX7ji+EC+xUI8Paxpbo+tSC6o2BAv+QIRPF2zO3cvKn3N3Pg==",
        "UYAUCPT2B475MESZAIA4BULTWIQM23VBPHQOLKKOPD7JRFB5QS4L3BOFUM",
    )
    cid = "test_cid"

    metadata = Arc3Metadata(
        arc=Arc.ARC3,
        name="NFT",
        decimals=0,
        description="My first NFT!",
    )

    asset_id = mint(mock_algod, account, metadata, cid)

    assert isinstance(asset_id, int)
    assert asset_id == 1007
