# YouVersion Bible API Client

Python client for the YouVersion Bible API. Use it to read scripture, export your notes and highlights, and work with moments, plans, events, and social features.

Please use responsibly.

## Installation

```bash
pip install youversion-bible-client
```

## Features

- [x] verse of the day
- [x] moments / feeds
- [x] notes
- [x] verse highlights
- [x] bookmarks
- [x] plan subscriptions
- [x] plan progress
- [x] plan completions
- [x] verse search


## Credentials

Set credentials via environment variables or a `.env` file:

```env
YOUVERSION_USERNAME=your_username
YOUVERSION_PASSWORD=your_password
```

## Quick start

### Async (recommended)

```python
import asyncio
from youversion.clients import AsyncClient

async def main():
    async with AsyncClient() as client:
        votd = await client.verse_of_the_day()
        print(votd.usfm)

        chapter = await client.get_bible_chapter("GEN.1", version_id=1)
        print(chapter["reference"]["human"])

asyncio.run(main())
```

### Sync

```python
from youversion.clients import SyncClient

with SyncClient() as client:
    notes = client.notes(page=1)
    print(len(notes))
```

## Common tasks

| Task | Method |
|------|--------|
| Verse of the day | `verse_of_the_day()` |
| Highlights, notes, bookmarks | `highlights()`, `notes()`, `bookmarks()` |
| Bible search | `search_bible("love", version_id=1)` |
| Bible chapter | `get_bible_chapter("GEN.1", version_id=1)` |
| Audio chapter | `get_audio_chapter("GEN.1", version_id=1)` |
| Reading plans | `plan_progress()`, `search_plans("daily")` |
| Friends | `get_friends()`, `get_friend_suggestions(language_tag="en")` |
| Notifications | `get_notifications()` |
| Events | `search_events("church")`, `get_event_details(event_id)` |

## Sample responses

Values below are trimmed from live integration tests. User-specific fields are anonymized.

**Verse of the day** (`verse_of_the_day()`):

```json
{
  "day": 178,
  "usfm": ["ISA.43.18", "ISA.43.19"],
  "image_id": null
}
```

**Bible chapter** (`get_bible_chapter("GEN.1", version_id=1)`):

```json
{
  "reference": {
    "usfm": ["GEN.1"],
    "human": "Genesis 1",
    "version_id": 1
  },
  "content": "<div>... verse HTML ...</div>",
  "next": {"usfm": ["GEN.2"], "human": "Genesis 2"}
}
```

**Bible configuration** (`get_bible_configuration()`):

```json
{
  "short_url": "https://www.bible.com/",
  "totals": {"versions": 3809, "languages": 2439}
}
```

Note: `default_versions[].id` is a **language** id, not a Bible version id. Resolve a version id via `get_bible_versions("eng")` or use a known id such as `1` (KJV).

## API notes

- **Public endpoints** (no Bearer token): `get_bible_chapter`, `get_audio_chapter`, `get_moments_configuration`, `get_moments_votd`. The client handles this automatically.
- **Friend suggestions** require `language_tag="en"` (ISO 639-1), not `eng`.
- **User badges** come from `badges()` via the moments feed, not a separate badges service.

## CLI

```bash
uv run youversion votd
uv run youversion highlights --page 1
uv run youversion get-bible-chapter --reference GEN.1 --version-id 1
```

See [DOCS.md](./DOCS.md) for the full method list and [docs/](docs/) for Sphinx documentation.

## Development

```bash
uv sync
uv run pytest
uv run pytest tests/test_api_integration.py -m integration  # requires .env credentials
```

Integration runs save request/response JSON under `results/integration/`.
