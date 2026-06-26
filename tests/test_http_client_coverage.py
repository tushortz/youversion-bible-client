"""Full HttpClient coverage with mocked httpx (no real API calls)."""

from __future__ import annotations

import inspect
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from youversion.config import Config
from youversion.core.http_client import HttpClient

ENVELOPE = {"response": {"code": 200, "data": {"ok": True}}}
PLAIN = {"ok": True}

HTTP_METHOD_ARGS: dict[str, dict] = {
    "get_bible_chapter": {"version_id": 1, "reference": "GEN.1"},
    "get_audio_chapter": {"version_id": 1, "reference": "GEN.1"},
    "search_bible": {"query": "love"},
    "search_plans": {"query": "faith"},
    "search_users": {"query": "john"},
    "get_images": {"reference": "GEN.1"},
    "search_events": {"query": "church"},
    "save_event": {"event_id": 1},
    "get_moments": {"page": 1},
    "create_moment": {"data": {"kind": "note"}},
    "update_moment": {"data": {"id": 1}},
    "hide_verse_colors": {"data": {"usfm": "JHN.3.16"}},
    "register_device": {"device_id": "dev-1"},
    "add_theme": {
        "theme_id": 1,
        "available_locales": ["en"],
        "colors": {},
        "cta_urls": {},
        "msgid_suffix": "x",
        "version_ids": {"en": 1},
    },
    "set_theme": {"theme_id": 1},
    "sync_friendship_contacts": {"contacts": [{"name": "A"}]},
    "update_notification_settings": {"data": {"email": True}},
    "update_notifications": {"data": {"read": [1]}},
    "update_votd_notification_settings": {"data": {"enabled": True}},
    "invite_by_email": {"data": {"emails": ["a@b.com"]}},
    "invite_by_sms": {"data": {"phones": ["+1"]}},
}


def _mock_response(payload: dict) -> MagicMock:
    response = MagicMock()
    response.json.return_value = payload
    return response


@pytest.fixture
def http_client():
    """HttpClient backed by mocked httpx AsyncClient."""
    mock_client = MagicMock()
    mock_client.get = AsyncMock(return_value=_mock_response(ENVELOPE))
    mock_client.post = AsyncMock(return_value=_mock_response(ENVELOPE))
    mock_client.aclose = AsyncMock()
    return HttpClient(mock_client, user_id=42)


@pytest.mark.asyncio
async def test_get_merges_headers_and_unwraps_envelope(http_client):
    result = await http_client.get("https://example.com", headers={"X-Test": "1"})
    assert result == {"ok": True}
    call = http_client._client.get.await_args
    assert call.kwargs["headers"]["X-Test"] == "1"
    assert "X-YouVersion-Client" in call.kwargs["headers"]


@pytest.mark.asyncio
async def test_get_plain_response_without_envelope(http_client):
    http_client._client.get = AsyncMock(return_value=_mock_response(PLAIN))
    result = await http_client.get("https://example.com")
    assert result == PLAIN


@pytest.mark.asyncio
async def test_get_awaitable_json(http_client):
    async def async_json():
        return ENVELOPE

    response = MagicMock()
    response.json.return_value = async_json()
    http_client._client.get = AsyncMock(return_value=response)
    result = await http_client.get("https://example.com")
    assert result == {"ok": True}


@pytest.mark.asyncio
async def test_get_json_parse_error(http_client):
    response = MagicMock()
    response.json.side_effect = ValueError("bad json")
    http_client._client.get = AsyncMock(return_value=response)
    with pytest.raises(ValueError, match="bad json"):
        await http_client.get("https://example.com")


@pytest.mark.asyncio
async def test_post_double_awaitable_json(http_client):
    async def async_json():
        return ENVELOPE

    response = MagicMock()
    response.json.return_value = async_json()
    http_client._client.post = AsyncMock(return_value=response)
    result = await http_client.post("https://example.com")
    assert result == {"ok": True}


@pytest.mark.asyncio
async def test_post_json_parse_error(http_client):
    response = MagicMock()
    response.json.side_effect = ValueError("bad json")
    http_client._client.post = AsyncMock(return_value=response)
    with pytest.raises(ValueError, match="bad json"):
        await http_client.post("https://example.com")


@pytest.mark.asyncio
async def test_get_public_uses_public_client(http_client):
    public = MagicMock()
    public.get = AsyncMock(return_value=_mock_response(ENVELOPE))
    http_client._public_client = public
    result = await http_client.get_public("https://example.com/public")
    assert result == {"ok": True}
    http_client._client.get.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_public_json_parse_error(http_client):
    public = MagicMock()
    bad = MagicMock()
    bad.json.side_effect = ValueError("bad json")
    public.get = AsyncMock(return_value=bad)
    http_client._public_client = public
    with pytest.raises(ValueError, match="bad json"):
        await http_client.get_public("https://example.com/public")


@pytest.mark.asyncio
async def test_ensure_public_client_creates_client():
    mock_client = MagicMock()
    client = HttpClient(mock_client)
    with patch("httpx.AsyncClient") as mock_cls:
        mock_cls.return_value = MagicMock()
        first = client._ensure_public_client()
        second = client._ensure_public_client()
        assert first is second
        mock_cls.assert_called_once()


@pytest.mark.asyncio
async def test_close_closes_both_clients(http_client):
    public = MagicMock()
    public.aclose = AsyncMock()
    http_client._public_client = public
    await http_client.close()
    public.aclose.assert_awaited_once()
    http_client._client.aclose.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_cards_omits_falsy_params(http_client):
    await http_client.get_cards(page=0, kind="")
    params = http_client._client.get.await_args.kwargs["params"]
    assert "kind" not in params


def _endpoint_methods() -> list[str]:
    skip = {
        "get",
        "get_public",
        "post",
        "close",
        "_unwrap_envelope",
        "_ensure_public_client",
    }
    return [
        name
        for name, obj in inspect.getmembers(HttpClient, predicate=inspect.isfunction)
        if not name.startswith("_") and name not in skip
    ]


@pytest.mark.parametrize("method_name", _endpoint_methods())
@pytest.mark.asyncio
async def test_http_endpoint_method(http_client, method_name):
    """Every HttpClient endpoint builds a request against mocked httpx."""
    method = getattr(http_client, method_name)
    sig = inspect.signature(method)
    kwargs = {}
    for param_name in sig.parameters:
        if param_name == "self":
            continue
        if param_name in HTTP_METHOD_ARGS.get(method_name, {}):
            kwargs[param_name] = HTTP_METHOD_ARGS[method_name][param_name]
        elif param_name in ("page", "version_id", "event_id", "moment_id", "video_id"):
            kwargs[param_name] = 1
        elif param_name in ("comment_id", "theme_id", "audio_id", "user_id"):
            kwargs[param_name] = 1
        elif param_name == "device_id":
            kwargs[param_name] = "dev-1"
        elif param_name == "usfm":
            kwargs[param_name] = "JHN.3.16"
        elif param_name == "comment":
            kwargs[param_name] = "hi"
        elif param_name == "reference":
            kwargs[param_name] = "GEN.1"
        elif param_name == "query":
            kwargs[param_name] = "test"
        elif param_name == "data":
            kwargs[param_name] = {"id": 1}
        elif param_name == "contacts":
            kwargs[param_name] = [{"name": "A"}]
        elif param_name == "kind":
            kwargs[param_name] = "note"
        elif param_name == "available_locales":
            kwargs[param_name] = ["en"]
        elif param_name == "colors":
            kwargs[param_name] = {}
        elif param_name == "cta_urls":
            kwargs[param_name] = {}
        elif param_name == "msgid_suffix":
            kwargs[param_name] = "x"
        elif param_name == "version_ids":
            kwargs[param_name] = {"en": 1}
        elif param_name == "language_tag":
            kwargs[param_name] = "en"
        elif param_name == "old_device_id":
            kwargs[param_name] = None
        elif param_name == "tags":
            kwargs[param_name] = None
        elif param_name == "device_type":
            kwargs[param_name] = "android"
        elif param_name == "previous_theme_id":
            kwargs[param_name] = None
        elif param_name == "latitude":
            kwargs[param_name] = None
        elif param_name == "longitude":
            kwargs[param_name] = None
        elif param_name == "comments":
            kwargs[param_name] = None
        elif param_name == "version_type":
            kwargs[param_name] = "all"
        elif param_name == "book":
            kwargs[param_name] = None
        elif param_name == "country":
            kwargs[param_name] = "US"

    if method_name == "get_moments_configuration":
        public = MagicMock()
        public.get = AsyncMock(return_value=_mock_response(ENVELOPE))
        http_client._public_client = public

    result = await method(**kwargs)
    assert result is not None


@pytest.mark.asyncio
async def test_get_verse_of_the_day_url(http_client):
    await http_client.get_verse_of_the_day()
    assert http_client._client.get.await_args.args[0] == Config.VOTD_URL


@pytest.mark.asyncio
async def test_search_bible_with_optional_params(http_client):
    await http_client.search_bible("love", version_id=1, book="GEN")
    params = http_client._client.get.await_args.kwargs["params"]
    assert params["version_id"] == 1
    assert params["book"] == "GEN"


@pytest.mark.asyncio
async def test_search_events_with_coordinates(http_client):
    await http_client.search_events("church", latitude=1.0, longitude=2.0)
    params = http_client._client.get.await_args.kwargs["params"]
    assert params["latitude"] == 1.0
    assert params["longitude"] == 2.0


@pytest.mark.asyncio
async def test_save_event_with_comments(http_client):
    await http_client.save_event(1, comments={"note": "hi"})
    assert http_client._client.post.await_args.kwargs["json"]["comments"] == {
        "note": "hi"
    }


@pytest.mark.asyncio
async def test_register_device_with_optional_fields(http_client):
    await http_client.register_device(
        "dev-1", old_device_id="old", tags="tag1", user_id=7
    )
    payload = http_client._client.post.await_args.kwargs["json"]
    assert payload["old_id"] == "old"
    assert payload["tags"] == "tag1"
    assert payload["user_id"] == 7


@pytest.mark.asyncio
async def test_set_theme_with_previous(http_client):
    await http_client.set_theme(2, previous_theme_id=1)
    assert http_client._client.post.await_args.kwargs["json"]["previous_id"] == 1


@pytest.mark.asyncio
async def test_get_public_awaitable_json(http_client):
    async def async_json():
        return ENVELOPE

    public = MagicMock()
    response = MagicMock()
    response.json.return_value = async_json()
    public.get = AsyncMock(return_value=response)
    http_client._public_client = public
    result = await http_client.get_public("https://example.com/public")
    assert result == {"ok": True}


@pytest.mark.asyncio
async def test_post_nested_awaitable_json(http_client):
    async def inner():
        return ENVELOPE

    async def outer():
        return inner()

    response = MagicMock()
    response.json.return_value = outer()
    http_client._client.post = AsyncMock(return_value=response)
    result = await http_client.post("https://example.com")
    assert result == {"ok": True}
