"""Example showing how to store JSON in IPFS.

Make sure the environment variable `AB_NFT_STORAGE_API_KEY` is set before running.
"""

from algobase.ipfs.nft_storage import NftStorage

# Instantiate the client object
client = NftStorage()

# Store JSON in IPFS (returns the CID of the file if successful)
cid = client.store_json(
    json='{"integer": 123, "boolean": true, "list": ["a", "b", "c"]}'
)

print(f"Stored JSON on IPFS with CID {cid}")
"""
Stored JSON on IPFS with CID bafkreiaci6q6dolsy32cnqhtmgvf23gzphzzc7urfnka2omgzn7behvbx4
"""

# Check IPFS pin status ('queued', 'pinning', 'pinned', or 'failed')
pin_status = client.fetch_pin_status(cid)

print(f"IPFS pin status for CID {cid} is '{pin_status}'")
"""
IPFS pin status for CID bafkreiaci6q6dolsy32cnqhtmgvf23gzphzzc7urfnka2omgzn7behvbx4 is 'pinned'
"""
