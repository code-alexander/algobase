# How to Validate ARC-3 Assets and Metadata

## ⚠️ Warning

This library is in the early stages of development.

The API is not stable and the code has not been audited.

## Context

`algobase` provides [Pydantic](https://github.com/pydantic/pydantic) models for validating [Algorand ARC-3](https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0003.md) assets and metadata.

There are three sets of constraints that must be adhered to:

- Constraints on the asset parameters (applies to all ASAs)
- Constraints on the JSON metadata
- Constraints on the combination of values in the ASA [asset parameters](https://developer.algorand.org/docs/get-details/transactions/transactions/#asset-parameters) and the JSON metadata

`algobase` provides models for validating the JSON metadata on its own, and in combination with the asset parameters.

## Set Up

Make sure `algobase` is intalled before you start this tutorial (see intructions [here](https://github.com/code-alexander/algobase/blob/main/README.md)).

## Understanding Pydantic

There are multiple ways to instantiate a model in [Pydantic](https://github.com/pydantic/pydantic).

Given a User model:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int | None
```

There are multiple ways to instantiate a Pydantic model and validate your data:

```python
# Using keyword arguments
>>> User(name="Sam", age=50)
User(name='Sam', age=50)

# Using dict unpacking
>>> User(**{"name": "Sam", "age": 50})
User(name='Sam', age=50)

# Passing a dict to the model_validate() classmethod
>>> User.model_validate({"name": "Sam", "age": 50})
User(name='Sam', age=50)

# Passing a json string to the model_validate() classmethod
>>> User.model_validate_json('{"name": "Sam", "age": 50}')
User(name='Sam', age=50)
```

By default, [Pydantic](https://github.com/pydantic/pydantic) will try to coerce your input data to the required type:

```python
# Using keyword arguments
>>> User(name="Sam", age="50")
User(name='Sam', age=50)
```

You can disable this by using [strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/):

```python
# Lax mode (default)
>>> User.model_validate({"name": "Sam", "age": "50"})
User(name='Sam', age=50)

# Strict mode
>>> User.model_validate({"name": "Sam", "age": "50"}, strict=True)
ValidationError: 1 validation error for User
age
  Input should be a valid integer [type=int_type, input_value='50', input_type=str]
    For further information visit https://errors.pydantic.dev/2.5/v/int_type
```

## Validating ASA Asset Parameters

To validate the asset parameters without checking the JSON metadata:

```python
from algobase.models.asset_params import AssetParams

# Define ASA asset params dict
asset_params = {
        "total": 1,
        "decimals": 0,
        "default_frozen": False,
        "unit_name": "USDT",
        "asset_name": "Tether",
        "url": "https://tether.to/",
        "metadata_hash": b"fACPO4nRgO55j1ndAK3W6Sgc4APkcyFh",
        "manager": "7ZUECA7HFLZTXENRV24SHLU4AVPUTMTTDUFUBNBD64C73F3UHRTHAIOF6Q",
        "reserve": "7ZUECA7HFLZTXENRV24SHLU4AVPUTMTTDUFUBNBD64C73F3UHRTHAIOF6Q",
        "freeze": "7ZUECA7HFLZTXENRV24SHLU4AVPUTMTTDUFUBNBD64C73F3UHRTHAIOF6Q",
        "clawback": "7ZUECA7HFLZTXENRV24SHLU4AVPUTMTTDUFUBNBD64C73F3UHRTHAIOF6Q",
    }

# Validate the asset params data
AssetParams.model_validate(asset_params)
```

## Validating ARC-3 JSON Metadata

To validate JSON metadata without checking the ASA parameters:

```python
from algobase.models.arc3 import Arc3Metadata

# Define dict containing both asset params and metadata
data = {
        "asset_params": {
            "total": 1,
            "decimals": 0,
            "default_frozen": False,
            "unit_name": "Song0001",
            "asset_name": "My Songs",
            "url": "https://tether.to/#arc3",
            "metadata_hash": b"fACPO4nRgO55j1ndAK3W6Sgc4APkcyFh",
            "manager": "7ZUECA7HFLZTXENRV24SHLU4AVPUTMTTDUFUBNBD64C73F3UHRTHAIOF6Q",
            "reserve": "7ZUECA7HFLZTXENRV24SHLU4AVPUTMTTDUFUBNBD64C73F3UHRTHAIOF6Q",
            "freeze": "7ZUECA7HFLZTXENRV24SHLU4AVPUTMTTDUFUBNBD64C73F3UHRTHAIOF6Q",
            "clawback": "7ZUECA7HFLZTXENRV24SHLU4AVPUTMTTDUFUBNBD64C73F3UHRTHAIOF6Q",
        },
        "metadata": {
            "arc": "arc3",
            "name": "My Songs",
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
    }

# Validate the data
Asa.model_validate(data)
```

## Validating ARC-3 Asset Parameters and JSON Metadata

To validate a combination of asset parameters and JSON metadata:

```python
from algobase.models.asa import Asa

# Define dict containing both asset params and metadata
data = {
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
        "metadata": {
            "arc": "arc3",
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
    }

# Validate the data
Asa.model_validate(data)
```

The extra field (`"arc": "arc3"`) is mandatory when validating a dict against the ASA model, if the `metadata` field is not None.

It will be excluded from model serialization, but is needed for a [discriminated union](https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions).
