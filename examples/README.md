# YouVersion Bible Client Examples

This folder contains example scripts demonstrating how to use the YouVersion Bible Client library.

## Prerequisites

Before running any examples, make sure you have:

1. **Installed the library**:

   ```bash
   poetry install
   ```

2. **Set up your credentials**:
   - Create a `.env` file in the project root
   - Add your YouVersion credentials:
     ```env
     YOUVERSION_USERNAME=your_username_here
     YOUVERSION_PASSWORD=your_password_here
     ```

## Example Files

### 1. `basic_usage.py`

**Complete API methods example demonstrating ALL public methods**

This example demonstrates every public method available in the Client class:

- `verse_of_the_day(day=None)` - Get verse of the day (current or specific day)
- `moments(page=1)` - Get all moments (friendships, highlights, notes, images, etc.)
- `highlights(page=1)` - Get highlights only
- `notes(page=1)` - Get notes only
- `bookmarks(page=1)` - Get bookmarks only
- `my_images(page=1)` - Get images only
- `badges(page=1)` - Get badges only
- `plan_progress(page=1)` - Get plan progress/segment completion
- `plan_subscriptions(page=1)` - Get plan subscriptions
- `plan_completions(page=1)` - Get plan completions
- `convert_note_to_md()` - Convert notes to markdown format

**Run with**:

```bash
python examples/basic_usage.py
```

### 2. `comprehensive_api_demo.py`

**Comprehensive example demonstrating all YouVersion Bible API endpoints**

This example demonstrates all API categories:

- Bible API (configuration, versions, chapters, languages)
- Audio Bible API (audio chapters, audio versions)
- Search API (Bible text, plans, users)
- Moments API (configuration, colors, labels, verse of the day)
- Content API (moments, highlights, notes, bookmarks, badges, plans)
- Events API (search, details, saved events)
- Videos API (list, details)
- Images API (reference images, upload URLs)
- Themes API (list, descriptions)
- Localization API (localization strings)

**Run with**:

```bash
python examples/comprehensive_api_demo.py
```

### 3. `sync_vs_async.py`

**Synchronous vs Asynchronous Usage Comparison**

This example demonstrates the difference between using the synchronous SyncClient and the asynchronous AsyncClient:

```bash
# Run the example
python examples/sync_vs_async.py
```

**Features:**

- Performance comparison between sync and async operations
- Concurrent operations demonstration
- Execution time measurements
- Usage recommendations

### 4. `concurrent_requests.py`

**Concurrent requests and performance optimization**

This example demonstrates how to use all API methods concurrently:

- Using `asyncio.gather()` for parallel requests with all methods
- Using `asyncio.as_completed()` for streaming results
- Background tasks with all method types
- Batch requests with rate limiting
- Error handling in concurrent operations
- Retry logic for all methods

**Run with**:

```bash
python examples/concurrent_requests.py
```

### 5. `create_moment_example.py`

**Example demonstrating how to create moments**

This example shows how to create notes, highlights, and other moments using the `CreateMoment` model:

- Creating notes with references
- Creating highlights with multiple references
- Creating moments from dictionaries
- Getting moment details
- Listing and filtering moments

**Run with**:

```bash
python examples/create_moment_example.py
```

### 6. `poetry_scripts.py`

**Poetry Script Commands Demo**

This example demonstrates the equivalent of Poetry script commands and shows how to use them:

```bash
# Run the example
python examples/poetry_scripts.py

# Or use the actual Poetry commands
poetry run votd
poetry run moments
poetry run highlights
poetry run notes
poetry run bookmarks
poetry run images
poetry run plan-progress
poetry run plan-subscriptions
poetry run plan-completions
poetry run badges
poetry run convert-notes
```

**Available Poetry Script Commands:**

- `poetry run votd` - Get verse of the day
- `poetry run moments` - Get moments
- `poetry run highlights` - Get highlights
- `poetry run notes` - Get notes
- `poetry run bookmarks` - Get bookmarks
- `poetry run images` - Get images
- `poetry run plan-progress` - Get plan progress
- `poetry run plan-subscriptions` - Get plan subscriptions
- `poetry run plan-completions` - Get plan completions
- `poetry run badges` - Get badges
- `poetry run convert-notes` - Convert notes to markdown

**Main CLI with arguments:**

- `poetry run youversion votd --day 100`
- `poetry run youversion moments --page 2 --limit 5`
- `poetry run youversion highlights --json`
- `poetry run youversion search-bible "love" --version-id 1`
- `poetry run youversion get-bible-chapter GEN.1 --version-id 1`
- `poetry run youversion get-themes --language-tag eng`

See the full CLI documentation with `poetry run youversion --help` for all 56+ available commands.

## Running Examples

### Method 1: Direct Python execution

```bash
# Navigate to project root
cd youversion-bible-client

# Run any example
python examples/basic_usage.py
```

### Method 2: Using Poetry

```bash
# Navigate to project root
cd youversion-bible-client

# Run with Poetry
poetry run python examples/basic_usage.py
```

### Method 3: Using Poetry shell

```bash
# Navigate to project root
cd youversion-bible-client

# Activate Poetry environment
poetry shell

# Run examples
python examples/basic_usage.py
```

## Example Output

Each example provides detailed output showing:

- ✅ Success messages
- ❌ Error messages
- ⚠️ Warning messages
- 📖 Data retrieval results
- ⏱️ Performance metrics
- 🔄 Async operation status

## API Methods Coverage

### Content Methods

1. **`verse_of_the_day(day=None)`**
   - Gets verse of the day for current day or specific day
   - Returns `Votd` object with day, usfm, and image_id

2. **`moments(page=1)`**
   - Gets all types of moments (friendships, highlights, notes, images, etc.)
   - Returns list of dynamically created `Moment` objects
   - Supports pagination

3. **`highlights(page=1)`**
   - Gets highlights only
   - Returns list of `Highlight` objects
   - Includes references and actions

4. **`notes(page=1)`**
   - Gets notes only
   - Returns list of `Note` objects
   - Includes content, status, and references

5. **`bookmarks(page=1)`**
   - Gets bookmarks only
   - Returns list of bookmark data
   - Supports pagination

6. **`my_images(page=1)`**
   - Gets images only
   - Returns list of image data
   - Includes body_image and metadata

7. **`badges(page=1)`**
   - Gets badges only
   - Returns list of badge data
   - Supports pagination

8. **`plan_progress(page=1)`**
   - Gets plan progress/segment completion
   - Returns list of plan progress data
   - Includes completion percentages

9. **`plan_subscriptions(page=1)`**
   - Gets plan subscriptions
   - Returns list of subscription data
   - Includes plan titles and metadata

10. **`plan_completions(page=1)`**
    - Gets completed reading plans
    - Returns list of completion data
    - Supports pagination

11. **`convert_note_to_md()`**
    - Converts notes to markdown format
    - Returns processed note data
    - Useful for note export functionality

### Bible API Methods

- `get_bible_configuration()` - Get Bible configuration
- `get_bible_versions(language_tag, version_type)` - Get Bible versions
- `get_bible_version(version_id)` - Get specific version
- `get_bible_chapter(reference, version_id)` - Get chapter content
- `get_recommended_languages(country)` - Get recommended languages

### Audio API Methods

- `get_audio_chapter(reference, version_id)` - Get audio chapter
- `get_audio_version(audio_id)` - Get audio version

### Search API Methods

- `search_bible(query, version_id, book, page)` - Search Bible text
- `search_plans(query, language_tag, page)` - Search reading plans
- `search_users(query, language_tag, page)` - Search users

### Video API Methods

- `get_videos(language_tag)` - Get videos list
- `get_video_details(video_id)` - Get video details

### Image API Methods

- `get_images(reference, language_tag, page)` - Get images for reference
- `get_image_upload_url()` - Get image upload URL

### Event API Methods

- `search_events(query, latitude, longitude, page)` - Search events
- `get_event_details(event_id)` - Get event details
- `get_saved_events(page)` - Get saved events
- `save_event(event_id, comments)` - Save event
- `delete_saved_event(event_id)` - Delete saved event
- `get_all_saved_event_ids()` - Get all saved event IDs
- `get_event_configuration()` - Get event configuration

### Moment Management Methods

- `get_moments(page, user_id, kind, version_id, usfm)` - Get moments with filters
- `get_moment_details(moment_id)` - Get moment details
- `create_moment(data)` - Create a moment
- `update_moment(data)` - Update moment
- `delete_moment(moment_id)` - Delete moment
- `get_moment_colors()` - Get highlight colors
- `get_moment_labels()` - Get moment labels
- `get_verse_colors(usfm, version_id)` - Get verse colors
- `hide_verse_colors(data)` - Hide verse colors
- `get_moments_configuration()` - Get moments configuration

### Comment API Methods

- `create_comment(moment_id, comment)` - Create comment
- `delete_comment(comment_id)` - Delete comment

### Like API Methods

- `like_moment(moment_id)` - Like moment
- `unlike_moment(moment_id)` - Unlike moment

### Device API Methods

- `register_device(device_id, device_type, user_id, old_device_id, tags)` - Register device
- `unregister_device(device_id)` - Unregister device

### Theme API Methods

- `get_themes(page, language_tag)` - Get themes
- `add_theme(theme_id, available_locales, colors, cta_urls, msgid_suffix, version_ids)` - Add theme
- `remove_theme(theme_id)` - Remove theme
- `set_theme(theme_id, previous_theme_id)` - Set active theme
- `get_theme_description(theme_id, language_tag)` - Get theme description

### Friend API Methods

- `send_friend_request(user_id)` - Send friend request

### Localization API Methods

- `get_localization_items(language_tag)` - Get localization strings

## Common Issues

### 1. Missing Credentials

```
❌ Error: Please set YOUVERSION_USERNAME and YOUVERSION_PASSWORD environment variables
```

**Solution**: Create a `.env` file with your credentials

### 2. Network Errors

```
❌ Unexpected error: Connection timeout
```

**Solution**: Check your internet connection and try again

### 3. Invalid Credentials

```
❌ API error: Authentication failed
```

**Solution**: Verify your username and password are correct

### 4. Import Errors

```
ModuleNotFoundError: No module named 'youversion'
```

**Solution**: Make sure you're in the project root and have installed dependencies

## Best Practices

1. **Always use context managers**:

   ```python
   # Async
   async with AsyncClient() as client:
       # Your code here

   # Sync
   with SyncClient() as client:
       # Your code here
   ```

2. **Handle errors gracefully**:

   ```python
   try:
       votd = await client.verse_of_the_day()
   except Exception as e:
       print(f"Error: {e}")
   ```

3. **Use environment variables for credentials**:

   ```python
   # Good
   async with AsyncClient() as client:  # Uses .env

   # Bad
   async with AsyncClient("username", "password") as client:  # Hardcoded
   ```

4. **Implement rate limiting for multiple requests**:

   ```python
   await asyncio.sleep(1)  # Wait between requests
   ```

5. **Use concurrent requests for better performance**:
   ```python
   results = await asyncio.gather(
       client.verse_of_the_day(),
       client.moments(),
       client.highlights(),
       client.notes(),
       client.bookmarks(),
       client.my_images(),
       client.badges(),
       client.plan_progress(),
       client.plan_subscriptions(),
       client.plan_completions()
   )
   ```

## Method Parameters

### Common Parameters

- `page` (int, optional): Page number for paginated results. Defaults to 1.

### Specific Parameters

- `verse_of_the_day(day=None)`: `day` can be None (current day) or specific day number
- `convert_note_to_md()`: No parameters required
- `get_bible_versions(language_tag="eng", version_type="all")`: Language and type filters
- `search_bible(query, version_id=None, book=None, page=1)`: Search with optional filters

## Return Types

All methods return dynamically created Pydantic models that can be:

- Accessed as objects: `moment.id`, `moment.moment_title`
- Converted to dicts: `moment.model_dump()`
- Serialized to JSON: `json.dumps(moment.model_dump(), default=str)`

## Contributing

If you create new examples:

1. Follow the existing naming convention
2. Include comprehensive error handling
3. Add detailed comments and docstrings
4. Test with valid credentials
5. Update this README
6. Ensure all public methods are demonstrated

## Support

For issues or questions:

1. Check the main project README
2. Review the DOCS.md file for comprehensive documentation
3. Review the example code
4. Check your `.env` file configuration
5. Verify your internet connection
