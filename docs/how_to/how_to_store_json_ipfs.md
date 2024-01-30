# How to Store JSON in IPFS

## ⚠️ Warning

This library is in the early stages of development.

The API is not stable and the code has not been audited.

## Context

`algobase` provides an easy way to upload JSON to [IPFS](https://ipfs.tech/) using [nft.storage](https://nft.storage/).

[nft.storage](https://nft.storage/) provides a free [IPFS](https://ipfs.tech/) pinning service.

## Set Up

Make sure `algobase` is intalled before you start this tutorial (see intructions [here](https://github.com/code-alexander/algobase/blob/main/README.md)).

Sign up for an [nft.storage account](https://nft.storage/docs/#create-an-account) and create an [API key](https://nft.storage/docs/#get-an-api-token).

You will need to set the API key as an environment variable called `NFT_STORAGE_API_KEY`, or add it to your .env file.

To set the environment variable in Python:

```python
import os

os.environ["NFT_STORAGE_API_KEY"] = "<your-api-key>"
```

`algobase` uses the [dotenv](https://github.com/theskumar/python-dotenv/tree/main?tab=readme-ov-file#command-line-interface) library. You can use its CLI to set the variable:

```
dotenv set NFT_STORAGE_API_KEY <your-api-key>
```

## How to Store JSON in IPFS

```python
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
```