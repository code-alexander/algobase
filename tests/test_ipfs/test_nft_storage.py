"""Tests the nft.storage IPFS."""

from functools import reduce

import httpx
import pytest
from _pytest.monkeypatch import MonkeyPatch
from pytest_httpx import HTTPXMock

from algobase.choices import IpfsProvider, IpfsProviderChoice
from algobase.ipfs.nft_storage import NftStorage
from algobase.settings import Settings
from tests.types import FixtureDict


class TestNftStorage:
    """Tests the NftStorage client class."""

    def test_from_settings_constructor(self) -> None:
        """Test that the client can be created from a settings object."""
        settings = Settings()
        settings.nft_storage_api_key = "test_api_key"
        test_client = NftStorage.from_settings(settings)
        assert isinstance(test_client, NftStorage)

    @pytest.mark.parametrize(
        "attribute, value",
        [
            ("api_version", "1.0"),
            ("base_url", "https://api.nft.storage"),
            ("is_api_key_required", True),
            ("ipfs_provider_name", IpfsProvider.NFT_STORAGE),
            ("api_key", "test_api_key"),
        ],
    )
    def test_properties(
        self,
        attribute: str,
        value: str | bool | IpfsProviderChoice,
    ) -> None:
        """Test that the client has the required abstract properties."""
        test_client = NftStorage(_api_key="test_api_key")
        assert getattr(test_client, attribute) == value

    def test_api_key_missing(self, monkeypatch: MonkeyPatch) -> None:
        """Test that the client raises an error if the API key is missing."""
        with pytest.raises(ValueError):
            NftStorage(_api_key=None)

    def test_store_json_successful(
        self,
        httpx_mock: HTTPXMock,
        nft_storage_store_json_successful: FixtureDict,
    ) -> None:
        """Test that a CID is returned when JSON is successfully stored in IPFS (response is mocked)."""
        httpx_mock.add_response(json=nft_storage_store_json_successful)
        test_client = NftStorage(_api_key="test_api_key")
        assert (
            test_client.store_json(
                json='{"integer": 123, "boolean": true, "list": ["a", "b", "c"]}'
            )
            == "bafkreic7xfupwwdiwnzudgi6s6brjunxktdfio4hj4a5tlp2hrou7rnjvy"
        )

    @pytest.mark.parametrize(
        "keys, value",
        [
            (["ok"], False),
            (["ok"], None),
            (["value", "cid"], None),
        ],
    )
    def test_store_json_cid_is_none(
        self,
        httpx_mock: HTTPXMock,
        nft_storage_store_json_successful: FixtureDict,
        keys: list[str],
        value: bool | None,
    ) -> None:
        """Test that an error is raise when a 200 response is returned but "ok" is False or "cid" is None (response is mocked)."""
        response_dict = nft_storage_store_json_successful
        reduce(dict.__getitem__, keys[:-1], response_dict)[keys[-1]] = value

        httpx_mock.add_response(json=response_dict)

        test_client = NftStorage(_api_key="test_api_key")
        with pytest.raises(httpx.HTTPError):
            test_client.store_json(
                json='{"integer": 123, "boolean": true, "list": ["a", "b", "c"]}'
            )

    def test_nft_storage_store_json_bad_request(
        self,
        httpx_mock: HTTPXMock,
        nft_storage_store_json_bad_request: FixtureDict,
    ) -> None:
        """Test that an error is raised when a 400 response is returned (response is mocked)."""
        httpx_mock.add_response(
            json=nft_storage_store_json_bad_request, status_code=400
        )

        test_client = NftStorage(_api_key="test_api_key")
        with pytest.raises(httpx.HTTPError):
            test_client.store_json(
                json='{"integer": 123, "boolean": true, "list": ["a", "b", "c"]}'
            )

    def test_nft_storage_store_json_unauthorized(
        self,
        httpx_mock: HTTPXMock,
        nft_storage_store_json_unauthorized: FixtureDict,
    ) -> None:
        """Test that an error is raised when a 401 response is returned (response is mocked)."""
        httpx_mock.add_response(
            json=nft_storage_store_json_unauthorized, status_code=401
        )

        test_client = NftStorage(_api_key="test_api_key")
        with pytest.raises(httpx.HTTPError):
            test_client.store_json(
                json='{"integer": 123, "boolean": true, "list": ["a", "b", "c"]}'
            )

    def test_nft_storage_store_json_forbidden(
        self,
        httpx_mock: HTTPXMock,
        nft_storage_store_json_forbidden: FixtureDict,
    ) -> None:
        """Test that an error is raised when a 403 response is returned (response is mocked)."""
        httpx_mock.add_response(json=nft_storage_store_json_forbidden, status_code=403)

        test_client = NftStorage(_api_key="test_api_key")
        with pytest.raises(httpx.HTTPError):
            test_client.store_json(
                json='{"integer": 123, "boolean": true, "list": ["a", "b", "c"]}'
            )

    def test_nft_storage_store_json_internal_server_error(
        self,
        httpx_mock: HTTPXMock,
        nft_storage_store_json_internal_server_error: FixtureDict,
    ) -> None:
        """Test that an error is raised when a 500 response is returned (response is mocked)."""
        httpx_mock.add_response(
            json=nft_storage_store_json_internal_server_error, status_code=500
        )

        test_client = NftStorage(_api_key="test_api_key")
        with pytest.raises(httpx.HTTPError):
            test_client.store_json(
                json='{"integer": 123, "boolean": true, "list": ["a", "b", "c"]}'
            )

    def test_fetch_pin_status_successful(
        self,
        httpx_mock: HTTPXMock,
        nft_storage_fetch_pin_status_successful: FixtureDict,
    ) -> None:
        """Test that a pin status is returned when a pin status is successfully checked from nft.storage (response is mocked)."""
        httpx_mock.add_response(json=nft_storage_fetch_pin_status_successful)

        test_client = NftStorage(_api_key="test_api_key")
        assert (
            test_client.fetch_pin_status(
                cid="bafkreic7xfupwwdiwnzudgi6s6brjunxktdfio4hj4a5tlp2hrou7rnjvy"
            )
            == "pinned"
        )

    @pytest.mark.parametrize(
        "keys, value",
        [
            (["ok"], False),
            (["ok"], None),
            (["value", "pin", "status"], None),
            (["value", "pin", "status"], "invalid_status"),
            (["value", "pin", "status"], "queueing"),
        ],
    )
    def test_fetch_pin_status_invalid_status_or_none(
        self,
        httpx_mock: HTTPXMock,
        nft_storage_fetch_pin_status_successful: FixtureDict,
        keys: list[str],
        value: bool | None,
    ) -> None:
        """Test that an error is raise when a 200 response is returned but "ok" is False or pin status is None or invalid. (response is mocked)."""
        response_dict = nft_storage_fetch_pin_status_successful
        reduce(dict.__getitem__, keys[:-1], response_dict)[keys[-1]] = value

        httpx_mock.add_response(json=response_dict)

        test_client = NftStorage(_api_key="test_api_key")
        with pytest.raises(httpx.HTTPError):
            test_client.fetch_pin_status(
                cid="bafkreic7xfupwwdiwnzudgi6s6brjunxktdfio4hj4a5tlp2hrou7rnjvy"
            )

    def test_fetch_pin_status_not_found(
        self,
        httpx_mock: HTTPXMock,
        nft_storage_fetch_pin_status_not_found: FixtureDict,
    ) -> None:
        """Test that an error is raised when a 400 response is returned (response is mocked)."""
        httpx_mock.add_response(
            json=nft_storage_fetch_pin_status_not_found, status_code=400
        )

        test_client = NftStorage(_api_key="test_api_key")
        with pytest.raises(httpx.HTTPError):
            test_client.fetch_pin_status(cid="0")

    def test_fetch_pin_status_internal_server_error(
        self,
        httpx_mock: HTTPXMock,
        nft_storage_fetch_pin_status_internal_server_error: FixtureDict,
    ) -> None:
        """Test that an error is raised when a 500 response is returned (response is mocked)."""
        httpx_mock.add_response(
            json=nft_storage_fetch_pin_status_internal_server_error, status_code=500
        )

        test_client = NftStorage(_api_key="test_api_key")
        with pytest.raises(httpx.HTTPError):
            test_client.fetch_pin_status(cid="0")
