"""Tests the `Account` class."""

from algobase.algorand.account import Account, create_account


def test_account() -> None:
    """Tests the `Account` class."""
    account = Account(private_key="test_key", address="test_address")
    assert account.private_key == "test_key"
    assert account.address == "test_address"


def test_create_account() -> None:
    """Test the create_account() function."""
    account = create_account()
    assert isinstance(account, Account)
