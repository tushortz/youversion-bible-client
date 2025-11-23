Error Handling
==============

Proper error handling is essential for building robust applications with the YouVersion Bible Client.

Exception Types
---------------

The client raises several types of exceptions:

ValueError
~~~~~~~~~~

Raised for configuration and validation errors:

.. code-block:: python

   from youversion.clients import AsyncClient

   try:
       # Missing credentials
       client = AsyncClient()  # No credentials provided
   except ValueError as e:
       print(f"Configuration error: {e}")

httpx.HTTPStatusError
~~~~~~~~~~~~~~~~~~~~~

Raised for HTTP errors from the API:

.. code-block:: python

   import httpx
   from youversion.clients import AsyncClient

   async def handle_http_errors():
       try:
           async with AsyncClient() as client:
               result = await client.verse_of_the_day()
       except httpx.HTTPStatusError as e:
           if e.response.status_code == 401:
               print("Authentication failed")
           elif e.response.status_code == 404:
               print("Resource not found")
           elif e.response.status_code == 429:
               print("Rate limit exceeded")
           else:
               print(f"HTTP error: {e.response.status_code}")

httpx.RequestError
~~~~~~~~~~~~~~~~~~

Raised for network and connection errors:

.. code-block:: python

   import httpx
   from youversion.clients import AsyncClient

   async def handle_network_errors():
       try:
           async with AsyncClient() as client:
               result = await client.verse_of_the_day()
       except httpx.RequestError as e:
           print(f"Network error: {e}")
           print("Check your internet connection")

Comprehensive Error Handling
-----------------------------

Example with all error types:

.. code-block:: python

   import asyncio
   import httpx
   from youversion.clients import AsyncClient

   async def robust_api_call():
       try:
           async with AsyncClient() as client:
               votd = await client.verse_of_the_day()
               return votd
       except ValueError as e:
           # Configuration errors
           print(f"❌ Configuration error: {e}")
           print("Please check your credentials")
           return None
       except httpx.HTTPStatusError as e:
           # HTTP errors
           status = e.response.status_code
           if status == 401:
               print("❌ Authentication failed")
               print("Please check your username and password")
           elif status == 403:
               print("❌ Access forbidden")
               print("Your account may not have permission")
           elif status == 404:
               print("❌ Resource not found")
           elif status == 429:
               print("❌ Rate limit exceeded")
               print("Please wait before making more requests")
           else:
               print(f"❌ HTTP error {status}: {e}")
           return None
       except httpx.RequestError as e:
           # Network errors
           print(f"❌ Network error: {e}")
           print("Please check your internet connection")
           return None
       except Exception as e:
           # Unexpected errors
           print(f"❌ Unexpected error: {e}")
           return None

   result = asyncio.run(robust_api_call())
   if result:
       print(f"✅ Success: {result.usfm}")

Retry Logic
-----------

Implement retry logic for transient errors:

.. code-block:: python

   import asyncio
   import httpx
   from youversion.clients import AsyncClient

   async def retry_api_call(max_retries=3, delay=1):
       for attempt in range(max_retries):
           try:
               async with AsyncClient() as client:
                   return await client.verse_of_the_day()
           except httpx.RequestError as e:
               if attempt < max_retries - 1:
                   print(f"Retry {attempt + 1}/{max_retries}...")
                   await asyncio.sleep(delay)
                   continue
               raise
           except httpx.HTTPStatusError as e:
               # Don't retry on 4xx errors (except 429)
               if e.response.status_code == 429:
                   if attempt < max_retries - 1:
                       wait_time = delay * (attempt + 1)
                       print(f"Rate limited. Waiting {wait_time}s...")
                       await asyncio.sleep(wait_time)
                       continue
               raise

   result = asyncio.run(retry_api_call())

Rate Limiting
-------------

Handle rate limiting gracefully:

.. code-block:: python

   import asyncio
   import httpx
   from youversion.clients import AsyncClient

   async def rate_limited_call():
       try:
           async with AsyncClient() as client:
               return await client.verse_of_the_day()
       except httpx.HTTPStatusError as e:
           if e.response.status_code == 429:
               # Extract retry-after header if available
               retry_after = e.response.headers.get("Retry-After", "60")
               print(f"Rate limited. Retry after {retry_after} seconds")
               await asyncio.sleep(int(retry_after))
               # Retry the call
               async with AsyncClient() as client:
                   return await client.verse_of_the_day()
           raise

   result = asyncio.run(rate_limited_call())

Error Logging
-------------

Log errors for debugging:

.. code-block:: python

   import logging
   import httpx
   from youversion.clients import AsyncClient

   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)

   async def logged_api_call():
       try:
           async with AsyncClient() as client:
               votd = await client.verse_of_the_day()
               logger.info(f"Successfully retrieved VOTD: {votd.usfm}")
               return votd
       except ValueError as e:
           logger.error(f"Configuration error: {e}", exc_info=True)
           return None
       except httpx.HTTPStatusError as e:
           logger.error(
               f"HTTP error {e.response.status_code}: {e}",
               exc_info=True
           )
           return None
       except Exception as e:
           logger.exception(f"Unexpected error: {e}")
           return None

   import asyncio
   result = asyncio.run(logged_api_call())

Custom Error Classes
--------------------

Create custom error handlers:

.. code-block:: python

   class YouVersionError(Exception):
       """Base exception for YouVersion client errors."""
       pass

   class AuthenticationError(YouVersionError):
       """Raised when authentication fails."""
       pass

   class APIError(YouVersionError):
       """Raised when API returns an error."""
       def __init__(self, status_code, message):
           self.status_code = status_code
           self.message = message
           super().__init__(f"API error {status_code}: {message}")

   async def custom_error_handler():
       try:
           async with AsyncClient() as client:
               return await client.verse_of_the_day()
       except ValueError as e:
           raise AuthenticationError(f"Authentication failed: {e}")
       except httpx.HTTPStatusError as e:
           raise APIError(e.response.status_code, str(e))

   import asyncio
   try:
       result = asyncio.run(custom_error_handler())
   except AuthenticationError as e:
       print(f"Auth error: {e}")
   except APIError as e:
       print(f"API error: {e.status_code} - {e.message}")

Error Recovery Strategies
------------------------

Graceful Degradation
~~~~~~~~~~~~~~~~~~~~

Continue operation even if some calls fail:

.. code-block:: python

   import asyncio
   from youversion.clients import AsyncClient

   async def graceful_degradation():
       results = {}
       async with AsyncClient() as client:
           # Try to get VOTD
           try:
               results['votd'] = await client.verse_of_the_day()
           except Exception as e:
               results['votd'] = None
               print(f"Could not get VOTD: {e}")

           # Try to get highlights
           try:
               results['highlights'] = await client.highlights()
           except Exception as e:
               results['highlights'] = []
               print(f"Could not get highlights: {e}")

           # Try to get notes
           try:
               results['notes'] = await client.notes()
           except Exception as e:
               results['notes'] = []
               print(f"Could not get notes: {e}")

       return results

   results = asyncio.run(graceful_degradation())
   print(f"Successfully retrieved: {[k for k, v in results.items() if v]}")

Fallback Values
~~~~~~~~~~~~~~~

Provide fallback values when API calls fail:

.. code-block:: python

   import asyncio
   from youversion.clients import AsyncClient

   async def with_fallback():
       async with AsyncClient() as client:
           try:
               votd = await client.verse_of_the_day()
           except Exception:
               # Fallback to default
               votd = type('Votd', (), {
                   'day': 1,
                   'usfm': ['JHN.3.16'],
                   'image_id': None
               })()
           return votd

   result = asyncio.run(with_fallback())

Best Practices
--------------

1. **Always use try-except blocks** around API calls
2. **Handle specific exceptions** rather than catching all
3. **Provide meaningful error messages** to users
4. **Log errors** for debugging
5. **Implement retry logic** for transient errors
6. **Respect rate limits** and implement backoff
7. **Use context managers** for automatic cleanup
8. **Validate input** before making API calls

