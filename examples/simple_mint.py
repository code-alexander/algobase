"""Example showing how to mint an NFT on an Algorand localnet.

To run this example, make sure you have localnet running.
You can follow the guide here: https://developer.algorand.org/docs/get-started/algokit/#start-a-localnet

The metadata for this NFT is stored in IPFS using the NFT Storage API.
It requires the environment variable `AB_NFT_STORAGE_API_KEY` to be set.
"""

from datetime import datetime

from algobase.algorand.client import (
    create_localnet_algod_client,
    get_default_account,
)
from algobase.algorand.simple_mint import create_metadata, mint
from algobase.ipfs.nft_storage import NftStorage
from algobase.settings import Settings

# Fetch settings from the environment
settings = Settings()

# Instantiate Algod client
algod_client = create_localnet_algod_client()

# Get the default localnet account
account = get_default_account(algod_client)

# Define the ARC-3 metadata for the NFT
metadata = create_metadata(
    description="My first NFT!",
    properties={
        "creator": account.address,
        "created_at": datetime.now().isoformat(),
    },
)

# Instantiate IPFS client
ipfs_client = settings | NftStorage.from_settings

# Store the metadata JSON in IPFS and get the CID
cid = ipfs_client.store_json(metadata.json_bytes)

print(f"Stored JSON on IPFS with CID {cid}")
print(f"View the metadata at https://nftstorage.link/ipfs/{cid}")
"""
Stored JSON on IPFS with CID bafkreif2cduyjxdljxaydxxiryxdiw5arljif745e46fv3sajkxwqvvtzq
View the metadata at https://nftstorage.link/ipfs/bafkreif2cduyjxdljxaydxxiryxdiw5arljif745e46fv3sajkxwqvvtzq
"""

# Mint the NFT on localnet
asset_id = mint(
    algod_client=algod_client,
    account=account,
    metadata=metadata,
    cid=cid,
)

print(f"NFT minted! Asset ID: {asset_id}")
print(f"View the asset in Dappflow: https://app.dappflow.org/explorer/asset/{asset_id}")
"""
NFT minted! Asset ID: 1008
View the asset in Dappflow: https://app.dappflow.org/explorer/asset/1008
"""
