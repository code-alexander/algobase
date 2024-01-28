"""Functions for reading and caching reference data files."""

import mimetypes
import tomllib


def read_ipfs_gateways() -> list[str]:
    """Read IPFS gateways from the reference data file.

    Returns:
        list[str]: The list of IPFS gateways.
    """
    with open("algobase/data/ipfs.toml", "rb") as f:
        data = tomllib.load(f)
    return list(data["ipfs_gateways"])


def read_mime_types() -> list[str]:
    """Read MIME types from the reference data file.

    Returns:
        list[str]: The list of MIME types.
    """
    mimetypes.init()
    return list(mimetypes.types_map.values())
