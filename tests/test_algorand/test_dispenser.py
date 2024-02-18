"""Tests for the Algorand TestNet dispenser API client."""

from typing import Any

import httpx
import pytest
from pytest_httpx import HTTPXMock

from algobase.algorand.dispenser import Dispenser
from algobase.choices import AlgorandAsset
from algobase.models.dispenser import DispenserFundResponse


@pytest.mark.parametrize(
    "field, expected",
    [
        ("_api_key", "test_key"),
        ("api_key", "test_key"),
        ("is_api_key_required", True),
        ("base_url", "https://api.dispenser.algorandfoundation.tools"),
        ("headers", {"Authorization": "Bearer test_key"}),
    ],
)
def test_properties(field: str, expected: Any) -> None:
    """Test the properties of the `TestNetDispenser` class."""
    client = Dispenser(_api_key="test_key")
    assert getattr(client, field) == expected


def test_fund_successful(
    httpx_mock: HTTPXMock,
) -> None:
    """Test that the response is parsed correctly when the request is successful (response is mocked)."""
    httpx_mock.add_response(
        json={
            "txID": "SFSHW3D33H6AIA26B53JPHX2HUXATKD4XL7T473XN7RIP7X7F3BA",
            "amount": 1000000,
        }
    )
    client = Dispenser(_api_key="test_key")
    response = client.fund(
        address="test_address", amount=1000000, asset_id=AlgorandAsset.ALGO
    )
    assert isinstance(response, DispenserFundResponse)
    assert response.tx_id == "SFSHW3D33H6AIA26B53JPHX2HUXATKD4XL7T473XN7RIP7X7F3BA"
    assert response.amount == 1000000


def test_fund_error(
    httpx_mock: HTTPXMock,
) -> None:
    """Test that an error is raised when the request is unsuccessful (response is mocked)."""
    httpx_mock.add_response(
        status_code=500,
        json={"code": "unexpected_error", "message": "Unexpected internal error"},
    )
    client = Dispenser(_api_key="test_key")
    with pytest.raises(httpx.HTTPError):
        client.fund(address="test_address", amount=1000000, asset_id=AlgorandAsset.ALGO)
