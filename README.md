# YouVersion Bible API Client

This project came about when I was looking to export all my notes from the Youversion Bible app. Please use responsibly.


A comprehensive Python client library for accessing the YouVersion Bible API. This library provides both synchronous and asynchronous interfaces to interact with all YouVersion API endpoints.


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


## Quick start

### Client

## Examples

### Create sync client

The sync client is a wrapper on top of the asynchronous client. See [DOCS.md](./DOCS.md) on examples on how to use

```py
from youversion.clients import SyncClient

client = SyncClient()

# get verse of the day
client.verse_of_the_day()
```

### creating async client

```py
import asyncio
from youversion.clients import AsyncClient

async def main():
    # Using async context manager (recommended)
    async with AsyncClient() as client:
        # Get verse of the day
        votd = await client.verse_of_the_day()
```


### Verse of the day

```py
# get's the current day's votd
result = client.verse_of_the_day()

# get's specified votd
client.verse_of_the_day(day=365)
```

### Moments

#### Get moments

Moments fall into different categories such as `bookmark`, `highlight`, `note`, `image`, `badge`, `plan_subscription`, `plan_completion`, `plan_segment_completion`, `friendship`

Moments take optional page parameters. default is page 1

```py
client.badges()
client.bookmarks()
client.friendships()
client.highlights()
client.moments()
client.my_images()
client.notes()
client.plan_completions()
client.plan_progress()
client.plan_subscriptions()
```

#### Create a moment

```py
# Some fields are optional or provide default values.
# infer those from the method type hints
# version_id for example kjv = 1
client.create_moment(
    {
        "kind": "note",
        "content": "My genesis 10:2 note body",
        "references": [
            {"human": "genesis 10:2", "version_id": 1, "usfm": ["GEN.10.2"]}
        ],
        "title": "My genesis 10:2 note",
        "status": "private",
        "body": "My genesis 10:2 note body",
        "color": "ff0000",
        "labels": ["test"],
        "language_tag": "en",
    }
)
```

### Bible

#### Verse search

```py
client.search_bible("christ died for us")
```

#### Get bible chapter

```py
client.get_bible_chapter(reference="GEN.1")
```

### Bible versions

```py
client.get_bible_versions()

# you can specify a 3 digit language tag. e.g. ita for italian
# default is eng (english)
client.get_bible_versions(language_tag="eng")

# You can also get a single bible version detail
client.get_bible_version(version_id=1)
```

### Bible Audio

```py
# version id defaults to 1 (kjv)
client.get_audio_chapter(reference="GEN.1")
client.get_audio_chapter(reference="GEN.1", version_id=1)

# Get audio version details
client.get_audio_version(audio_id=1)
```


### Friends

#### Send friend request

```py
client.send_friend_request(user_id=123456789)
```