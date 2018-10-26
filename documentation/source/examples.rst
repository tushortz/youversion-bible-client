Usage Examples
==============

This section provides comprehensive examples of using the YouVersion Bible Client.

Basic Examples
--------------

Getting Verse of the Day
~~~~~~~~~~~~~~~~~~~~~~~~

Synchronous usage:

.. code-block:: python

   from youversion import Client

   with Client() as client:
       votd = client.verse_of_the_day()
       print(f"Today's verse: {votd.usfm}")
       print(f"Day: {votd.day}")

Asynchronous usage:

.. code-block:: python

   import asyncio
   from youversion import AsyncClient

   async def main():
       async with AsyncClient() as client:
           votd = await client.verse_of_the_day()
           print(f"Today's verse: {votd.usfm}")
           print(f"Day: {votd.day}")

   asyncio.run(main())

Getting Highlights
~~~~~~~~~~~~~~~~~~

Synchronous usage:

.. code-block:: python

   from youversion import Client

   with Client() as client:
       highlights = client.highlights()
       print(f"Found {len(highlights)} highlights")

       for highlight in highlights[:5]:  # First 5 highlights
           print(f"Title: {highlight.moment_title}")
           print(f"References: {[ref.human for ref in highlight.references]}")
           print(f"Time: {highlight.time_ago}")
           print("-" * 40)

Asynchronous usage:

.. code-block:: python

   import asyncio
   from youversion import AsyncClient

   async def main():
       async with AsyncClient() as client:
           highlights = await client.highlights()
           print(f"Found {len(highlights)} highlights")

           for highlight in highlights[:5]:
               print(f"Title: {highlight.moment_title}")
               print(f"References: {[ref.human for ref in highlight.references]}")
               print(f"Time: {highlight.time_ago}")
               print("-" * 40)

   asyncio.run(main())

Getting Notes
~~~~~~~~~~~~~

Synchronous usage:

.. code-block:: python

   from youversion import Client

   with Client() as client:
       notes = client.notes()
       print(f"Found {len(notes)} notes")

       for note in notes[:3]:  # First 3 notes
           print(f"Title: {note.moment_title}")
           print(f"Content: {note.content[:100]}...")
           print(f"Status: {note.status.value}")
           print(f"Time: {note.time_ago}")
           print("-" * 40)

Asynchronous usage:

.. code-block:: python

   import asyncio
   from youversion import AsyncClient

   async def main():
       async with AsyncClient() as client:
           notes = await client.notes()
           print(f"Found {len(notes)} notes")

           for note in notes[:3]:
               print(f"Title: {note.moment_title}")
               print(f"Content: {note.content[:100]}...")
               print(f"Status: {note.status.value}")
               print(f"Time: {note.time_ago}")
               print("-" * 40)

   asyncio.run(main())

Advanced Examples
-----------------

Concurrent Requests
~~~~~~~~~~~~~~~~~~~

Using asyncio.gather() for concurrent requests:

.. code-block:: python

   import asyncio
   from youversion import AsyncClient

   async def get_all_data():
       async with AsyncClient() as client:
           # Make concurrent requests
           votd, highlights, notes = await asyncio.gather(
               client.verse_of_the_day(),
               client.highlights(),
               client.notes()
           )

           print(f"Verse of the day: {votd.usfm}")
           print(f"Highlights: {len(highlights)}")
           print(f"Notes: {len(notes)}")

   asyncio.run(get_all_data())

Pagination
~~~~~~~~~~

Handling paginated results:

.. code-block:: python

   import asyncio
   from youversion import AsyncClient

   async def get_all_highlights():
       async with AsyncClient() as client:
           all_highlights = []
           page = 1

           while True:
               highlights = await client.highlights(page=page)
               if not highlights:
                   break

               all_highlights.extend(highlights)
               print(f"Page {page}: {len(highlights)} highlights")
               page += 1

               # Limit to first 3 pages for demo
               if page > 3:
                   break

           print(f"Total highlights: {len(all_highlights)}")
           return all_highlights

   asyncio.run(get_all_highlights())

Error Handling
~~~~~~~~~~~~~~

Comprehensive error handling:

.. code-block:: python

   import asyncio
   from youversion import AsyncClient
   import httpx

   async def safe_get_data():
       try:
           async with AsyncClient() as client:
               votd = await client.verse_of_the_day()
               return votd
       except ValueError as e:
           print(f"Authentication error: {e}")
           return None
       except httpx.HTTPStatusError as e:
           print(f"HTTP error: {e.response.status_code}")
           return None
       except Exception as e:
           print(f"Unexpected error: {e}")
           return None

   result = asyncio.run(safe_get_data())
   if result:
       print(f"Success: {result.usfm}")

Data Processing Examples
------------------------

Processing Highlights
~~~~~~~~~~~~~~~~~~~~~

Extract and process highlight data:

.. code-block:: python

   import asyncio
   from youversion import AsyncClient
   from collections import Counter

   async def analyze_highlights():
       async with AsyncClient() as client:
           highlights = await client.highlights()

           # Count references by book
           book_counts = Counter()
           for highlight in highlights:
               for ref in highlight.references:
                   book = ref.human.split(':')[0]  # Extract book name
                   book_counts[book] += 1

           print("Most highlighted books:")
           for book, count in book_counts.most_common(5):
               print(f"{book}: {count} highlights")

   asyncio.run(analyze_highlights())

Converting Notes to Markdown
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Convert notes to markdown format:

.. code-block:: python

   import asyncio
   from youversion import AsyncClient

   async def convert_notes_to_markdown():
       async with AsyncClient() as client:
           notes_md = await client.convert_note_to_md()

           print("Converted notes to markdown:")
           print(f"Processed {len(notes_md)} notes")

           # Save to file
           with open('notes.md', 'w', encoding='utf-8') as f:
               for note in notes_md:
                   f.write(f"# {note.get('title', 'Untitled')}\n\n")
                   f.write(f"{note.get('content', '')}\n\n")
                   f.write("---\n\n")

   asyncio.run(convert_notes_to_markdown())

CLI Integration Examples
------------------------

Using CLI from Python
~~~~~~~~~~~~~~~~~~~~~

Call CLI commands from Python:

.. code-block:: python

   import subprocess
   import json

   def get_votd_json():
       """Get verse of the day as JSON using CLI"""
       result = subprocess.run(
           ['poetry', 'run', 'youversion', 'votd', '--json'],
           capture_output=True,
           text=True
       )

       if result.returncode == 0:
           return json.loads(result.stdout)
       else:
           print(f"Error: {result.stderr}")
           return None

   votd_data = get_votd_json()
   if votd_data:
       print(f"Verse: {votd_data['usfm']}")

Batch Processing
~~~~~~~~~~~~~~~~

Process multiple CLI commands:

.. code-block:: python

   import subprocess
   import json

   def batch_cli_commands():
       """Run multiple CLI commands and collect results"""
       commands = [
           ['poetry', 'run', 'youversion', 'votd', '--json'],
           ['poetry', 'run', 'youversion', 'highlights', '--limit', '5', '--json'],
           ['poetry', 'run', 'youversion', 'notes', '--limit', '3', '--json']
       ]

       results = {}
       for i, cmd in enumerate(commands):
           result = subprocess.run(cmd, capture_output=True, text=True)
           if result.returncode == 0:
               results[f'command_{i}'] = json.loads(result.stdout)
           else:
               results[f'command_{i}'] = {'error': result.stderr}

       return results

   data = batch_cli_commands()
   print("Batch processing results:")
   for key, value in data.items():
       print(f"{key}: {type(value)}")

Configuration Examples
----------------------

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Setting up environment variables:

.. code-block:: python

   import os
   from youversion import Client

   # Set environment variables programmatically
   os.environ['YOUVERSION_USERNAME'] = 'your_username'
   os.environ['YOUVERSION_PASSWORD'] = 'your_password'

   with Client() as client:
       votd = client.verse_of_the_day()
       print(f"Success: {votd.usfm}")

Custom Configuration
~~~~~~~~~~~~~~~~~~~~

Using custom configuration:

.. code-block:: python

   import asyncio
   from youversion import AsyncClient

   async def custom_config():
       # Pass credentials directly
       async with AsyncClient(
           username='your_username',
           password='your_password'
       ) as client:
           votd = await client.verse_of_the_day()
           print(f"Success: {votd.usfm}")

   asyncio.run(custom_config())

Testing Examples
----------------

Unit Testing
~~~~~~~~~~~~

Example unit test:

.. code-block:: python

   import pytest
   from unittest.mock import AsyncMock, patch
   from youversion import AsyncClient

   @pytest.mark.asyncio
   async def test_verse_of_the_day():
       with patch('youversion.clients.AsyncClient') as mock_client:
           # Mock the response
           mock_votd = AsyncMock()
           mock_votd.usfm = ["JHN.3.16"]
           mock_votd.day = 1

           mock_client.return_value.__aenter__.return_value.verse_of_the_day.return_value = mock_votd

           async with AsyncClient() as client:
               votd = await client.verse_of_the_day()
               assert votd.usfm == ["JHN.3.16"]
               assert votd.day == 1

Integration Testing
~~~~~~~~~~~~~~~~~~~

Example integration test:

.. code-block:: python

   import pytest
   from youversion import Client

   @pytest.mark.integration
   def test_real_api_call():
       """Test with real API (requires valid credentials)"""
       with Client() as client:
           votd = client.verse_of_the_day()
           assert votd.day is not None
           assert votd.usfm is not None
           assert len(votd.usfm) > 0

Performance Examples
--------------------

Timing Operations
~~~~~~~~~~~~~~~~~

Measure performance:

.. code-block:: python

   import asyncio
   import time
   from youversion import AsyncClient

   async def measure_performance():
       async with AsyncClient() as client:
           start_time = time.time()

           # Measure individual operations
           votd_start = time.time()
           votd = await client.verse_of_the_day()
           votd_time = time.time() - votd_start

           highlights_start = time.time()
           highlights = await client.highlights()
           highlights_time = time.time() - highlights_start

           total_time = time.time() - start_time

           print(f"Verse of the day: {votd_time:.2f}s")
           print(f"Highlights: {highlights_time:.2f}s")
           print(f"Total time: {total_time:.2f}s")

   asyncio.run(measure_performance())

Caching Results
~~~~~~~~~~~~~~~

Simple caching example:

.. code-block:: python

   import asyncio
   import time
   from youversion import AsyncClient

   class CachedClient:
       def __init__(self):
           self.cache = {}
           self.cache_timeout = 300  # 5 minutes

       async def get_cached_votd(self):
           now = time.time()
           if 'votd' in self.cache:
               data, timestamp = self.cache['votd']
               if now - timestamp < self.cache_timeout:
                   return data

           async with AsyncClient() as client:
               votd = await client.verse_of_the_day()
               self.cache['votd'] = (votd, now)
               return votd

   async def use_cached_client():
       cached_client = CachedClient()

       # First call - hits API
       votd1 = await cached_client.get_cached_votd()
       print(f"First call: {votd1.usfm}")

       # Second call - uses cache
       votd2 = await cached_client.get_cached_votd()
       print(f"Second call: {votd2.usfm}")

   asyncio.run(use_cached_client())
