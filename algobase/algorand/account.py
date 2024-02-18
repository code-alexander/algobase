"""Algorand account class."""

from dataclasses import dataclass
from typing import Self

from algosdk.account import address_from_private_key, generate_account


@dataclass(frozen=True, slots=True)
class Account:
    """Represents an Algorand account."""

    private_key: str
    address: str

    @classmethod
    def from_private_key(cls, private_key: str) -> Self:
        """Create an account from the given private key."""
        return cls(
            private_key=private_key, address=address_from_private_key(private_key)
        )


def create_account() -> Account:
    """Create a new Algorand account.

    Returns:
        Account: The account.
    """
    private_key, address = generate_account()
    return Account(private_key=private_key, address=address)
