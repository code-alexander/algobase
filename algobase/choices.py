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


class IpfsProvider(StrEnum):
    """An enumeration of IPFS providers."""

    NFT_STORAGE = auto()


IpfsProviderChoice: TypeAlias = Literal[IpfsProvider.NFT_STORAGE]


class IpfsPinStatus(StrEnum):
    """An enumeration of IPFS pin statuses."""

    QUEUED = auto()
    PINNING = auto()
    PINNED = auto()
    FAILED = auto()


IpfsPinStatusChoice: TypeAlias = Literal[
    IpfsPinStatus.QUEUED,
    IpfsPinStatus.PINNING,
    IpfsPinStatus.PINNED,
    IpfsPinStatus.FAILED,
]


class AlgorandNetwork(StrEnum):
    """An enumeration of Algorand networks."""

    LOCALNET = auto()
    TESTNET = auto()
    MAINNET = auto()


AlgorandNetworkChoice: TypeAlias = Literal[
    AlgorandNetwork.LOCALNET, AlgorandNetwork.TESTNET, AlgorandNetwork.MAINNET
]


class AlgorandApi(StrEnum):
    """An enumeration of Algorand APIs."""

    ALGOD = auto()
    INDEXER = auto()
    KMD = auto()


AlgorandApiChoice: TypeAlias = Literal[
    AlgorandApi.ALGOD, AlgorandApi.INDEXER, AlgorandApi.KMD
]


class AlgorandApiProvider(StrEnum):
    """An enumeration of Algorand API providers."""

    LOCALHOST = auto()
    CUSTOM = auto()
    ALGONODE = auto()


AlgorandApiProviderChoice: TypeAlias = Literal[
    AlgorandApiProvider.LOCALHOST,
    AlgorandApiProvider.CUSTOM,
    AlgorandApiProvider.ALGONODE,
]
