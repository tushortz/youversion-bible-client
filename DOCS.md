# YouVersion Bible API Client

Python library with sync and async clients for the YouVersion API.

## Table of contents

- [Installation](#installation)
- [Authentication](#authentication)
- [Clients](#clients)
- [API reference](#api-reference)
- [Sample responses](#sample-responses)
- [API behaviour](#api-behaviour)
- [CLI](#cli)
- [Testing](#testing)

## Installation

```bash
pip install youversion-bible-client
# or
uv add youversion-bible-client
```

## Authentication

Provide credentials in one of three ways:

```python
# Constructor
client = AsyncClient(username="user", password="pass")

# Environment variables
# YOUVERSION_USERNAME, YOUVERSION_PASSWORD

# .env file in project root
```

Most endpoints require a logged-in user. A few Bible and moments endpoints are public (see [API behaviour](#api-behaviour)).

## Clients

```python
from youversion.clients import AsyncClient, SyncClient
```

| Client | Use when |
|--------|----------|
| `AsyncClient` | `async`/`await`, concurrent requests |
| `SyncClient` | scripts, notebooks, synchronous code |

```python
import asyncio
from youversion.clients import AsyncClient

async def main():
    async with AsyncClient() as client:
        votd = await client.verse_of_the_day()
        friends = await client.get_friends(page=1)

asyncio.run(main())
```

```python
from youversion.clients import SyncClient

with SyncClient() as client:
    highlights = client.highlights(page=1)
```

## API reference

### Moments and content (authenticated)

| Method | Description |
|--------|-------------|
| `moments(page=1)` | All moment types |
| `highlights(page=1)` | Highlights |
| `notes(page=1)` | Notes |
| `bookmarks(page=1)` | Bookmarks |
| `my_images(page=1)` | User images |
| `badges(page=1)` | User badges (moments feed) |
| `plan_progress(page=1)` | Plan segment progress |
| `plan_subscriptions(page=1)` | Active plan subscriptions |
| `plan_completions(page=1)` | Completed plans |
| `convert_note_to_md()` | Export notes as markdown |
| `verse_of_the_day(day=None)` | Verse of the day |
| `create_moment(data)` | Create highlight, note, etc. |
| `get_moment_details(moment_id)` | Single moment |
| `delete_moment(moment_id)` | Delete moment |
| `get_client_side_moments(page=1)` | Client-side moment items |

### Bible (mostly public for chapter/audio)

| Method | Description |
|--------|-------------|
| `get_bible_configuration()` | Global Bible app config |
| `get_bible_versions(language_tag="eng", version_type="all")` | Versions for a language |
| `get_bible_version(version_id)` | Single version metadata |
| `get_bible_chapter(reference, version_id)` | Chapter HTML and audio links |
| `get_recommended_languages(country="US")` | Recommended languages |
| `search_bible(query, version_id=1, page=1)` | Full-text Bible search |

### Audio Bible

| Method | Description |
|--------|-------------|
| `get_audio_chapter(reference, version_id)` | Audio URLs and timing |
| `get_audio_version(audio_id)` | Audio version metadata |

### Search

| Method | Description |
|--------|-------------|
| `search_plans(query, language_tag="en", page=1)` | Reading plan search |
| `search_users(query, language_tag="eng", page=1)` | User search |

### Events

| Method | Description |
|--------|-------------|
| `search_events(query, page=1)` | Search events |
| `get_event_details(event_id)` | Event detail |
| `get_saved_events(page=1)` | Saved events |
| `save_event(event_id, comments="")` | Save event |
| `delete_saved_event(event_id)` | Remove saved event |
| `get_event_configuration()` | Events service config |

### Friends and friendships

| Method | Description |
|--------|-------------|
| `get_friends(page=1)` | Friends list |
| `get_all_friends(page=1)` | Friends with extended metadata |
| `delete_friend(user_id)` | Remove friend |
| `get_incoming_friend_requests(page=1)` | Pending requests (404 if none) |
| `get_friend_suggestions(page=1, language_tag="en")` | Suggested friends |
| `accept_friend_request(user_id)` | Accept request |
| `decline_friend_request(user_id)` | Decline request |
| `dismiss_friend_suggestion(user_id)` | Dismiss suggestion |
| `send_friend_request(user_id)` | Send request |
| `get_facebook_friends(page=1)` | Facebook-linked friends |
| `sync_friendship_contacts(contacts)` | Upload contacts for matching |

### Notifications

| Method | Description |
|--------|-------------|
| `get_notifications(page=1)` | Notification feed |
| `get_notification_settings()` | Current settings |
| `update_notification_settings(data)` | Update settings |
| `get_votd_notification_settings()` | VOTD notification prefs |
| `update_votd_notification_settings(data)` | Update VOTD prefs |

### Moments service (configuration, comments, likes)

| Method | Description |
|--------|-------------|
| `get_moments_configuration()` | Moments app config (public) |
| `get_moments_votd()` | VOTD from moments API (public) |
| `get_moment_colors()` | Highlight colours |
| `get_moment_labels()` | Labels |
| `create_comment(moment_id, comment)` | Add comment |
| `delete_comment(comment_id)` | Delete comment |
| `like_moment(moment_id)` / `unlike_moment(moment_id)` | Like toggles |

### Themes, images, videos, share

| Method | Description |
|--------|-------------|
| `get_themes(page=1, language_tag="en")` | Theme catalog |
| `get_theme_description(theme_id, language_tag="eng")` | Theme copy |
| `get_images(reference, language_tag="eng", page=1)` | Verse images |
| `get_image_upload_url()` | S3 upload parameters |
| `get_videos(language_tag="eng")` | Video list |
| `get_video_details(video_id)` | Video detail |
| `invite_by_email(data)` / `invite_by_sms(data)` | Share invites |

### Devices

| Method | Description |
|--------|-------------|
| `register_device(device_id, user_id=None)` | Push registration |
| `unregister_device(device_id)` | Unregister device |

## Sample responses

### Verse of the day

```json
{
  "day": 178,
  "usfm": ["ISA.43.18", "ISA.43.19"],
  "image_id": null
}
```

### Bible chapter (version_id=1, GEN.1)

```json
{
  "reference": {
    "usfm": ["GEN.1"],
    "human": "Genesis 1",
    "version_id": 1
  },
  "audio": [
    {
      "id": 8,
      "version_id": 1,
      "title": "The Listener's Bible: KJV Edition",
      "download_urls": {
        "format_mp3_32k": "//audio-bible-cdn.youversionapi.com/.../GEN/1-....mp3?version_id=1"
      }
    }
  ]
}
```

### Friend suggestions (`language_tag="en"`)

```json
{
  "suggestions": [
    {
      "id": 10001,
      "name": "Friend A",
      "location": "City",
      "source": "1 Mutual Friend",
      "mutual_friends_user_ids": [20001]
    }
  ],
  "next_page": 2
}
```

### Moments configuration

```json
{
  "images": {
    "verse_images": {
      "url": "//imageproxy.youversionapi.com/{0}x{1}/https://s3.amazonaws.com/..."
    }
  },
  "votd": {
    "iso_639_1": ["af", "am", "ar", "en", "..."]
  }
}
```

## API behaviour

**Language vs version ids.** `get_bible_configuration().default_versions[].id` is a language id. For chapters use `get_bible_versions("eng")` and pick a `versions[].id`, or use `1` for KJV.

**Public endpoints.** These reject Bearer tokens. The client uses an unauthenticated HTTP client for:

- `get_bible_chapter`
- `get_audio_chapter`
- `get_moments_configuration`
- `get_moments_votd`

**Locale tags.** Friend suggestions and themes use ISO 639-1 (`en`). Bible version lists use ISO 639-3 (`eng`).

**Removed from this client.** The following YouVersion endpoints are retired or return 404/410 and are not implemented:

- `search/3.1/suggest.json` (search autocomplete)
- `badges.youversionapi.com/3.1/items.json` (standalone badges service; use `badges()` instead)
- `moments/3.1/search/moments.json`
- `moments/3.1/localization/items.po`

## CLI

```bash
youversion votd
youversion highlights --page 1
youversion get-bible-chapter --reference GEN.1 --version-id 1
youversion search-bible --query love --version-id 1
```

uv script shortcuts: `uv run votd`, `uv run highlights`, etc.

## Testing

```bash
uv sync
uv run pytest
uv run pytest tests/test_api_integration.py -m integration  # requires .env
```

Integration tests record anonymized request/response JSON under `results/integration/<timestamp>/`.

