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

### 1. `poetry_scripts.py`

**Poetry Script Commands Demo**

This example demonstrates the equivalent of Poetry script commands and shows how to use them:

```bash
# Run the example
python -m examples.poetry_scripts

# Or use the actual Poetry commands
poetry run votd
poetry run moments
poetry run highlights
poetry run notes
poetry run bookmarks
poetry run images
poetry run plan-progress
poetry run plan-subscriptions
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
- `poetry run convert-notes` - Convert notes to markdown

**Main CLI with arguments:**

- `poetry run youversion votd --day 100`
- `poetry run youversion moments --page 2 --limit 5`
- `poetry run youversion highlights --json`

### 2. `basic_usage.py`

**Complete API methods example demonstrating ALL public methods**

This example demonstrates every public method available in the Client class:

- `verse_of_the_day(day=None)` - Get verse of the day (current or specific day)
- `moments(page=1)` - Get all moments (friendships, highlights, notes, images, etc.)
- `highlights(page=1)` - Get highlights only
- `notes(page=1)` - Get notes only
- `bookmarks(page=1)` - Get bookmarks only
- `my_images(page=1)` - Get images only
- `plan_progress(page=1)` - Get plan progress/segment completion
- `plan_subscriptions(page=1)` - Get plan subscriptions
- `convert_note_to_md()` - Convert notes to markdown format

**Run with**:

```bash
python examples/basic_usage.py
```

### 3. `sync_vs_async.py`

**Synchronous vs Asynchronous Usage Comparison**

This example demonstrates the difference between using the synchronous SyncClient and the asynchronous AsyncClient:

```bash
# Run the example
python -m examples.sync_vs_async
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

### All Public Methods Demonstrated

1. **`verse_of_the_day(day=None)`**

   - Gets verse of the day for current day or specific day
   - Returns `Votd` object with day, usfm, and image_id

2. **`moments(page=1)`**

   - Gets all types of moments (friendships, highlights, notes, images, etc.)
   - Returns list of `Moment` objects
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

7. **`plan_progress(page=1)`**

   - Gets plan progress/segment completion
   - Returns list of plan progress data
   - Includes completion percentages

8. **`plan_subscriptions(page=1)`**

   - Gets plan subscriptions
   - Returns list of subscription data
   - Includes plan titles and metadata

9. **`convert_note_to_md()`**
   - Converts notes to markdown format
   - Returns processed note data
   - Useful for note export functionality

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

1. **Always use async context managers**:

   ```python
   async with Client() as client:
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
   async with Client() as client:  # Uses .env

   # Bad
   async with Client("username", "password") as client:  # Hardcoded
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
       client.plan_progress(),
       client.plan_subscriptions(),
       client.convert_note_to_md()
   )
   ```

## Method Parameters

### Common Parameters

- `page` (int, optional): Page number for paginated results. Defaults to 1.

### Specific Parameters

- `verse_of_the_day(day=None)`: `day` can be None (current day) or specific day number
- `convert_note_to_md()`: No parameters required

## Return Types

- `verse_of_the_day()` → `Votd` object
- `moments()` → `List[Moment]`
- `highlights()` → `List[Highlight]`
- `notes()` → `List[Note]`
- `bookmarks()` → `List[dict]`
- `my_images()` → `List[dict]`
- `plan_progress()` → `List[dict]`
- `plan_subscriptions()` → `List[dict]`
- `convert_note_to_md()` → `List[dict]`

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
2. Review the example code
3. Check your `.env` file configuration
4. Verify your internet connection
