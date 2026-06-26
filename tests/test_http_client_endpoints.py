"""Unit tests for HttpClient endpoint URL and payload construction."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from youversion.config import Config
from youversion.core.http_client import HttpClient


@pytest.fixture
def http_client():
    """HttpClient with a mocked underlying httpx client."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "response": {"code": 200, "data": {"ok": True}},
    }
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.post = AsyncMock(return_value=mock_response)
    return HttpClient(mock_client, user_id=42)


@pytest.mark.asyncio
async def test_get_friends_uses_friends_service(http_client):
    """Friends list should call friends.youversionapi.com items endpoint."""
    await http_client.get_friends(page=2)
    call = http_client._client.get.await_args
    assert call.args[0] == f"{Config.FRIENDS_API_BASE}{Config.FRIENDS_ITEMS_URL}"
    assert call.kwargs["params"] == {"page": 2}


@pytest.mark.asyncio
async def test_delete_friend_posts_json_body(http_client):
    """Delete friend should POST JSON, not query params."""
    await http_client.delete_friend(99)
    call = http_client._client.post.await_args
    assert call.args[0] == f"{Config.FRIENDS_API_BASE}{Config.FRIENDS_DELETE_URL}"
    assert call.kwargs["json"] == {"user_id": 99}


@pytest.mark.asyncio
async def test_delete_saved_event_posts_json_body(http_client):
    """Delete saved event should POST JSON id field."""
    await http_client.delete_saved_event(123)
    call = http_client._client.post.await_args
    assert call.args[0] == f"{Config.EVENTS_API_BASE}{Config.EVENTS_DELETE_SAVED_URL}"
    assert call.kwargs["json"] == {"id": 123}


@pytest.mark.asyncio
async def test_register_device_posts_json_body(http_client):
    """Device registration should send JSON payload."""
    await http_client.register_device("device-1", user_id=42)
    call = http_client._client.post.await_args
    assert call.kwargs["json"]["id"] == "device-1"
    assert call.kwargs["json"]["user_id"] == 42


@pytest.mark.asyncio
async def test_get_notifications_uses_notifications_service(http_client):
    """Notifications feed should hit notifications API."""
    await http_client.get_notifications()
    call = http_client._client.get.await_args
    assert call.args[0] == (
        f"{Config.NOTIFICATIONS_API_BASE}{Config.NOTIFICATIONS_ITEMS_URL}"
    )


@pytest.mark.asyncio
async def test_get_notification_settings_is_get(http_client):
    """Notification settings should be fetched with GET."""
    await http_client.get_notification_settings()
    call = http_client._client.get.await_args
    assert call.args[0] == (
        f"{Config.NOTIFICATIONS_API_BASE}{Config.NOTIFICATIONS_SETTINGS_URL}"
    )


@pytest.mark.asyncio
async def test_get_friend_suggestions_includes_language_tag(http_client):
    """Friend suggestions require ISO 639-1 language_tag (e.g. en)."""
    await http_client.get_friend_suggestions(page=1)
    call = http_client._client.get.await_args
    assert call.kwargs["params"]["language_tag"] == "en"


@pytest.mark.asyncio
async def test_get_moments_configuration_uses_public_client(http_client):
    """Moments configuration rejects Authorization and must use public GET."""
    public = MagicMock()
    public.get = AsyncMock(return_value=http_client._client.get.return_value)
    http_client._public_client = public
    await http_client.get_moments_configuration()
    public.get.assert_awaited_once()
    http_client._client.get.assert_not_awaited()
