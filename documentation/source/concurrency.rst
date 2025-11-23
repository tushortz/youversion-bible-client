Concurrency and Performance
============================

The YouVersion Bible Client supports concurrent operations through the AsyncClient, enabling efficient parallel API calls.

Why Use Concurrency?
--------------------

* **Faster Execution**: Multiple requests happen simultaneously
* **Better Resource Usage**: Efficient use of network and CPU
* **Improved User Experience**: Reduced waiting time

Basic Concurrency
-----------------

Using asyncio.gather()
~~~~~~~~~~~~~~~~~~~~~~

Execute multiple API calls concurrently:

.. code-block:: python

   import asyncio
   from youversion.clients import AsyncClient

   async def get_all_data():
       async with AsyncClient() as client:
           # All three calls happen concurrently
           votd, highlights, notes = await asyncio.gather(
               client.verse_of_the_day(),
               client.highlights(page=1),
               client.notes(page=1)
           )
           return votd, highlights, notes

   results = asyncio.run(get_all_data())

Concurrent Pagination
----------------------

Fetch multiple pages concurrently:

.. code-block:: python

   import asyncio
   from youversion.clients import AsyncClient

   async def get_multiple_pages(max_pages=5):
       async with AsyncClient() as client:
           # Fetch pages 1-5 concurrently
           tasks = [
               client.highlights(page=i)
               for i in range(1, max_pages + 1)
           ]
           results = await asyncio.gather(*tasks, return_exceptions=True)

           # Flatten results, handling errors
           all_highlights = []
           for result in results:
               if isinstance(result, list):
                   all_highlights.extend(result)
               elif isinstance(result, Exception):
                   print(f"Error: {result}")

           return all_highlights

   highlights = asyncio.run(get_multiple_pages())

Error Handling in Concurrent Operations
----------------------------------------

Handle errors in concurrent operations:

.. code-block:: python

   import asyncio
   import httpx
   from youversion.clients import AsyncClient

   async def safe_concurrent_calls():
       async with AsyncClient() as client:
           results = await asyncio.gather(
               client.verse_of_the_day(),
               client.highlights(page=1),
               client.notes(page=1),
               return_exceptions=True  # Don't fail all if one fails
           )

           votd, highlights, notes = results

           # Check each result
           if isinstance(votd, Exception):
               print(f"VOTD error: {votd}")
               votd = None

           if isinstance(highlights, Exception):
               print(f"Highlights error: {highlights}")
               highlights = []

           if isinstance(notes, Exception):
               print(f"Notes error: {notes}")
               notes = []

           return votd, highlights, notes

   results = asyncio.run(safe_concurrent_calls())

Rate Limiting
-------------

Respect API Rate Limits
~~~~~~~~~~~~~~~~~~~~~~~

Implement rate limiting for concurrent requests:

.. code-block:: python

   import asyncio
   from asyncio import Semaphore
   from youversion.clients import AsyncClient

   async def rate_limited_requests(semaphore, requests):
       async with semaphore:
           async with AsyncClient() as client:
               return await client.verse_of_the_day()

   async def batch_with_rate_limit(max_concurrent=5):
       semaphore = Semaphore(max_concurrent)
       tasks = [
           rate_limited_requests(semaphore, i)
           for i in range(20)  # 20 requests, max 5 concurrent
       ]
       results = await asyncio.gather(*tasks)
       return results

   results = asyncio.run(batch_with_rate_limit())

Batching Operations
------------------

Process data in batches:

.. code-block:: python

   import asyncio
   from youversion.clients import AsyncClient

   async def process_in_batches(items, batch_size=10):
       async with AsyncClient() as client:
           for i in range(0, len(items), batch_size):
               batch = items[i:i + batch_size]
               # Process batch concurrently
               tasks = [process_item(item) for item in batch]
               await asyncio.gather(*tasks)

   async def process_item(item):
       # Process individual item
       pass

Performance Tips
----------------

1. **Reuse Client**: Create one client and reuse it
2. **Batch Requests**: Group related requests together
3. **Use Semaphores**: Limit concurrent requests
4. **Handle Errors**: Use return_exceptions in gather()
5. **Cache Results**: Cache expensive operations

Example: Complete Concurrent Workflow
---------------------------------------

.. code-block:: python

   import asyncio
   from youversion.clients import AsyncClient
   from asyncio import Semaphore

   async def comprehensive_data_fetch():
       semaphore = Semaphore(5)  # Max 5 concurrent requests

       async def fetch_with_limit(coro):
           async with semaphore:
               return await coro

       async with AsyncClient() as client:
           # Fetch all data concurrently with rate limiting
           results = await asyncio.gather(
               fetch_with_limit(client.verse_of_the_day()),
               fetch_with_limit(client.highlights(page=1)),
               fetch_with_limit(client.notes(page=1)),
               fetch_with_limit(client.bookmarks(page=1)),
               fetch_with_limit(client.get_bible_versions("eng", "all")),
               return_exceptions=True
           )

           # Process results
           data = {}
           keys = ['votd', 'highlights', 'notes', 'bookmarks', 'versions']

           for key, result in zip(keys, results):
               if isinstance(result, Exception):
                   print(f"Error fetching {key}: {result}")
                   data[key] = None
               else:
                   data[key] = result

           return data

   data = asyncio.run(comprehensive_data_fetch())

