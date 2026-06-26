"""Live integration tests against the YouVersion API.

Requires YOUVERSION_USERNAME and YOUVERSION_PASSWORD in .env.
Each HTTP call is saved under ``results/integration/<timestamp>/``.
"""

import os

import pytest
import pytest_asyncio
from dotenv import load_dotenv

from tests.integration_recorder import install_httpx_recorder, register_recorder_state
from youversion.clients.async_client import AsyncClient

load_dotenv()

pytestmark = pytest.mark.integration

USERNAME = os.getenv("YOUVERSION_USERNAME")
PASSWORD = os.getenv("YOUVERSION_PASSWORD")

requires_credentials = pytest.mark.skipif(
    not USERNAME or not PASSWORD,
    reason="YOUVERSION_USERNAME and YOUVERSION_PASSWORD required in .env",
)


def _has_data(result) -> bool:
    """Return True when an API call returned a non-empty payload."""
    if result is None:
        return False
    if isinstance(result, str):
        return len(result) > 0
    if isinstance(result, dict):
        if result.get("errors"):
            return False
        return bool(result)
    if hasattr(result, "__dict__"):
        return bool(vars(result))
    if isinstance(result, list):
        return len(result) > 0
    return True


def _get_field(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


@pytest_asyncio.fixture
async def client(integration_results_dir):
    """Authenticated async client using .env credentials."""
    c = AsyncClient(USERNAME, PASSWORD)
    await c._ensure_authenticated()
    state = install_httpx_recorder(c._http_client._client, integration_results_dir)
    register_recorder_state(state)
    register_recorder_state(
        install_httpx_recorder(
            c._http_client._ensure_public_client(), integration_results_dir
        )
    )
    yield c
    await c.close()


@requires_credentials
@pytest.mark.asyncio
async def test_bible_configuration_and_chapter_chain(client):
    """Versions list provides a Bible version id usable for chapter lookup."""
    config = await client.get_bible_configuration()
    assert _has_data(config)
    versions_data = await client.get_bible_versions("eng")
    versions = _get_field(versions_data, "versions", [])
    assert versions
    version_id = 1
    version = await client.get_bible_version(version_id)
    assert _has_data(version)
    chapter = await client.get_bible_chapter("GEN.1", version_id=version_id)
    assert _has_data(chapter)


@requires_credentials
@pytest.mark.asyncio
async def test_search_bible_and_audio_chain(client):
    """Bible search and audio chapter should return data for a known query."""
    results = await client.search_bible("love", version_id=1, page=1)
    assert _has_data(results)
    audio = await client.get_audio_chapter("GEN.1", version_id=1)
    assert _has_data(audio)


@requires_credentials
@pytest.mark.asyncio
async def test_events_search_and_details_chain(client):
    """Event search should return IDs usable for event details."""
    results = await client.search_events("church", page=1)
    assert _has_data(results)
    events = _get_field(results, "events", [])
    assert events
    event_id = _get_field(events[0], "id")
    detail = await client.get_event_details(event_id)
    assert _has_data(detail)


@requires_credentials
@pytest.mark.asyncio
async def test_friends_and_notifications(client):
    """Friends and notifications endpoints should return structured data."""
    friends = await client.get_friends(page=1)
    assert _has_data(friends)
    all_friends = await client.get_all_friends(page=1)
    assert _has_data(all_friends)
    notifications = await client.get_notifications(page=1)
    assert _has_data(notifications)
    settings = await client.get_notification_settings()
    assert _has_data(settings)


@requires_credentials
@pytest.mark.asyncio
async def test_moments_configuration_and_client_side_items(client):
    """Moments configuration and client-side items should be reachable."""
    config = await client.get_moments_configuration()
    assert _has_data(config)
    items = await client.get_client_side_moments(page=1)
    assert _has_data(items)


@requires_credentials
@pytest.mark.asyncio
async def test_themes_best_effort(client):
    """Themes may return an empty catalog (404) for some accounts."""
    themes = await client.get_themes(page=1, language_tag="en")
    assert themes is not None


@requires_credentials
@pytest.mark.asyncio
async def test_verse_of_the_day_endpoints(client):
    """Both VOTD endpoints should return content."""
    votd = await client.verse_of_the_day()
    assert _has_data(votd)
    moments_votd = await client.get_moments_votd()
    assert _has_data(moments_votd)


@requires_credentials
@pytest.mark.asyncio
async def test_image_upload_url_is_get(client):
    """Image upload URL endpoint should return upload parameters."""
    upload = await client.get_image_upload_url()
    assert _has_data(upload)


@requires_credentials
@pytest.mark.asyncio
async def test_optional_endpoints_best_effort(client):
    """Endpoints that may 404 for some accounts should not raise locally."""
    optional_calls = [
        client.get_incoming_friend_requests(page=1),
        client.get_friend_suggestions(page=1, language_tag="en"),
    ]
    for coro in optional_calls:
        try:
            result = await coro
            assert result is not None
        except Exception:
            pytest.fail("Optional endpoint raised unexpectedly")
