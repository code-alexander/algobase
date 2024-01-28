"""Enums and enum type aliases for algobase."""

from enum import StrEnum, auto
from typing import Literal, TypeAlias


class Arc(StrEnum):
    """An enumeration of Algorand ARC standards that are supported in algobase."""

    ARC3 = auto()


ArcChoice: TypeAlias = Literal[Arc.ARC3]


class AsaType(StrEnum):
    """An enumeration of Algorand Standard Asset (ASA) types."""

    FUNGIBLE = auto()
    NON_FUNGIBLE_PURE = auto()
    NON_FUNGIBLE_FRACTIONAL = auto()


AsaTypeChoice: TypeAlias = Literal[
    AsaType.FUNGIBLE, AsaType.NON_FUNGIBLE_PURE, AsaType.NON_FUNGIBLE_FRACTIONAL
]
