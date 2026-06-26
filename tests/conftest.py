"""Shared pytest fixtures for integration result recording."""

from __future__ import annotations

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tests.integration_recorder import flush_manifest, make_run_dir
from youversion.clients.sync_client import SyncClient
from youversion.core.http_client import HttpClient
from youversion.enums import MomentKinds, StatusEnum

_integration_run_dir = None

CARDS_RESPONSE = {"moments": [{"id": 1, "kind_id": "note", "extras": {}}]}
DEFAULT_RESPONSE = {"ok": True}
VOTD_RESPONSE = {
    "votd": [
        {
            "day": datetime.now().timetuple().tm_yday,
            "usfm": ["JHN.3.16"],
            "image_id": None,
        }
    ],
}

CREATE_MOMENT_DATA = {
    "kind": MomentKinds.NOTE,
    "content": "Test content",
    "references": [
        {"human": "John 3:16", "version_id": 1, "usfm": ["JHN.3.16"]},
    ],
    "title": "Test Title",
    "status": StatusEnum.PRIVATE,
    "body": "Test body",
    "color": "ff0000",
    "labels": ["test"],
    "language_tag": "en",
}


def make_mock_http_client() -> MagicMock:
    """Build a mock HttpClient with AsyncMock on every public method."""
    mock = MagicMock(spec=HttpClient)
    for name in dir(HttpClient):
        if name.startswith("_"):
            continue
        attr = getattr(HttpClient, name)
        if not callable(attr):
            continue
        if name == "get_cards":
            mock_method = AsyncMock(return_value=CARDS_RESPONSE)
        elif name == "get_verse_of_the_day":
            mock_method = AsyncMock(return_value=VOTD_RESPONSE)
        else:
            mock_method = AsyncMock(return_value=DEFAULT_RESPONSE)
        setattr(mock, name, mock_method)
    return mock


@pytest.fixture
def mocked_sync_client():
    """SyncClient with mocked auth and HTTP layer (no real API calls)."""
    with patch("youversion.core.base_client.Authenticator") as mock_auth_cls:
        mock_auth = MagicMock()
        mock_auth.username = "testuser"
        mock_auth.password = "testpass"
        mock_auth_cls.return_value = mock_auth

        client = SyncClient(username="testuser", password="testpass")
        client._http_client = make_mock_http_client()
        client._user_id = 42
        client._access_token = "token"
        yield client
        if client._loop and not client._loop.is_closed():
            client._loop.close()


@pytest.fixture(scope="session")
def integration_results_dir():
    """Directory where this session's live API results are stored."""
    global _integration_run_dir
    _integration_run_dir = make_run_dir()
    return _integration_run_dir


def pytest_sessionfinish(session, exitstatus):
    """Write manifest.json after integration tests record HTTP traffic."""
    if _integration_run_dir is not None:
        flush_manifest(_integration_run_dir)
