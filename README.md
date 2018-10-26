# YouVersion Bible API Client

This project came about when I was looking to export all my notes from the Youversion Bible app. Please use responsibly.


A comprehensive Python client library for accessing the YouVersion Bible API. This library provides both synchronous and asynchronous interfaces to interact with all YouVersion API endpoints.


## Installation

```bash
pip install youversion-bible-client
```

## Quick Start

### Asynchronous Usage

```python
import asyncio
from youversion import AsyncClient

async def main():
    async with AsyncClient() as client:
        # Get Bible configuration
        config = await client.get_bible_configuration()
        print(f"Total versions: {config['response']['data']['totals']['versions']}")

        # Get Bible versions
        versions = await client.get_bible_versions("eng", "all")
        print(f"Found {len(versions['response']['data']['versions'])} English versions")

        # Search Bible text
        results = await client.search_bible("love", version_id=1)
        print(f"Search results: {results}")

asyncio.run(main())
```

### Synchronous Usage

```python
from youversion import SyncClient

with SyncClient() as client:
    # Get Bible configuration
    config = client.get_bible_configuration()
    print(f"Total versions: {config['response']['data']['totals']['versions']}")

    # Get Bible versions
    versions = client.get_bible_versions("eng", "all")
    print(f"Found {len(versions['response']['data']['versions'])} English versions")
```

## API Endpoints

### Bible API

Access Bible content, versions, and configuration.

```python
# Get Bible configuration
config = await client.get_bible_configuration()

# Get Bible versions for a language
versions = await client.get_bible_versions("eng", "all")

# Get specific version details
version = await client.get_bible_version(version_id)

# Get chapter content
chapter = await client.get_bible_chapter(version_id, "GEN.1")

# Get recommended languages for a country
languages = await client.get_recommended_languages("US")
```

### Audio Bible API

Access audio Bible content and versions.

```python
# Get audio chapter information
audio_chapter = await client.get_audio_chapter(version_id, "GEN.1")

# Get audio version details
audio_version = await client.get_audio_version(audio_id)
```

### Search API

Search across Bible text, reading plans, and users.

```python
# Search Bible text
results = await client.search_bible("love", version_id=1, book="JHN")

# Search reading plans
plans = await client.search_plans("daily", "eng")

# Search users
users = await client.search_users("john", "eng")
```

### Moments API

Manage notes, highlights, bookmarks, and other user moments.

```python
# Get moments list
moments = await client.get_moments(page=1, kind="note")

# Get moment details
moment = await client.get_moment_details(moment_id)

# Create a moment
new_moment = await client.create_moment({
    "kind": "note",
    "content": "My note",
    "reference": "GEN.1.1"
})

# Update a moment
updated = await client.update_moment({
    "id": moment_id,
    "content": "Updated note"
})

# Delete a moment
await client.delete_moment(moment_id)

# Get available highlight colors
colors = await client.get_moment_colors()

# Get moment labels
labels = await client.get_moment_labels()

# Get verse highlight colors
verse_colors = await client.get_verse_colors("GEN.1.1", version_id)

# Hide verse colors
await client.hide_verse_colors({"verses": ["GEN.1.1"]})

# Get verse of the day
votd = await client.get_verse_of_the_day_new("eng")

# Get moments configuration
config = await client.get_moments_configuration()
```

### Comments API

Manage comments on moments.

```python
# Create a comment
comment = await client.create_comment(moment_id, "Great verse!")

# Delete a comment
await client.delete_comment(comment_id)
```

### Likes API

Manage likes on moments.

```python
# Like a moment
await client.like_moment(moment_id)

# Unlike a moment
await client.unlike_moment(moment_id)
```

### Events API

Search and manage church events.

```python
# Search events
events = await client.search_events("church", latitude=40.7128, longitude=-74.0060)

# Get event details
event = await client.get_event_details(event_id)

# Get saved events
saved = await client.get_saved_events()

# Save an event
await client.save_event(event_id, {"note": "My personal note"})

# Delete saved event
await client.delete_saved_event(event_id)

# Get all saved event IDs
ids = await client.get_all_saved_event_ids()

# Get event configuration
config = await client.get_event_configuration()
```

### Videos API

Access video content.

```python
# Get videos list
videos = await client.get_videos("eng")

# Get video details
video = await client.get_video_details(video_id)
```

### Badges API

Access user badges and achievements.

```python
# Get user badges
badges = await client.get_badges(user_id)
```

### Images API

Manage images and media.

```python
# Get images for a reference
images = await client.get_images("GEN.1.1", "eng")

# Get image upload URL
upload_info = await client.get_image_upload_url()
```

### Messaging API

Manage push notifications and device registration.

```python
# Register device for push notifications
await client.register_device(
    device_id="device_token",
    device_type="android",
    user_id=user_id,
    tags="reading_plan_yes"
)

# Unregister device
await client.unregister_device("device_token")
```

### Themes API

Manage app themes.

```python
# Get available themes
themes = await client.get_themes(page=1, language_tag="eng")

# Add theme to collection
await client.add_theme(theme_id)

# Remove theme from collection
await client.remove_theme(theme_id)

# Set active theme
await client.set_theme(theme_id, previous_theme_id)

# Get theme description
description = await client.get_theme_description(theme_id, "eng")
```

### Localization API

Access localization strings.

```python
# Get localization strings
localization = await client.get_localization_items("eng")
```

## Authentication

Some endpoints require authentication. Initialize the client with credentials:

```python
# Asynchronous
async with AsyncClient(username="your_username", password="your_password") as client:
    # Authenticated API calls
    moments = await client.get_moments()

# Synchronous
with SyncClient(username="your_username", password="your_password") as client:
    # Authenticated API calls
    moments = client.get_moments()
```

## Data Models

The library includes comprehensive data models for all API responses:

```python
from youversion.models import (
    Version, Language, Publisher, Book, Chapter,
    Moment, MomentComment, MomentLike,
    Event, EventLocation, EventTime,
    Friend, Contact, UserBase,
    ApiError, ApiResponse
)
```

## Error Handling

The library provides robust error handling:

```python
try:
    result = await client.get_bible_version(version_id)
except Exception as e:
    print(f"Error: {e}")
    # Handle error appropriately
```

## Examples

See the `examples/` directory for comprehensive usage examples:

- `comprehensive_api_demo.py` - Demonstrates all API endpoints
- `basic_usage.py` - Basic usage examples
- `sync_vs_async.py` - Comparison of sync vs async usage

## API Response Format

All API responses follow this format:

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

## Rate Limiting

The YouVersion API has rate limits. The client handles this automatically with appropriate delays and retries.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on GitHub or contact the maintainers.