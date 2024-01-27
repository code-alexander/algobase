"""Pytest fixtures for the models tests."""

from copy import deepcopy

import pytest

from tests.types import FixtureDict

arc3_metadata = {
    "name": "My Song",
    "decimals": 0,
    "description": "My first and best song!",
    "image": "https://s3.amazonaws.com/your-bucket/song/cover/mysong.png",
    "image_integrity": "sha256-47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=",
    "image_mimetype": "image/png",
    "background_color": "FFFFFF",
    "external_url": "https://mysongs.com/song/mysong",
    "external_url_integrity": "sha256-7IGatqxLhUYkruDsEva52Ku43up6774yAmf0k98MXnU=",
    "external_url_mimetype": "text/html",
    "animation_url": "https://s3.amazonaws.com/your-bucket/song/preview/mysong.ogg",
    "animation_url_integrity": "sha256-LwArA6xMdnFF3bvQjwODpeTG/RVn61weQSuoRyynA1I=",
    "animation_url_mimetype": "audio/ogg",
    "properties": {
        "traits": {
            "background": "red",
            "shirt_color": "blue",
            "glasses": "none",
            "tattoos": 4,
        },
        "simple_property": "example value",
        "rich_property": {
            "name": "Name",
            "value": "123",
            "display_value": "123 Example Value",
            "class": "emphasis",
            "css": {
                "color": "#ffffff",
                "font-weight": "bold",
                "text-decoration": "underline",
            },
        },
        "valid_types": {
            "string": "Name",
            "int": 1,
            "float": 3.14,
            "list": ["a", "b", "c"],
        },
        "array_property": {
            "name": "Name",
            "value": [1, 2, 3, 4],
            "class": "emphasis",
        },
    },
    "extra_metadata": "iHcUslDaL/jEM/oTxqEX++4CS8o3+IZp7/V5Rgchqwc=",
    "localization": {
        "uri": "ipfs://QmWS1VAdMD353A6SDk9wNyvkT14kyCiZrNDYAad4w1tKqT/{locale}.json",
        "default": "en",
        "locales": ["en", "es", "fr"],
        "integrity": {
            "es": "sha256-T0UofLOqdamWQDLok4vy/OcetEFzD8dRLig4229138Y=",
            "fr": "sha256-UUM89QQlXRlerdzVfatUzvNrEI/gwsgsN/lGkR13CKw=",
        },
    },
}


@pytest.fixture
def arc3_metadata_fixture() -> FixtureDict:
    """Pytest fixture for a dictionary containing valid ARC-3 metadata.

    Returns:
        FixtureDict: The dictionary of valid ARC-3 metadata.
    """
    return deepcopy(arc3_metadata)


@pytest.fixture
def arc3_metadata_with_extra_metadata() -> FixtureDict:
    """Pytest fixture for a dictionary containing valid ARC-3 metadata.

    This is the 'extra metadata' example from the ARC-3 spec:
    https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0003.md

    Returns:
        FixtureDict: he dictionary of valid ARC-3 metadata
    """
    return {
        "name": "My Picture",
        "description": "Lorem ipsum...",
        "image": "https://s3.amazonaws.com/your-bucket/images/{id}.png",
        "image_integrity": "sha256-47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=",
        "image_mimetype": "image/png",
        "external_url": "https://mysongs.com/song/{id}",
        "extra_metadata": "iHcUslDaL/jEM/oTxqEX++4CS8o3+IZp7/V5Rgchqwc=",
    }


@pytest.fixture
def asa_nft_fixture() -> FixtureDict:
    """Pytest fixture for a dictionary containing valid ASA data.

    Returns:
        FixtureDict: The dictionary of valid ASA data.
    """
    return {
        "asset_params": {
            "total": 1,
            "decimals": 0,
            "default_frozen": False,
            "unit_name": "USDT",
            "asset_name": "My Song",
            "url": "https://tether.to/#arc3",
            "metadata_hash": b"fACPO4nRgO55j1ndAK3W6Sgc4APkcyFh",
            "manager": "7ZUECA7HFLZTXENRV24SHLU4AVPUTMTTDUFUBNBD64C73F3UHRTHAIOF6Q",
            "reserve": "7ZUECA7HFLZTXENRV24SHLU4AVPUTMTTDUFUBNBD64C73F3UHRTHAIOF6Q",
            "freeze": "7ZUECA7HFLZTXENRV24SHLU4AVPUTMTTDUFUBNBD64C73F3UHRTHAIOF6Q",
            "clawback": "7ZUECA7HFLZTXENRV24SHLU4AVPUTMTTDUFUBNBD64C73F3UHRTHAIOF6Q",
        },
        "metadata": deepcopy(arc3_metadata),
    }


@pytest.fixture
def asa_nft_extra_metadata_fixture() -> FixtureDict:
    """Pytest fixture for a dictionary containing valid ASA data.

    Returns:
        FixtureDict: The dictionary of valid ASA data.
    """
    return {
        "asset_params": {
            "total": 1,
            "decimals": 0,
            "default_frozen": False,
            "unit_name": "USDT",
            "asset_name": "My Picture",
            "url": "https://tether.to/#arc3",
            "metadata_hash": b"fACPO4nRgO55j1ndAK3W6Sgc4APkcyFh",
            "manager": "7ZUECA7HFLZTXENRV24SHLU4AVPUTMTTDUFUBNBD64C73F3UHRTHAIOF6Q",
            "reserve": "7ZUECA7HFLZTXENRV24SHLU4AVPUTMTTDUFUBNBD64C73F3UHRTHAIOF6Q",
            "freeze": "7ZUECA7HFLZTXENRV24SHLU4AVPUTMTTDUFUBNBD64C73F3UHRTHAIOF6Q",
            "clawback": "7ZUECA7HFLZTXENRV24SHLU4AVPUTMTTDUFUBNBD64C73F3UHRTHAIOF6Q",
        },
        "metadata": {
            "name": "My Picture",
            "description": "Lorem ipsum...",
            "image": "https://s3.amazonaws.com/your-bucket/images/{id}.png",
            "image_integrity": "sha256-47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=",
            "image_mimetype": "image/png",
            "external_url": "https://mysongs.com/song/{id}",
            "extra_metadata": "iHcUslDaL/jEM/oTxqEX++4CS8o3+IZp7/V5Rgchqwc=",
        },
    }
