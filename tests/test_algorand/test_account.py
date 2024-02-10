"""Tests the `Account` class."""

from algobase.algorand.account import Account


def test_account() -> None:
    """Tests the `Account` class."""
    account = Account(private_key="test_key", address="test_address")
    assert account.private_key == "test_key"
    assert account.address == "test_address"
