# How to Mint an ARC-3 NFT on LocalNet

## ⚠️ Warning

This library is in the early stages of development.

The API is not stable and the code has not been audited.

## Context

`algobase` makes it easy to mint ARC-3 NFTs on Algorand and upload metadata to IPFS.

This tutorial uses [nft.storage](https://nft.storage/), which provides a free [IPFS](https://ipfs.tech/) pinning service.

For more information on ARC standards, check out these resources:

- [ARC Token Standards Explained for NFT Creators](https://www.algorand.foundation/news/arc-token-standards-explained-for-nft-creators)
- [Algorand Requests for Comments (ARCs)](https://arc.algorand.foundation/)

## Set Up

Make sure `algobase` is intalled before you start this tutorial (see intructions [here](https://github.com/code-alexander/algobase/blob/main/README.md)).

You will also need to install [algokit](https://developer.algorand.org/docs/get-started/algokit/) and start a [LocalNet](https://developer.algorand.org/docs/get-started/algokit/#start-a-localnet) instance with the following command:
`algokit localnet start`

If you want to store your NFT's metadata in IPFS using [nft.storage](https://nft.storage/), you can sign for an [nft.storage account](https://nft.storage/docs/#create-an-account) and create an [API key](https://nft.storage/docs/#get-an-api-token).

You will need to set the API key as an environment variable called `AB_NFT_STORAGE_API_KEY`, or add it to your .env file.

Follow our [IPFS tutorial](https://code-alexander.github.io/algobase/how_to/how_to_store_json_ipfs/) if you get stuck 🤗

## Mint an ARC-3 NFT

```python
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
```
