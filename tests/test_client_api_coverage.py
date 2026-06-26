"""Parametrized API coverage tests with mocked HTTP (no real API calls)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tests.conftest import CREATE_MOMENT_DATA, make_mock_http_client
from youversion.clients.sync_client import SyncClient

# method_name -> positional args tuple
SYNC_API_CALLS: dict[str, tuple] = {
    "moments": (),
    "highlights": (),
    "verse_of_the_day": (),
    "notes": (),
    "bookmarks": (),
    "my_images": (),
    "plan_progress": (),
    "plan_subscriptions": (),
    "plan_completions": (),
    "send_friend_request": (99,),
    "get_bible_configuration": (),
    "get_bible_versions": (),
    "get_bible_version": (1,),
    "get_bible_chapter": ("GEN.1",),
    "get_recommended_languages": (),
    "get_audio_chapter": ("GEN.1",),
    "get_audio_version": (1,),
    "search_bible": ("love",),
    "search_plans": ("faith",),
    "search_users": ("john",),
    "get_videos": (),
    "get_video_details": (1,),
    "get_images": ("GEN.1",),
    "get_image_upload_url": (),
    "search_events": ("church",),
    "get_event_details": (1,),
    "get_saved_events": (),
    "save_event": (1,),
    "delete_saved_event": (1,),
    "get_all_saved_event_ids": (),
    "get_event_configuration": (),
    "get_moments": (),
    "get_moment_details": (1,),
    "create_moment": (CREATE_MOMENT_DATA,),
    "update_moment": ({"id": 1, "content": "updated"},),
    "delete_moment": (1,),
    "get_moment_colors": (),
    "get_moment_labels": (),
    "get_verse_colors": ("JHN.3.16", 1),
    "hide_verse_colors": ({"usfm": "JHN.3.16", "version_id": 1},),
    "get_moments_configuration": (),
    "create_comment": (1, "hello"),
    "delete_comment": (1,),
    "like_moment": (1,),
    "unlike_moment": (1,),
    "register_device": ("device-1",),
    "unregister_device": ("device-1",),
    "get_themes": (),
    "add_theme": (
        1,
        ["en"],
        {"primary": "#ffffff"},
        {"url": "https://example.com"},
        "suffix",
        {"en": 1},
    ),
    "remove_theme": (1,),
    "set_theme": (1,),
    "get_theme_description": (1,),
    "get_friends": (),
    "get_all_friends": (),
    "delete_friend": (99,),
    "get_incoming_friend_requests": (),
    "get_friend_suggestions": (),
    "accept_friend_request": (99,),
    "decline_friend_request": (99,),
    "dismiss_friend_suggestion": (99,),
    "get_facebook_friends": (),
    "sync_friendship_contacts": ([{"name": "Alice", "email": "a@b.com"}],),
    "get_notifications": (),
    "get_notification_settings": (),
    "update_notification_settings": ({"email": True},),
    "update_notifications": ({"read": [1]},),
    "get_votd_notification_settings": (),
    "update_votd_notification_settings": ({"enabled": True},),
    "invite_by_email": ({"emails": ["a@b.com"]},),
    "invite_by_sms": ({"phones": ["+15551234567"]},),
    "get_client_side_moments": (),
    "get_moments_votd": (),
}


@pytest.mark.parametrize("method_name", list(SYNC_API_CALLS.keys()))
def test_sync_client_api_method(mocked_sync_client, method_name):
    """Each SyncClient wrapper delegates through mocked HTTP."""
    method = getattr(mocked_sync_client, method_name)
    result = method(*SYNC_API_CALLS[method_name])
    assert result is not None


def test_sync_client_username_from_authenticator(mocked_sync_client):
    """username property reads from authenticator when available."""
    mocked_sync_client._authenticator.username = "auth-user"
    assert mocked_sync_client.username == "auth-user"


def test_sync_client_convert_note_to_md(mocked_sync_client):
    """convert_note_to_md sync wrapper delegates to async implementation."""
    from youversion.core.base_client import BaseClient

    with patch.object(
        BaseClient,
        "convert_note_to_md",
        new_callable=AsyncMock,
        return_value=[{"id": 1}],
    ):
        result = mocked_sync_client.convert_note_to_md()
    assert result == [{"id": 1}]


def test_sync_client_context_manager(mocked_sync_client):
    """Context manager enter/exit runs without real API calls."""
    with mocked_sync_client:
        pass


def test_sync_client_username_fallback():
    """username property falls back to _username when auth is absent."""
    with patch("youversion.core.base_client.Authenticator") as mock_auth_cls:
        mock_auth = MagicMock(spec=[])
        mock_auth_cls.return_value = mock_auth
        client = SyncClient(username="stored")
        client._authenticator = mock_auth
        assert client.username == "stored"


def test_sync_client_close_loop_owner_without_loop(mocked_sync_client):
    """close() creates a loop when owner but none exists."""
    mocked_sync_client._loop = None
    mocked_sync_client._loop_owner = True
    mocked_sync_client.close()


@pytest.mark.asyncio
async def test_base_client_convert_note_to_md():
    """convert_note_to_md delegates to async notes on BaseClient."""
    from youversion.core.base_client import BaseClient

    with patch("youversion.core.base_client.Authenticator"):
        client = BaseClient("u", "p")
        client._http_client = make_mock_http_client()
        client.notes = AsyncMock(return_value=[{"id": 1}])
        result = await client.convert_note_to_md()
        assert result == [{"id": 1}]


@pytest.mark.asyncio
async def test_base_client_create_moment_with_model():
    """create_moment accepts a CreateMoment instance directly."""
    from youversion.core.base_client import BaseClient
    from youversion.models.moments import CreateMoment

    with patch("youversion.core.base_client.Authenticator"):
        client = BaseClient("u", "p")
        client._http_client = make_mock_http_client()
        moment = CreateMoment(**CREATE_MOMENT_DATA)
        result = await client.create_moment(moment)
        assert result is not None


def test_sync_client_close_with_loop_owner(mocked_sync_client):
    """close() shuts down an owned event loop."""
    mocked_sync_client._get_loop()
    mocked_sync_client.close()


def test_sync_client_close_without_loop(mocked_sync_client):
    """close() works when no loop has been created yet."""
    mocked_sync_client._loop = None
    mocked_sync_client._loop_owner = False
    mocked_sync_client.close()


def test_sync_client_close_temp_loop(mocked_sync_client):
    """close() uses a temporary loop when not the owner."""
    mocked_sync_client._loop = None
    mocked_sync_client._loop_owner = False
    mocked_sync_client._http_client.close = AsyncMock()
    mocked_sync_client.close()


@pytest.mark.asyncio
async def test_async_client_context_manager():
    """AsyncClient __aenter__/__aexit__ with mocked HTTP."""
    from youversion.clients.async_client import AsyncClient

    with patch("youversion.core.base_client.Authenticator") as mock_auth_cls:
        mock_auth = MagicMock()
        mock_auth.username = "u"
        mock_auth.password = "p"
        mock_auth_cls.return_value = mock_auth

        client = AsyncClient("u", "p")
        client._http_client = make_mock_http_client()
        client._user_id = 1

        async with client:
            pass

        client._http_client.close.assert_awaited()


def test_badges_with_errors_path(mocked_sync_client):
    """badges() handles an errors payload from cards data."""

    async def cards_with_errors(**_kwargs):
        return {"errors": [{"id": 1, "title": "Badge"}]}

    mocked_sync_client._http_client.get_cards = AsyncMock(side_effect=cards_with_errors)
    result = mocked_sync_client.badges()
    assert isinstance(result, list)
