"""Tests for the CID utility functions."""

from algobase.utils.cid import cid_to_algorand_address


def test_cid_to_algorand_address() -> None:
    """Test the cid_to_algorand_address() function."""
    # Test case comes from: https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0019.md
    assert (
        cid_to_algorand_address("QmQZyq4b89RfaUw8GESPd2re4hJqB8bnm4kVHNtyQrHnnK")
        == "EEQYWGGBHRDAMTEVDPVOSDVX3HJQIG6K6IVNR3RXHYOHV64ZWAEISS4CTI"
    )
