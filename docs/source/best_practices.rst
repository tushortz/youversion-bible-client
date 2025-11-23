Best Practices
==============

This guide covers best practices for using the YouVersion Bible Client effectively and efficiently.

Client Management
-----------------

Reuse Client Instances
~~~~~~~~~~~~~~~~~~~~~~

**Good**: Reuse a single client instance for multiple requests:

.. code-block:: python

   async with AsyncClient() as client:
       votd = await client.verse_of_the_day()
       highlights = await client.highlights()
       notes = await client.notes()
       # All requests use the same authenticated session

**Bad**: Creating new clients for each request:

.. code-block:: python

   # Inefficient - creates new client each time
   votd = await AsyncClient().verse_of_the_day()
   highlights = await AsyncClient().highlights()  # New authentication!

Use Context Managers
~~~~~~~~~~~~~~~~~~~~

Always use context managers for automatic cleanup:

.. code-block:: python

   # Good - automatic cleanup
   async with AsyncClient() as client:
       result = await client.verse_of_the_day()

   # Bad - manual cleanup required
   client = AsyncClient()
   result = await client.verse_of_the_day()
   await client.close()  # Easy to forget!

Concurrency
-----------

Use AsyncClient for Concurrent Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Good**: Make concurrent requests with AsyncClient:

.. code-block:: python

   import asyncio
   from youversion.clients import AsyncClient

   async def get_all_data():
       async with AsyncClient() as client:
           # All requests happen concurrently
           votd, highlights, notes = await asyncio.gather(
               client.verse_of_the_day(),
               client.highlights(),
               client.notes()
           )
           return votd, highlights, notes

   results = asyncio.run(get_all_data())

**Less Efficient**: Sequential requests:

.. code-block:: python

   # Slower - requests happen one after another
   votd = await client.verse_of_the_day()
   highlights = await client.highlights()  # Waits for votd
   notes = await client.notes()  # Waits for highlights

Batch Operations
~~~~~~~~~~~~~~~~

Batch similar operations together:

.. code-block:: python

   import asyncio
   from youversion.clients import AsyncClient

   async def get_all_moments():
       async with AsyncClient() as client:
           # Get all moment types concurrently
           results = await asyncio.gather(
               client.highlights(page=1),
               client.notes(page=1),
               client.bookmarks(page=1),
               client.my_images(page=1),
               client.badges(page=1),
               return_exceptions=True  # Don't fail if one fails
           )
           return results

   results = asyncio.run(get_all_moments())

Pagination
----------

Handle Pagination Efficiently
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Good**: Use async iteration for pagination:

.. code-block:: python

   import asyncio
   from youversion.clients import AsyncClient

   async def get_all_highlights():
       async with AsyncClient() as client:
           all_highlights = []
           page = 1

           while True:
               highlights = await client.highlights(page=page)
               if not highlights:
                   break

               all_highlights.extend(highlights)
               page += 1

               # Optional: limit pages to avoid excessive requests
               if page > 10:
                   break

           return all_highlights

   highlights = asyncio.run(get_all_highlights())

**Better**: Use concurrent pagination with limits:

.. code-block:: python

   async def get_pages_concurrently(max_pages=5):
       async with AsyncClient() as client:
           # Get multiple pages concurrently
           tasks = [
               client.highlights(page=i)
               for i in range(1, max_pages + 1)
           ]
           results = await asyncio.gather(*tasks, return_exceptions=True)
           # Flatten results
           all_highlights = []
           for result in results:
               if isinstance(result, list):
                   all_highlights.extend(result)
           return all_highlights

Data Processing
---------------

Process Data Efficiently
~~~~~~~~~~~~~~~~~~~~~~~~~

**Good**: Process data in batches:

.. code-block:: python

   from youversion.clients import SyncClient

   with SyncClient() as client:
       highlights = client.highlights(page=1)

       # Process in batches
       batch_size = 10
       for i in range(0, len(highlights), batch_size):
           batch = highlights[i:i + batch_size]
           process_batch(batch)

**Good**: Use list comprehensions for filtering:

.. code-block:: python

   with SyncClient() as client:
       highlights = client.highlights(page=1)

       # Filter highlights
       recent = [h for h in highlights if h.time_ago == "just now"]
       long_highlights = [h for h in highlights if len(h.text or "") > 100]

Error Handling
--------------

Comprehensive Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Always implement proper error handling:

.. code-block:: python

   import asyncio
   import httpx
   from youversion.clients import AsyncClient

   async def safe_api_call():
       try:
           async with AsyncClient() as client:
               return await client.verse_of_the_day()
       except ValueError as e:
           # Handle configuration errors
           print(f"Configuration error: {e}")
           return None
       except httpx.HTTPStatusError as e:
           # Handle HTTP errors
           if e.response.status_code == 429:
               print("Rate limited - waiting...")
               await asyncio.sleep(60)
               # Retry
               async with AsyncClient() as client:
                   return await client.verse_of_the_day()
           return None
       except Exception as e:
           # Handle unexpected errors
           print(f"Unexpected error: {e}")
           return None

   result = asyncio.run(safe_api_call())

Caching
-------

Implement Caching for Expensive Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cache results that don't change frequently:

.. code-block:: python

   import asyncio
   import time
   from functools import lru_cache
   from youversion.clients import SyncClient

   # Cache Bible versions (rarely change)
   @lru_cache(maxsize=1)
   def get_cached_versions():
       with SyncClient() as client:
           return client.get_bible_versions("eng", "all")

   # First call - hits API
   versions1 = get_cached_versions()

   # Second call - uses cache
   versions2 = get_cached_versions()  # Much faster!

Custom Caching
~~~~~~~~~~~~~~

Implement time-based caching:

.. code-block:: python

   import time
   from youversion.clients import AsyncClient

   class CachedClient:
       def __init__(self, cache_ttl=300):  # 5 minutes
           self.cache = {}
           self.cache_ttl = cache_ttl

       async def get_cached_votd(self):
           now = time.time()
           cache_key = 'votd'

           if cache_key in self.cache:
               data, timestamp = self.cache[cache_key]
               if now - timestamp < self.cache_ttl:
                   return data

           async with AsyncClient() as client:
               votd = await client.verse_of_the_day()
               self.cache[cache_key] = (votd, now)
               return votd

   cached_client = CachedClient()
   votd = await cached_client.get_cached_votd()

Performance Optimization
------------------------

Minimize API Calls
~~~~~~~~~~~~~~~~~

**Good**: Get all needed data in one session:

.. code-block:: python

   async with AsyncClient() as client:
       # Single session, multiple calls
       votd = await client.verse_of_the_day()
       highlights = await client.highlights()
       notes = await client.notes()

**Bad**: Multiple sessions:

.. code-block:: python

   # Multiple authentication sessions
   votd = await AsyncClient().verse_of_the_day()
   highlights = await AsyncClient().highlights()  # New auth!

Use Appropriate Client Type
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Use **AsyncClient** for async applications and concurrent operations
* Use **SyncClient** for simple scripts and synchronous code
* Don't mix both in the same application

Resource Management
-------------------

Clean Up Resources
~~~~~~~~~~~~~~~~~~

Always close clients properly:

.. code-block:: python

   # Good - automatic cleanup
   async with AsyncClient() as client:
       result = await client.verse_of_the_day()

   # Also good - explicit cleanup
   client = AsyncClient()
   try:
       result = await client.verse_of_the_day()
   finally:
       await client.close()

Memory Management
~~~~~~~~~~~~~~~~~

For large datasets, process in chunks:

.. code-block:: python

   async def process_large_dataset():
       async with AsyncClient() as client:
           page = 1
           while True:
               highlights = await client.highlights(page=page)
               if not highlights:
                   break

               # Process chunk
               for highlight in highlights:
                   process_highlight(highlight)

               page += 1

               # Optional: clear memory
               del highlights

Security
--------

Secure Credential Storage
~~~~~~~~~~~~~~~~~~~~~~~~~

**Good**: Use environment variables:

.. code-block:: python

   import os
   from youversion.clients import AsyncClient

   username = os.getenv("YOUVERSION_USERNAME")
   password = os.getenv("YOUVERSION_PASSWORD")

   client = AsyncClient(username=username, password=password)

**Bad**: Hardcode credentials:

.. code-block:: python

   # Never do this!
   client = AsyncClient(
       username="my_username",  # Exposed in code!
       password="my_password"   # Security risk!
   )

Validate Input
~~~~~~~~~~~~~~

Always validate user input:

.. code-block:: python

   def safe_search(query: str):
       if not query or len(query) < 2:
           raise ValueError("Query must be at least 2 characters")
       if len(query) > 100:
           raise ValueError("Query too long")

       with SyncClient() as client:
           return client.search_bible(query)

Code Organization
-----------------

Separate Concerns
~~~~~~~~~~~~~~~~

Organize code into logical modules:

.. code-block:: python

   # api_client.py
   from youversion.clients import AsyncClient

   class BibleAPIClient:
       def __init__(self):
           self.client = AsyncClient()

       async def get_daily_verse(self):
           return await self.client.verse_of_the_day()

   # data_processor.py
   class DataProcessor:
       def process_highlights(self, highlights):
           # Process highlights
           pass

   # main.py
   from api_client import BibleAPIClient
   from data_processor import DataProcessor

   async def main():
       client = BibleAPIClient()
       processor = DataProcessor()

       votd = await client.get_daily_verse()
       # Process data...

Use Type Hints
~~~~~~~~~~~~~

Always use type hints for better code clarity:

.. code-block:: python

   from typing import List, Optional
   from youversion.clients import AsyncClient

   async def get_highlights(
       page: int = 1
   ) -> List[dict]:
       """Get highlights for a page.

       Args:
           page: Page number

       Returns:
           List of highlight dictionaries
       """
       async with AsyncClient() as client:
           return await client.highlights(page=page)

Testing
-------

Mock API Calls in Tests
~~~~~~~~~~~~~~~~~~~~~~~

Use mocks for unit tests:

.. code-block:: python

   from unittest.mock import AsyncMock, patch
   import pytest
   from youversion.clients import AsyncClient

   @pytest.mark.asyncio
   async def test_verse_of_the_day():
       with patch('youversion.clients.AsyncClient') as mock_client:
           mock_votd = AsyncMock()
           mock_votd.usfm = ["JHN.3.16"]
           mock_votd.day = 1

           mock_client.return_value.__aenter__.return_value.verse_of_the_day.return_value = mock_votd

           async with AsyncClient() as client:
               votd = await client.verse_of_the_day()
               assert votd.usfm == ["JHN.3.16"]

Documentation
-------------

Document Your Code
~~~~~~~~~~~~~~~~~~

Add docstrings to your functions:

.. code-block:: python

   async def get_user_highlights(
       page: int = 1,
       limit: Optional[int] = None
   ) -> List[dict]:
       """Get user highlights with optional limit.

       Args:
           page: Page number to retrieve
           limit: Maximum number of highlights to return

       Returns:
           List of highlight dictionaries

       Raises:
           ValueError: If page < 1
           httpx.HTTPStatusError: If API call fails
       """
       if page < 1:
           raise ValueError("Page must be >= 1")

       async with AsyncClient() as client:
           highlights = await client.highlights(page=page)
           if limit:
               return highlights[:limit]
           return highlights

Summary
-------

Key Takeaways:

1. **Reuse client instances** - Don't create new clients for each request
2. **Use context managers** - Automatic cleanup and error handling
3. **Leverage concurrency** - Use AsyncClient for concurrent operations
4. **Handle errors properly** - Implement comprehensive error handling
5. **Cache expensive operations** - Reduce API calls with caching
6. **Secure credentials** - Never hardcode credentials
7. **Organize code** - Separate concerns and use type hints
8. **Test thoroughly** - Mock API calls in unit tests

