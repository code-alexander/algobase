"""Utilities for minting assets on Algorand with sensible defaults."""


# def create_asset_config_txn(client: AlgodClient, account: Account, asa: Asa) -> AssetConfigTxn:

#     return AssetConfigTxn(
#         sender=account.address,
#         sp=client.suggested_params(),
#         index=None,
#         total=asa.asset_params.total,
#         default_frozen=False,
#         unit_name=asa.asset_params.unit_name,
#         asset_name=asa.asset_params.asset_name,
#         manager=account.address,
#         reserve=account.address,
#         freeze=None,
#         clawback=None,
#         url=asa.asset_params.url,
#         metadata_hash=asa.metadata_hash,
#         note=None,
#         lease=None,
#         strict_empty_address_check=False,
#         decimals=asa.asset_params.decimals,
#         rekey_to=None,
#     )
