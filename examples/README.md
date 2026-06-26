# Examples

Runnable scripts for the YouVersion Bible client. All authenticated examples need `.env` credentials.

## Setup

```bash
uv sync
```

```env
# .env
YOUVERSION_USERNAME=your_username
YOUVERSION_PASSWORD=your_password
```

## Scripts

| File | What it shows |
|------|----------------|
| `basic_usage.py` | Core moment methods, VOTD, plans, concurrent fetch |
| `comprehensive_api_demo.py` | Bible, audio, search, events, friends, notifications |
| `create_moment_example.py` | Creating notes and highlights |
| `sync_vs_async.py` | `SyncClient` vs `AsyncClient` |
| `concurrent_requests.py` | Parallel API calls with asyncio |
| `cli_scripts.py` | Console script entry points (`uv run votd`, etc.) |

## Run

```bash
uv run python examples/basic_usage.py
uv run python examples/comprehensive_api_demo.py
```

## Sample output shape

Verse of the day:

```json
{"day": 178, "usfm": ["ISA.43.18", "ISA.43.19"]}
```

Bible chapter (`get_bible_chapter("GEN.1", version_id=1)`):

```json
{
  "reference": {"usfm": ["GEN.1"], "human": "Genesis 1", "version_id": 1}
}
```

## Notes

- Use `version_id=1` for KJV when trying chapter lookups.
- `get_bible_configuration().default_versions[].id` is a **language** id, not a version id.
- Friend suggestions need `language_tag="en"`.
- User badges: call `badges()`, not a separate badges API.

See [DOCS.md](../DOCS.md) for the full method list.
