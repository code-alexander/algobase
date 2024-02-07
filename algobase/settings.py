"""Configuration settings for the algobase."""


from collections.abc import Callable
from typing import Self, TypeVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from algobase.choices import (
    AlgorandApiProvider,
    AlgorandApiProviderChoice,
    AlgorandNetwork,
    AlgorandNetworkChoice,
)

T = TypeVar("T")


class Settings(BaseSettings):
    """Pydantic model for algobase settings."""

    model_config = SettingsConfigDict(env_prefix="AB_")

    algorand_network: AlgorandNetworkChoice = Field(
        description="The name of the Algorand network.",
        default=AlgorandNetwork.LOCALNET,
    )
    algorand_provider: AlgorandApiProviderChoice = Field(
        description="The Algorand API provider.", default=AlgorandApiProvider.LOCALHOST
    )
    algod_token: str = Field(description="The Algod API token.", default="a" * 64)

    nft_storage_api_key: str | None = Field(
        description="API key for nft.storage.", default=None
    )

    def __or__(self, f: Callable[[Self], T]) -> T:
        """Operator overloading to pipe settings into a function or other callable.

        Args:
            f (Callable[[Self], T]): The function that takes `settings` as an argument.

        Returns:
            T: The type returned by the function.
        """
        return f(self)
