# YouVersion Bible API Client Documentation

A comprehensive Python client library for accessing the YouVersion Bible API. This library provides both synchronous and asynchronous interfaces to interact with all YouVersion API endpoints.

## Table of Contents

- [Installation](#installation)
- [Authentication](#authentication)
- [AsyncClient Usage](#asynclient-usage)
- [SyncClient Usage](#synclient-usage)
- [API Methods Reference](#api-methods-reference)
  - [Moments & Content](#moments--content)
  - [Bible API](#bible-api)
  - [Audio Bible API](#audio-bible-api)
  - [Search API](#search-api)
  - [Video API](#video-api)
  - [Image API](#image-api)
  - [Event API](#event-api)
  - [Comment API](#comment-api)
  - [Like API](#like-api)
  - [Device API](#device-api)
  - [Theme API](#theme-api)
  - [Friend API](#friend-api)
  - [Localization API](#localization-api)
- [Data Models](#data-models)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

## Installation

```bash
pip install youversion-bible-client
```

Or using Poetry:

```bash
poetry add youversion-bible-client
```

## Authentication

The client supports authentication via:
1. **Constructor arguments** (recommended for scripts)
2. **Environment variables** (recommended for production)
3. **`.env` file** (recommended for development)

### Environment Variables

Set the following environment variables:

```bash
export YOUVERSION_USERNAME="your_username"
export YOUVERSION_PASSWORD="your_password"
```

Or create a `.env` file in your project root:

```env
YOUVERSION_USERNAME=your_username
YOUVERSION_PASSWORD=your_password
```

### Authentication Examples

```python
# Using constructor arguments
client = AsyncClient(username="user", password="pass")

# Using environment variables
client = AsyncClient()  # Reads from env vars automatically
```

## AsyncClient Usage

The `AsyncClient` is designed for async/await code and provides better performance for concurrent operations.

### Basic Usage

```python
import asyncio
from youversion.clients import AsyncClient

async def main():
    # Using async context manager (recommended)
    async with AsyncClient() as client:
        # Get verse of the day
        votd = await client.verse_of_the_day()
        print(f"Verse: {votd.usfm}")

        # Get moments
        moments = await client.moments(page=1)
        print(f"Found {len(moments)} moments")

        # Get highlights
        highlights = await client.highlights(page=1)
        for highlight in highlights:
            print(f"Highlight: {highlight.id}")

asyncio.run(main())
```

### Manual Resource Management

```python
import asyncio
from youversion.clients import AsyncClient

async def main():
    client = AsyncClient()
    try:
        await client._ensure_authenticated()

        # Use the client
        moments = await client.moments()
        print(f"Found {len(moments)} moments")

    finally:
        await client.close()

asyncio.run(main())
```

### Concurrent Operations

```python
import asyncio
from youversion.clients import AsyncClient

async def main():
    async with AsyncClient() as client:
        # Run multiple operations concurrently
        moments_task = client.moments(page=1)
        highlights_task = client.highlights(page=1)
        notes_task = client.notes(page=1)

        # Wait for all to complete
        moments, highlights, notes = await asyncio.gather(
            moments_task,
            highlights_task,
            notes_task
        )

        print(f"Moments: {len(moments)}")
        print(f"Highlights: {len(highlights)}")
        print(f"Notes: {len(notes)}")

asyncio.run(main())
```

### Accessing User Information

```python
async with AsyncClient() as client:
    # Access username
    username = client.username
    print(f"Logged in as: {username}")

    # Access user ID (available after authentication)
    user_id = client.user_id
    print(f"User ID: {user_id}")
```

## SyncClient Usage

The `SyncClient` provides a synchronous interface that wraps the async operations, making it easier to use in synchronous code.

### Basic Usage

```python
from youversion.clients import SyncClient

# Using context manager (recommended)
with SyncClient() as client:
    # Get verse of the day
    votd = client.verse_of_the_day()
    print(f"Verse: {votd.usfm}")

    # Get moments
    moments = client.moments(page=1)
    print(f"Found {len(moments)} moments")

    # Get highlights
    highlights = client.highlights(page=1)
    for highlight in highlights:
        print(f"Highlight: {highlight.id}")
```

### Manual Resource Management

```python
from youversion.clients import SyncClient

client = SyncClient()
try:
    # Use the client
    moments = client.moments()
    print(f"Found {len(moments)} moments")
finally:
    client.close()
```

### Sequential Operations

```python
from youversion.clients import SyncClient

with SyncClient() as client:
    # All operations are synchronous
    moments = client.moments(page=1)
    highlights = client.highlights(page=1)
    notes = client.notes(page=1)

    print(f"Moments: {len(moments)}")
    print(f"Highlights: {len(highlights)}")
    print(f"Notes: {len(notes)}")
```

### Important Notes for SyncClient

- **Cannot be used inside async functions**: If you're already in an async context, use `AsyncClient` instead
- **Creates its own event loop**: The `SyncClient` manages an event loop internally
- **Thread-safe**: Each `SyncClient` instance manages its own event loop

## API Methods Reference

All methods are available in both `AsyncClient` and `SyncClient` with identical signatures. The only difference is that `AsyncClient` methods are `async` and must be awaited, while `SyncClient` methods are synchronous.

### Moments & Content

These methods retrieve user-generated content like moments, highlights, notes, bookmarks, and badges.

#### `moments(page: int = 1) -> list[Moment]`

Get all moments (mixed content types).

**Parameters:**
- `page` (int, optional): Page number. Default: 1

**Returns:** List of dynamically created Moment objects

**Example:**
```python
# Async
moments = await client.moments(page=1)

# Sync
moments = client.moments(page=1)

# Access moment properties
for moment in moments:
    print(f"ID: {moment.id}")
    print(f"Kind: {moment.kind_id}")
    print(f"Title: {moment.moment_title}")
```

#### `highlights(page: int = 1) -> list[Any]`

Get user highlights.

**Parameters:**
- `page` (int, optional): Page number. Default: 1

**Returns:** List of Highlight objects

**Example:**
```python
highlights = await client.highlights(page=1)
for highlight in highlights:
    print(f"Text: {highlight.text}")
    print(f"References: {highlight.references}")
```

#### `notes(page: int = 1) -> list[Any]`

Get user notes.

**Parameters:**
- `page` (int, optional): Page number. Default: 1

**Returns:** List of Note objects

**Example:**
```python
notes = await client.notes(page=1)
for note in notes:
    print(f"Content: {note.content}")
    print(f"Status: {note.status}")
```

#### `bookmarks(page: int = 1) -> list[Any]`

Get user bookmarks.

**Parameters:**
- `page` (int, optional): Page number. Default: 1

**Returns:** List of Bookmark objects

**Example:**
```python
bookmarks = await client.bookmarks(page=1)
for bookmark in bookmarks:
    print(f"Title: {bookmark.moment_title}")
```

#### `my_images(page: int = 1) -> list[Any]`

Get user images.

**Parameters:**
- `page` (int, optional): Page number. Default: 1

**Returns:** List of Image objects

**Example:**
```python
images = await client.my_images(page=1)
for image in images:
    print(f"Image ID: {image.id}")
```

#### `badges(page: int = 1) -> list[Any]`

Get user badges.

**Parameters:**
- `page` (int, optional): Page number. Default: 1

**Returns:** List of Badge objects

**Example:**
```python
badges = await client.badges(page=1)
for badge in badges:
    print(f"Badge: {badge.id}")
```

#### `verse_of_the_day(day: Optional[int] = None) -> Any`

Get verse of the day.

**Parameters:**
- `day` (int, optional): Specific day number (1-365). If None, returns current day's verse.

**Returns:** Votd object

**Example:**
```python
# Get today's verse
votd = await client.verse_of_the_day()
print(f"Day: {votd.day}")
print(f"USFM: {votd.usfm}")

# Get verse for specific day
votd = await client.verse_of_the_day(day=100)
```

#### `plan_progress(page: int = 1) -> list[Any]`

Get reading plan progress.

**Parameters:**
- `page` (int, optional): Page number. Default: 1

**Returns:** List of PlanProgress objects

**Example:**
```python
progress = await client.plan_progress(page=1)
for item in progress:
    print(f"Plan: {item.plan_title}")
    print(f"Progress: {item.percent_complete}%")
```

#### `plan_subscriptions(page: int = 1) -> list[Any]`

Get subscribed reading plans.

**Parameters:**
- `page` (int, optional): Page number. Default: 1

**Returns:** List of PlanSubscription objects

**Example:**
```python
subscriptions = await client.plan_subscriptions(page=1)
for sub in subscriptions:
    print(f"Plan: {sub.plan_title}")
```

#### `plan_completions(page: int = 1) -> list[Any]`

Get completed reading plans.

**Parameters:**
- `page` (int, optional): Page number. Default: 1

**Returns:** List of PlanCompletion objects

**Example:**
```python
completions = await client.plan_completions(page=1)
for completion in completions:
    print(f"Completed Plan: {completion.plan_title}")
```

#### `convert_note_to_md() -> list[Any]`

Convert notes to markdown format.

**Returns:** List of converted note data

**Example:**
```python
notes_md = await client.convert_note_to_md()
```

### Bible API

Methods for accessing Bible content, versions, and configuration.

#### `get_bible_configuration() -> dict[str, Any]`

Get Bible configuration including available languages, books, and metadata.

**Returns:** Bible configuration data

**Example:**
```python
config = await client.get_bible_configuration()
# Access configuration data
print(config)
```

#### `get_bible_versions(language_tag: str = "eng", version_type: str = "all") -> dict[str, Any]`

Get Bible versions for a specific language.

**Parameters:**
- `language_tag` (str, optional): Language tag (e.g., 'eng', 'spa'). Default: "eng"
- `version_type` (str, optional): Type of versions ('all', 'text', 'audio'). Default: "all"

**Returns:** Bible versions data

**Example:**
```python
# Get all English versions
versions = await client.get_bible_versions("eng", "all")

# Get only text versions
text_versions = await client.get_bible_versions("eng", "text")

# Get only audio versions
audio_versions = await client.get_bible_versions("eng", "audio")
```

#### `get_bible_version(version_id: int) -> dict[str, Any]`

Get specific Bible version details.

**Parameters:**
- `version_id` (int): Version ID

**Returns:** Bible version data

**Example:**
```python
version = await client.get_bible_version(1)
print(f"Version: {version.name}")
print(f"Language: {version.language}")
```

#### `get_bible_chapter(reference: str, version_id: int = 1) -> dict[str, Any]`

Get Bible chapter content.

**Parameters:**
- `reference` (str): USFM reference (e.g., 'GEN.1', 'JHN.3.16')
- `version_id` (int, optional): Version ID. Default: 1

**Returns:** Chapter content data

**Example:**
```python
# Get Genesis chapter 1
chapter = await client.get_bible_chapter("GEN.1", version_id=1)

# Get John 3:16
verse = await client.get_bible_chapter("JHN.3.16", version_id=1)
```

#### `get_recommended_languages(country: str = "US") -> dict[str, Any]`

Get recommended languages for a country.

**Parameters:**
- `country` (str, optional): Country code (e.g., 'US', 'CA'). Default: "US"

**Returns:** Recommended languages data

**Example:**
```python
languages = await client.get_recommended_languages("US")
```

### Audio Bible API

Methods for accessing audio Bible content.

#### `get_audio_chapter(reference: str, version_id: int = 1) -> dict[str, Any]`

Get audio chapter information.

**Parameters:**
- `reference` (str): USFM reference (e.g., 'GEN.1')
- `version_id` (int, optional): Audio version ID. Default: 1

**Returns:** Audio chapter data

**Example:**
```python
audio_chapter = await client.get_audio_chapter("GEN.1", version_id=1)
# Returns list or dict depending on API response
```

#### `get_audio_version(audio_id: int) -> dict[str, Any]`

Get audio version details.

**Parameters:**
- `audio_id` (int): Audio version ID

**Returns:** Audio version data

**Example:**
```python
audio_version = await client.get_audio_version(1)
```

### Search API

Methods for searching Bible text, plans, and users.

#### `search_bible(query: str, version_id: Optional[int] = None, book: Optional[str] = None, page: int = 1) -> dict[str, Any]`

Search Bible text.

**Parameters:**
- `query` (str): Search query
- `version_id` (int, optional): Version ID to search in
- `book` (str, optional): Book filter (e.g., 'JHN', 'GEN')
- `page` (int, optional): Page number. Default: 1

**Returns:** Search results data

**Example:**
```python
# Search all versions
results = await client.search_bible("love")

# Search specific version
results = await client.search_bible("love", version_id=1)

# Search specific book
results = await client.search_bible("love", book="JHN")
```

#### `search_plans(query: str, language_tag: str = "en", page: int = 1) -> dict[str, Any]`

Search reading plans.

**Parameters:**
- `query` (str): Search query
- `language_tag` (str, optional): Language tag. Default: "en"
- `page` (int, optional): Page number. Default: 1

**Returns:** Plan search results data

**Example:**
```python
plans = await client.search_plans("daily", language_tag="en")
```

#### `search_users(query: str, language_tag: str = "eng", page: int = 1) -> dict[str, Any]`

Search users.

**Parameters:**
- `query` (str): Search query
- `language_tag` (str, optional): Language tag. Default: "eng"
- `page` (int, optional): Page number. Default: 1

**Returns:** User search results data

**Example:**
```python
users = await client.search_users("john", language_tag="eng")
```

### Video API

Methods for accessing video content.

#### `get_videos(language_tag: str = "eng") -> dict[str, Any]`

Get videos list.

**Parameters:**
- `language_tag` (str, optional): Language tag. Default: "eng"

**Returns:** Videos data

**Example:**
```python
videos = await client.get_videos("eng")
```

#### `get_video_details(video_id: int) -> dict[str, Any]`

Get video details.

**Parameters:**
- `video_id` (int): Video ID

**Returns:** Video details data

**Example:**
```python
video = await client.get_video_details(123)
```

### Image API

Methods for accessing images (different from `my_images` which gets user's images).

#### `get_images(reference: str, language_tag: str = "eng", page: int = 1) -> dict[str, Any]`

Get images for a Bible reference.

**Parameters:**
- `reference` (str): USFM reference
- `language_tag` (str, optional): Language tag. Default: "eng"
- `page` (int, optional): Page number. Default: 1

**Returns:** Images data

**Example:**
```python
images = await client.get_images("GEN.1.1", language_tag="eng")
```

#### `get_image_upload_url() -> dict[str, Any]`

Get image upload URL and parameters.

**Returns:** Upload URL data

**Example:**
```python
upload_info = await client.get_image_upload_url()
print(f"Upload URL: {upload_info.upload_url}")
```

### Event API

Methods for searching and managing church events.

#### `search_events(query: str, latitude: Optional[float] = None, longitude: Optional[float] = None, page: int = 1) -> dict[str, Any]`

Search events.

**Parameters:**
- `query` (str): Search query
- `latitude` (float, optional): Latitude for location-based search
- `longitude` (float, optional): Longitude for location-based search
- `page` (int, optional): Page number. Default: 1

**Returns:** Event search results data

**Example:**
```python
# Search by query
events = await client.search_events("church")

# Search by location
events = await client.search_events(
    "church",
    latitude=40.7128,
    longitude=-74.0060
)
```

#### `get_event_details(event_id: int) -> dict[str, Any]`

Get event details.

**Parameters:**
- `event_id` (int): Event ID

**Returns:** Event details data

**Example:**
```python
event = await client.get_event_details(123)
```

#### `get_saved_events(page: int = 1) -> dict[str, Any]`

Get saved events.

**Parameters:**
- `page` (int, optional): Page number. Default: 1

**Returns:** Saved events data

**Example:**
```python
saved_events = await client.get_saved_events(page=1)
```

#### `save_event(event_id: int, comments: Optional[dict[str, Any]] = None) -> dict[str, Any]`

Save an event.

**Parameters:**
- `event_id` (int): Event ID
- `comments` (dict, optional): Comments/notes about the event

**Returns:** Save result data

**Example:**
```python
result = await client.save_event(123, comments={"note": "Looking forward to this!"})
```

#### `delete_saved_event(event_id: int) -> dict[str, Any]`

Delete a saved event.

**Parameters:**
- `event_id` (int): Event ID

**Returns:** Delete result data

**Example:**
```python
result = await client.delete_saved_event(123)
```

#### `get_all_saved_event_ids() -> dict[str, Any]`

Get all saved event IDs.

**Returns:** All saved event IDs data

**Example:**
```python
event_ids = await client.get_all_saved_event_ids()
```

#### `get_event_configuration() -> dict[str, Any]`

Get event configuration.

**Returns:** Event configuration data

**Example:**
```python
config = await client.get_event_configuration()
```

### Moment Management API

Methods for managing moments (notes, highlights, etc.).

#### `get_moments(page: int = 1, user_id: Optional[int] = None, kind: Optional[str] = None, version_id: Optional[int] = None, usfm: Optional[str] = None) -> dict[str, Any]`

Get moments list with optional filters.

**Parameters:**
- `page` (int, optional): Page number. Default: 1
- `user_id` (int, optional): Filter by user ID
- `kind` (str, optional): Filter by moment kind (e.g., 'note', 'highlight')
- `version_id` (int, optional): Filter by Bible version ID
- `usfm` (str, optional): Filter by USFM reference

**Returns:** Moments data

**Example:**
```python
# Get all moments
moments = await client.get_moments()

# Get notes only
notes = await client.get_moments(kind="note")

# Get moments for specific verse
verse_moments = await client.get_moments(usfm="JHN.3.16")
```

#### `get_moment_details(moment_id: int) -> dict[str, Any]`

Get moment details.

**Parameters:**
- `moment_id` (int): Moment ID

**Returns:** Moment details data

**Example:**
```python
moment = await client.get_moment_details(12345)
```

#### `create_moment(data: Union[CreateMoment, dict[str, Any]]) -> dict[str, Any]`

Create a new moment.

**Parameters:**
- `data` (CreateMoment or dict): Moment data

**Returns:** Created moment data

**Example:**
```python
from youversion.models.moments import CreateMoment, ReferenceCreate
from youversion.enums import MomentKinds, StatusEnum

# Using Pydantic model (recommended)
reference = ReferenceCreate(
    human="John 3:16",
    version_id=1,
    usfm=["JHN.3.16"]
)

moment = CreateMoment(
    kind=MomentKinds.NOTE,
    content="This is my note",
    references=[reference],
    title="My Note Title",
    status=StatusEnum.PRIVATE,
    body="Note body text",
    color="ff0000",
    labels=["favorite"],
    language_tag="en"
)

result = await client.create_moment(moment)

# Using dict
moment_dict = {
    "kind": "note",
    "content": "My note",
    "references": [{
        "human": "John 3:16",
        "version_id": 1,
        "usfm": ["JHN.3.16"]
    }],
    "title": "My Note",
    "status": "private",
    "body": "Body text",
    "color": "ff0000",
    "labels": ["favorite"],
    "language_tag": "en"
}
result = await client.create_moment(moment_dict)
```

#### `update_moment(data: dict[str, Any]) -> dict[str, Any]`

Update an existing moment.

**Parameters:**
- `data` (dict): Moment data including ID and fields to update

**Returns:** Updated moment data

**Example:**
```python
update_data = {
    "id": 12345,
    "content": "Updated content",
    "title": "Updated title"
}
result = await client.update_moment(update_data)
```

#### `delete_moment(moment_id: int) -> dict[str, Any]`

Delete a moment.

**Parameters:**
- `moment_id` (int): Moment ID

**Returns:** Delete result data

**Example:**
```python
result = await client.delete_moment(12345)
```

#### `get_moment_colors() -> dict[str, Any]`

Get available highlight colors.

**Returns:** Colors data

**Example:**
```python
colors = await client.get_moment_colors()
```

#### `get_moment_labels() -> dict[str, Any]`

Get moment labels.

**Returns:** Labels data

**Example:**
```python
labels = await client.get_moment_labels()
```

#### `get_verse_colors(usfm: str, version_id: int) -> dict[str, Any]`

Get verse highlight colors.

**Parameters:**
- `usfm` (str): USFM reference
- `version_id` (int): Bible version ID

**Returns:** Verse colors data

**Example:**
```python
colors = await client.get_verse_colors("JHN.3.16", version_id=1)
```

#### `hide_verse_colors(data: dict[str, Any]) -> dict[str, Any]`

Hide verse highlight colors.

**Parameters:**
- `data` (dict): Hide colors data

**Returns:** Hide result data

**Example:**
```python
hide_data = {
    "verses": ["JHN.3.16"],
    "version_id": 1
}
result = await client.hide_verse_colors(hide_data)
```

#### `get_moments_configuration() -> dict[str, Any]`

Get moments configuration.

**Returns:** Moments configuration data

**Example:**
```python
config = await client.get_moments_configuration()
```

### Comment API

Methods for managing comments on moments.

#### `create_comment(moment_id: int, comment: str) -> dict[str, Any]`

Create a comment on a moment.

**Parameters:**
- `moment_id` (int): Moment ID
- `comment` (str): Comment text

**Returns:** Created comment data

**Example:**
```python
result = await client.create_comment(12345, "Great verse!")
```

#### `delete_comment(comment_id: int) -> dict[str, Any]`

Delete a comment.

**Parameters:**
- `comment_id` (int): Comment ID

**Returns:** Delete result data

**Example:**
```python
result = await client.delete_comment(67890)
```

### Like API

Methods for liking and unliking moments.

#### `like_moment(moment_id: int) -> dict[str, Any]`

Like a moment.

**Parameters:**
- `moment_id` (int): Moment ID

**Returns:** Like result data

**Example:**
```python
result = await client.like_moment(12345)
```

#### `unlike_moment(moment_id: int) -> dict[str, Any]`

Unlike a moment.

**Parameters:**
- `moment_id` (int): Moment ID

**Returns:** Unlike result data

**Example:**
```python
result = await client.unlike_moment(12345)
```

### Device API

Methods for managing push notification devices.

#### `register_device(device_id: str, device_type: str = "android", user_id: Optional[int] = None, old_device_id: Optional[str] = None, tags: Optional[str] = None) -> dict[str, Any]`

Register device for push notifications.

**Parameters:**
- `device_id` (str): Device ID/token
- `device_type` (str, optional): Device type ('android', 'ios'). Default: "android"
- `user_id` (int, optional): User ID
- `old_device_id` (str, optional): Previous device ID to replace
- `tags` (str, optional): Device tags

**Returns:** Registration result data

**Example:**
```python
result = await client.register_device(
    device_id="device_token_123",
    device_type="android",
    tags="reading_plan_yes"
)
```

#### `unregister_device(device_id: str) -> dict[str, Any]`

Unregister device from push notifications.

**Parameters:**
- `device_id` (str): Device ID

**Returns:** Unregistration result data

**Example:**
```python
result = await client.unregister_device("device_token_123")
```

### Theme API

Methods for managing app themes.

#### `get_themes(page: int = 1, language_tag: str = "eng") -> dict[str, Any]`

Get available themes.

**Parameters:**
- `page` (int, optional): Page number. Default: 1
- `language_tag` (str, optional): Language tag. Default: "eng"

**Returns:** Themes data

**Example:**
```python
themes = await client.get_themes(page=1, language_tag="eng")
```

#### `add_theme(theme_id: int, available_locales: list[str], colors: dict[str, Any], cta_urls: dict[str, Any], msgid_suffix: str, version_ids: dict[str, int]) -> dict[str, Any]`

Add a theme to user's collection.

**Parameters:**
- `theme_id` (int): Theme ID
- `available_locales` (list[str]): List of available locale codes
- `colors` (dict): Theme colors dictionary
- `cta_urls` (dict): Call-to-action URLs dictionary
- `msgid_suffix` (str): Message ID suffix
- `version_ids` (dict): Dictionary of version IDs by locale code

**Returns:** Add result data

**Example:**
```python
# First, get theme details
themes = await client.get_themes()
theme = themes["response"]["data"]["themes"][0]  # Example: first theme

# Then add it with all required fields
result = await client.add_theme(
    theme_id=theme["id"],
    available_locales=theme["available_locales"],
    colors=theme["colors"],
    cta_urls=theme["cta_urls"],
    msgid_suffix=theme["msgid_suffix"],
    version_ids=theme["version_ids"]
)
```

#### `remove_theme(theme_id: int) -> dict[str, Any]`

Remove a theme from user's collection.

**Parameters:**
- `theme_id` (int): Theme ID

**Returns:** Remove result data

**Example:**
```python
result = await client.remove_theme(123)
```

#### `set_theme(theme_id: int, previous_theme_id: Optional[int] = None) -> dict[str, Any]`

Set active theme.

**Parameters:**
- `theme_id` (int): Theme ID to set as active
- `previous_theme_id` (int, optional): Previous theme ID

**Returns:** Set result data

**Example:**
```python
result = await client.set_theme(theme_id=123, previous_theme_id=456)
```

#### `get_theme_description(theme_id: int, language_tag: str = "eng") -> dict[str, Any]`

Get theme description.

**Parameters:**
- `theme_id` (int): Theme ID
- `language_tag` (str, optional): Language tag. Default: "eng"

**Returns:** Theme description data

**Example:**
```python
description = await client.get_theme_description(123, language_tag="eng")
```

### Friend API

Methods for managing friendships.

#### `send_friend_request(user_id: int) -> dict[str, Any]`

Send a friend request to a user.

**Parameters:**
- `user_id` (int): User ID to send friend request to

**Returns:** Friend request response data with incoming and outgoing lists

**Example:**
```python
result = await client.send_friend_request(123456)
print(f"Outgoing requests: {result.outgoing}")
```

### Localization API

Methods for accessing localization strings.

#### `get_localization_items(language_tag: str = "eng") -> str`

Get localization strings for a language.

**Parameters:**
- `language_tag` (str, optional): Language tag. Default: "eng"

**Returns:** Localization strings (PO file format)

**Example:**
```python
localization = await client.get_localization_items("eng")
# Returns PO file format string
```

## Data Models

The library uses **dynamic Pydantic models** created at runtime based on API responses. This means:

1. **Type Safety**: All responses are validated Pydantic models
2. **Flexibility**: Models adapt to API changes automatically
3. **Protocol-Based Type Hints**: Static type checking with Protocols

### Working with Dynamic Models

```python
# All returned objects are Pydantic models
moments = await client.moments()

for moment in moments:
    # Access attributes directly
    print(moment.id)
    print(moment.kind_id)
    print(moment.moment_title)

    # Convert to dict
    moment_dict = moment.model_dump()

    # Access nested attributes safely
    if hasattr(moment, 'base'):
        print(moment.base.title)
```

### Static Models

Some models are statically defined for input:

```python
from youversion.models.moments import CreateMoment, ReferenceCreate
from youversion.enums import MomentKinds, StatusEnum

# CreateMoment - for creating moments
moment = CreateMoment(
    kind=MomentKinds.NOTE,
    content="My note",
    references=[...],
    title="Title",
    status=StatusEnum.PRIVATE,
    body="Body",
    color="ff0000",
    labels=["tag1"],
    language_tag="en"
)

# ReferenceCreate - for moment references
reference = ReferenceCreate(
    human="John 3:16",
    version_id=1,
    usfm=["JHN.3.16"]
)
```

### Enums

```python
from youversion.enums import MomentKinds, StatusEnum

# MomentKinds
MomentKinds.NOTE
MomentKinds.HIGHLIGHT
MomentKinds.BOOKMARK
MomentKinds.IMAGE
MomentKinds.BADGE
MomentKinds.PLAN_COMPLETION
MomentKinds.PLAN_SEGMENT_COMPLETION
MomentKinds.PLAN_SUBSCRIPTION
MomentKinds.FRIENDSHIP

# StatusEnum
StatusEnum.PRIVATE
StatusEnum.DRAFT
StatusEnum.PUBLIC
```

## Error Handling

The library provides robust error handling:

```python
from youversion.clients import AsyncClient

async def main():
try:
        async with AsyncClient() as client:
            result = await client.get_bible_version(99999)
    except ValueError as e:
        print(f"Validation error: {e}")
except Exception as e:
        print(f"API error: {e}")
    # Handle error appropriately

asyncio.run(main())
```

### Common Error Scenarios

1. **Authentication Errors**: Invalid credentials
2. **Validation Errors**: Invalid input parameters
3. **API Errors**: Server errors or rate limiting
4. **Network Errors**: Connection issues

## Best Practices

### 1. Use Context Managers

Always use context managers to ensure proper resource cleanup:

```python
# ✅ Good
async with AsyncClient() as client:
    moments = await client.moments()

# ❌ Bad
client = AsyncClient()
moments = await client.moments()
# Resources may not be cleaned up
```

### 2. Handle Errors Gracefully

```python
async with AsyncClient() as client:
    try:
        moments = await client.moments()
    except Exception as e:
        logger.error(f"Error fetching moments: {e}")
        # Fallback or retry logic
```

### 3. Use AsyncClient for Concurrent Operations

```python
# ✅ Good - concurrent execution
async with AsyncClient() as client:
    moments, highlights, notes = await asyncio.gather(
        client.moments(),
        client.highlights(),
        client.notes()
    )

# ❌ Less efficient - sequential execution
async with AsyncClient() as client:
    moments = await client.moments()
    highlights = await client.highlights()
    notes = await client.notes()
```

### 4. Use SyncClient for Simple Scripts

```python
# ✅ Good for simple scripts
with SyncClient() as client:
    moments = client.moments()
    print(f"Found {len(moments)} moments")
```

### 5. Pagination

Many endpoints support pagination:

```python
async with AsyncClient() as client:
    page = 1
    while True:
        moments = await client.moments(page=page)
        if not moments:
            break

        for moment in moments:
            print(moment.id)

        page += 1
```

### 6. Accessing Dynamic Model Attributes

```python
moments = await client.moments()
for moment in moments:
    # Safe attribute access
    moment_id = getattr(moment, 'id', None)

    # Convert to dict for flexible access
    moment_dict = moment.model_dump()
    title = moment_dict.get('moment_title', 'N/A')

    # Check for nested attributes
    if hasattr(moment, 'base') and hasattr(moment.base, 'title'):
        print(moment.base.title)
```

### 7. Environment Variables for Credentials

```python
# ✅ Good - use environment variables
import os
from youversion.clients import AsyncClient

client = AsyncClient(
    username=os.getenv("YOUVERSION_USERNAME"),
    password=os.getenv("YOUVERSION_PASSWORD")
)

# Or let it read from .env automatically
client = AsyncClient()  # Reads from .env or environment
```

## Complete Examples

### Example 1: Export All Notes

```python
import asyncio
from youversion.clients import AsyncClient

async def export_notes():
    async with AsyncClient() as client:
        all_notes = []
        page = 1

        while True:
            notes = await client.notes(page=page)
            if not notes:
                break

            all_notes.extend(notes)
            page += 1

        # Export to JSON
        import json
        notes_data = [note.model_dump() for note in all_notes]
        with open("notes.json", "w") as f:
            json.dump(notes_data, f, indent=2, default=str)

        print(f"Exported {len(all_notes)} notes")

asyncio.run(export_notes())
```

### Example 2: Search and Create Moment

```python
import asyncio
from youversion.clients import AsyncClient
from youversion.models.moments import CreateMoment, ReferenceCreate
from youversion.enums import MomentKinds, StatusEnum

async def search_and_create():
    async with AsyncClient() as client:
        # Search for verses about love
        results = await client.search_bible("love", version_id=1)

        # Get first result
        if results.get("verses"):
            verse = results["verses"][0]
            usfm = verse.get("usfm", ["JHN.3.16"])

            # Create a note about it
            reference = ReferenceCreate(
                human=verse.get("human", "John 3:16"),
                version_id=1,
                usfm=usfm
            )

            moment = CreateMoment(
                kind=MomentKinds.NOTE,
                content="Found this verse about love",
                references=[reference],
                title="Love Verse",
                status=StatusEnum.PRIVATE,
                body="This is a great verse about love",
                color="ff0000",
                labels=["love", "favorite"],
                language_tag="en"
            )

            result = await client.create_moment(moment)
            print(f"Created moment: {result}")

asyncio.run(search_and_create())
```

### Example 3: Get All User Content

```python
import asyncio
from youversion.clients import AsyncClient

async def get_all_content():
    async with AsyncClient() as client:
        # Get all content types concurrently
        moments, highlights, notes, bookmarks, badges = await asyncio.gather(
            client.moments(),
            client.highlights(),
            client.notes(),
            client.bookmarks(),
            client.badges()
        )

        print(f"Moments: {len(moments)}")
        print(f"Highlights: {len(highlights)}")
        print(f"Notes: {len(notes)}")
        print(f"Bookmarks: {len(bookmarks)}")
        print(f"Badges: {len(badges)}")

asyncio.run(get_all_content())
```

### Example 4: SyncClient Usage

```python
from youversion.clients import SyncClient

def main():
    with SyncClient() as client:
        # All operations are synchronous
        votd = client.verse_of_the_day()
        print(f"Verse of the Day: {votd.usfm}")

        moments = client.moments()
        print(f"Found {len(moments)} moments")

        highlights = client.highlights()
        print(f"Found {len(highlights)} highlights")

if __name__ == "__main__":
    main()
```

## API Response Format

All API responses are processed through the `DataProcessor` which converts raw API responses into dynamic Pydantic models. The raw API format is:

```json
{
  "response": {
    "code": 200,
    "data": {
      // Response data
    },
    "buildtime": "2025-01-20T20:58:45.062524+00:00"
  }
}
```

The client automatically extracts and processes the `data` field, returning structured Pydantic models.

## Rate Limiting

The YouVersion API has rate limits. The client handles this automatically with appropriate delays and retries. For best practices:

- Use `AsyncClient` with `asyncio.gather()` for concurrent requests
- Implement your own rate limiting if making many sequential requests
- Handle `429 Too Many Requests` errors gracefully

## Command Line Interface (CLI)

The library includes a comprehensive CLI with 47+ commands accessible via Poetry scripts, Makefile targets, or directly.

### Installation

The CLI is automatically available when you install the package:

```bash
# Using Poetry
poetry install
poetry run youversion --help

# Or using pip
pip install youversion-bible-client
youversion --help
```

### Standardized Output Format

All CLI commands use a standardized output format that displays:
- **ID**: Item identifier
- **Kind**: Item type (e.g., NOTE, HIGHLIGHT, PLAN_SEGMENT_COMPLETION.V1)
- **Metadata**: Key-value pairs from `base/title/l_args` (e.g., Segment, Title, etc.)
- **Time**: Creation timestamp

**Example Output:**
```
  1. PLAN_SEGMENT_COMPLETION.V1
     ID         : 4892085495582558077
     Kind       : PLAN_SEGMENT_COMPLETION.V1
     Segment    : 1
     Title      : Teach Us To Pray
     Time       : 2025-11-22T19:00:35+00:00
```

### Using Poetry Scripts

All commands are available as Poetry scripts:

```bash
# Moments & Content
poetry run votd                    # Get verse of the day
poetry run moments                 # Get moments
poetry run highlights              # Get highlights
poetry run notes                   # Get notes
poetry run bookmarks               # Get bookmarks
poetry run images                  # Get images
poetry run badges                  # Get badges
poetry run create-moment           # Create a moment
poetry run convert-notes           # Convert notes to markdown

# Plans
poetry run plan-progress           # Get plan progress
poetry run plan-subscriptions     # Get plan subscriptions
poetry run plan-completions       # Get plan completions

# Bible & Audio
poetry run get-bible-configuration # Get Bible configuration
poetry run get-bible-versions      # Get Bible versions
poetry run get-bible-version       # Get Bible version by ID
poetry run get-bible-chapter       # Get Bible chapter
poetry run get-recommended-languages # Get recommended languages
poetry run get-audio-chapter       # Get audio chapter
poetry run get-audio-version       # Get audio version

# Search
poetry run search-bible            # Search Bible
poetry run search-plans            # Search plans
poetry run search-users            # Search users

# And 25+ more commands...
```

### Using Makefile Commands

All commands are also available via Makefile:

```bash
# Moments & Content
make cli-votd                      # Get verse of the day
make cli-moments                   # Get moments
make cli-highlights                # Get highlights
make cli-notes                     # Get notes
make cli-bookmarks                 # Get bookmarks
make cli-images                    # Get images
make cli-badges                    # Get badges
make cli-create-moment KIND='note' CONTENT='...' TITLE='...'  # Create moment
make cli-convert-notes             # Convert notes to markdown

# Plans
make cli-plan-progress             # Get plan progress
make cli-plan-subscriptions        # Get plan subscriptions
make cli-plan-completions          # Get plan completions

# Bible & Audio
make cli-get-bible-configuration   # Get Bible configuration
make cli-get-bible-versions        # Get Bible versions
make cli-get-bible-version ID=1    # Get Bible version by ID
make cli-get-bible-chapter REFERENCE='GEN.1' VERSION_ID=1  # Get chapter
make cli-get-recommended-languages # Get recommended languages
make cli-get-audio-chapter REFERENCE='GEN.1' VERSION_ID=1  # Get audio chapter
make cli-get-audio-version ID=1    # Get audio version

# Search
make cli-search-bible QUERY='love' VERSION_ID=1  # Search Bible
make cli-search-plans QUERY='daily' LANGUAGE_TAG='en'  # Search plans
make cli-search-users QUERY='john'  # Search users

# See all commands: make help
```

### Direct CLI Usage

You can also use the CLI directly:

```bash
# Basic usage
youversion votd
youversion moments --page 2
youversion highlights --limit 5
youversion notes --json

# With options
youversion votd --day 100
youversion moments --page 1 --limit 20 --json
youversion create-moment --kind note --content "My note" --title "Title"
youversion get-bible-chapter GEN.1 --version-id 1
youversion search-bible "love" --version-id 1
```

### Global Options

All commands support these global options:

- `--json`: Output results in JSON format instead of human-readable format
- `--limit LIMIT`: Limit the number of items displayed (default: 10)

### Complete Command List

The CLI provides 47+ commands organized into categories:

**Moments & Content (9 commands):**
- `votd`, `moments`, `highlights`, `notes`, `bookmarks`, `images`, `badges`, `create-moment`, `convert-notes`

**Plans (3 commands):**
- `plan-progress`, `plan-subscriptions`, `plan-completions`

**Bible & Audio (7 commands):**
- `get-bible-configuration`, `get-bible-versions`, `get-bible-version`, `get-bible-chapter`, `get-recommended-languages`, `get-audio-chapter`, `get-audio-version`

**Search (3 commands):**
- `search-bible`, `search-plans`, `search-users`

**Videos & Images (4 commands):**
- `get-videos`, `get-video-details`, `get-images`, `get-image-upload-url`

**Events (6 commands):**
- `search-events`, `get-event-details`, `get-saved-events`, `save-event`, `delete-saved-event`, `get-all-saved-event-ids`, `get-event-configuration`

**Moments Management (8 commands):**
- `get-moments`, `get-moment-details`, `update-moment`, `delete-moment`, `get-moment-colors`, `get-moment-labels`, `get-verse-colors`, `hide-verse-colors`, `get-moments-configuration`

**Comments & Likes (4 commands):**
- `create-comment`, `delete-comment`, `like-moment`, `unlike-moment`

**Devices (2 commands):**
- `register-device`, `unregister-device`

**Themes (5 commands):**
- `get-themes`, `add-theme`, `remove-theme`, `set-theme`, `get-theme-description`

**Social (1 command):**
- `send-friend-request`

**Localization (1 command):**
- `get-localization-items`

For detailed usage of each command, run:

```bash
youversion <command> --help
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on GitHub or contact the maintainers.
