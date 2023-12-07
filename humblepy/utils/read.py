"""Functions for reading and caching reference data files."""

import tomllib
from functools import cache


@cache
def read_ipfs_gateways() -> list[str]:
    """Read IPFS gateways from the reference data file.

    Returns:
        list[str]: The list of IPFS gateways.
    """
    with open("humblepy/data/ipfs.toml", "rb") as f:
        data = tomllib.load(f)
    return list(data["ipfs_gateways"])
