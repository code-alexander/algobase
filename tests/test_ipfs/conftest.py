"""Pytest fixtures for the IPFS client tests."""


import pytest

from tests.types import FixtureDict


@pytest.fixture
def nft_storage_store_json_successful() -> FixtureDict:
    """Pytest fixture that returns a dictionary response from a successful upload to IPFS via nft.storage.

    Returns:
        FixtureDict: The dictionary response.
    """
    return {
        "ok": True,
        "value": {
            "cid": "bafkreic7xfupwwdiwnzudgi6s6brjunxktdfio4hj4a5tlp2hrou7rnjvy",
            "created": "2024-01-29T09:15:48.637+00:00",
            "type": "application/json",
            "scope": "test-1",
            "files": [],
            "size": 58,
            "name": "Upload at 2024-01-29T09:17:17.808Z",
            "pin": {
                "cid": "bafkreic7xfupwwdiwnzudgi6s6brjunxktdfio4hj4a5tlp2hrou7rnjvy",
                "created": "2024-01-29T09:15:48.637+00:00",
                "size": 58,
                "status": "pinned",
            },
            "deals": [],
        },
    }


@pytest.fixture
def nft_storage_store_json_bad_request() -> FixtureDict:
    """Pytest fixture that returns a dictionary response from a failed upload to IPFS via nft.storage (HTTP 400).

    Returns:
        FixtureDict: The dictionary response.
    """
    return {"ok": False, "error": {"name": "string", "message": "string"}}


@pytest.fixture
def nft_storage_store_json_unauthorized() -> FixtureDict:
    """Pytest fixture that returns a dictionary response from a failed upload to IPFS via nft.storage (HTTP 401).

    Returns:
        FixtureDict: The dictionary response.
    """
    return {"ok": False, "error": {"name": "HTTP Error", "message": "Unauthorized"}}


@pytest.fixture
def nft_storage_store_json_forbidden() -> FixtureDict:
    """Pytest fixture that returns a dictionary response from a failed upload to IPFS via nft.storage (HTTP 403).

    Returns:
        FixtureDict: The dictionary response.
    """
    return {
        "ok": False,
        "error": {"name": "HTTP Error", "message": "Token is not valid"},
    }


@pytest.fixture
def nft_storage_store_json_internal_server_error() -> FixtureDict:
    """Pytest fixture that returns a dictionary response from a failed upload to IPFS via nft.storage (HTTP 500).

    Returns:
        FixtureDict: The dictionary response.
    """
    return {"ok": False, "error": {"name": "string", "message": "string"}}


@pytest.fixture
def nft_storage_fetch_pin_status_successful() -> FixtureDict:
    """Pytest fixture that returns a dictionary response from a successful pin status check from nft.storage.

    Returns:
        FixtureDict: The dictionary response.
    """
    return {
        "ok": True,
        "value": {
            "cid": "bafkreic7xfupwwdiwnzudgi6s6brjunxktdfio4hj4a5tlp2hrou7rnjvy",
            "pin": {
                "cid": "bafkreic7xfupwwdiwnzudgi6s6brjunxktdfio4hj4a5tlp2hrou7rnjvy",
                "created": "2024-01-29T09:15:48.637+00:00",
                "size": 58,
                "status": "pinned",
            },
            "deals": [
                {
                    "status": "active",
                    "lastChanged": "2024-01-30T00:30:04.385474+00:00",
                    "chainDealID": 70754247,
                    "datamodelSelector": "Links/224/Hash/Links/23/Hash/Links/0/Hash",
                    "statusText": None,
                    "dealActivation": "2024-02-01T20:28:00+00:00",
                    "dealExpiration": "2025-07-17T20:28:00+00:00",
                    "miner": "f020378",
                    "pieceCid": "baga6ea4seaqe5zxp37xbig2veyqbp5e2ce7jzqrptwxgj6ys3echq56vnaeggga",
                    "batchRootCid": "bafybeihcgb5rwrkde6zf3bn2xrvr7ytfvtu3g6yrhez6sq5pjw5nkrf2m4",
                }
            ],
        },
    }


@pytest.fixture
def nft_storage_fetch_pin_status_not_found() -> FixtureDict:
    """Pytest fixture that returns a dictionary response from a failed pin status check from nft.storage (HTTP 404).

    Returns:
        FixtureDict: The dictionary response.
    """
    return {"ok": False, "error": {"name": "string", "message": "string"}}


@pytest.fixture
def nft_storage_fetch_pin_status_internal_server_error() -> FixtureDict:
    """Pytest fixture that returns a dictionary response from a failed pin status check from nft.storage (HTTP 500).

    Returns:
        FixtureDict: The dictionary response.
    """
    return {"ok": False, "error": {"name": "string", "message": "string"}}
