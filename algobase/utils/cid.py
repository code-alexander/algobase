"""Utility functions for working with IPFS content identifiers (CIDs)."""

import multihash
from algosdk import encoding
from multiformats_cid import make_cid  # type: ignore[attr-defined]
from pydantic import TypeAdapter
from returns.pipeline import flow

from algobase.types.annotated import AlgorandAddress


def cid_to_algorand_address(cid: str) -> AlgorandAddress:
    """Converts a CID to an Algorand address.

    This is used in ARC-19: https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0019.md

    Args:
        cid (str): The CID to convert.

    Returns:
        AlgorandAddress: The Algorand address.
    """
    return flow(
        make_cid(cid).multihash,
        lambda h: multihash.decode(h).digest,
        encoding.encode_address,
        TypeAdapter(AlgorandAddress).validate_python,
    )


print(cid_to_algorand_address("QmQZyq4b89RfaUw8GESPd2re4hJqB8bnm4kVHNtyQrHnnK"))
print(type(cid_to_algorand_address("QmQZyq4b89RfaUw8GESPd2re4hJqB8bnm4kVHNtyQrHnnK")))
