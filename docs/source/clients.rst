Client Documentation
====================

The YouVersion Bible Client provides two main client implementations: synchronous and asynchronous.

AsyncClient
-----------

The ``AsyncClient`` is the primary client for modern Python applications using async/await patterns.

.. class:: AsyncClient(username=None, password=None)

   Asynchronous client for YouVersion Bible API access.

   :param username: YouVersion username (optional if set in environment)
   :param password: YouVersion password (optional if set in environment)

   .. method:: async __aenter__()

      Async context manager entry. Automatically authenticates the client.

   .. method:: async __aexit__(exc_type, exc_val, exc_tb)

      Async context manager exit. Closes the HTTP client.

   .. method:: async moments(page=1)

      Get user moments.

      :param page: Page number to retrieve
      :return: List of Moment objects
      :rtype: List[Moment]

   .. method:: async highlights(page=1)

      Get user highlights.

      :param page: Page number to retrieve
      :return: List of Highlight objects
      :rtype: List[Highlight]

   .. method:: async verse_of_the_day(day=None)

      Get verse of the day.

      :param day: Specific day number (1-365), defaults to current day
      :return: Votd object
      :rtype: Votd

   .. method:: async notes(page=1)

      Get user notes.

      :param page: Page number to retrieve
      :return: List of Note objects
      :rtype: List[Note]

   .. method:: async bookmarks(page=1)

      Get user bookmarks.

      :param page: Page number to retrieve
      :return: List of Moment objects
      :rtype: List[Moment]

   .. method:: async my_images(page=1)

      Get user images.

      :param page: Page number to retrieve
      :return: List of Image objects
      :rtype: List[Image]

   .. method:: async plan_progress(page=1)

      Get plan progress.

      :param page: Page number to retrieve
      :return: List of PlanSegmentCompletion objects
      :rtype: List[PlanSegmentCompletion]

   .. method:: async plan_subscriptions(page=1)

      Get plan subscriptions.

      :param page: Page number to retrieve
      :return: List of PlanSubscription objects
      :rtype: List[PlanSubscription]

   .. method:: async convert_note_to_md()

      Convert notes to markdown format.

      :return: List of converted note data
      :rtype: List[Dict[str, Any]]

   .. method:: async close()

      Close the HTTP client.

Usage Example
~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from youversion import AsyncClient

   async def main():
       async with AsyncClient() as client:
           # Get verse of the day
           votd = await client.verse_of_the_day()
           print(f"Today's verse: {votd.usfm}")

           # Get highlights
           highlights = await client.highlights()
           for highlight in highlights[:5]:  # First 5 highlights
               print(f"Highlight: {highlight.moment_title}")

   asyncio.run(main())

SyncClient
----------

The ``SyncClient`` provides a synchronous wrapper around the AsyncClient for applications that prefer synchronous programming patterns.

.. class:: SyncClient(username=None, password=None)

   Synchronous client for YouVersion Bible API access.

   :param username: YouVersion username (optional if set in environment)
   :param password: YouVersion password (optional if set in environment)

   .. method:: __enter__()

      Context manager entry. Automatically authenticates the client.

   .. method:: __exit__(exc_type, exc_val, exc_tb)

      Context manager exit. Closes the HTTP client.

   .. method:: moments(page=1)

      Get user moments (synchronous).

      :param page: Page number to retrieve
      :return: List of Moment objects
      :rtype: List[Moment]

   .. method:: highlights(page=1)

      Get user highlights (synchronous).

      :param page: Page number to retrieve
      :return: List of Highlight objects
      :rtype: List[Highlight]

   .. method:: verse_of_the_day(day=None)

      Get verse of the day (synchronous).

      :param day: Specific day number (1-365), defaults to current day
      :return: Votd object
      :rtype: Votd

   .. method:: notes(page=1)

      Get user notes (synchronous).

      :param page: Page number to retrieve
      :return: List of Note objects
      :rtype: List[Note]

   .. method:: bookmarks(page=1)

      Get user bookmarks (synchronous).

      :param page: Page number to retrieve
      :return: List of Moment objects
      :rtype: List[Moment]

   .. method:: my_images(page=1)

      Get user images (synchronous).

      :param page: Page number to retrieve
      :return: List of Image objects
      :rtype: List[Image]

   .. method:: plan_progress(page=1)

      Get plan progress (synchronous).

      :param page: Page number to retrieve
      :return: List of PlanSegmentCompletion objects
      :rtype: List[PlanSegmentCompletion]

   .. method:: plan_subscriptions(page=1)

      Get plan subscriptions (synchronous).

      :param page: Page number to retrieve
      :return: List of PlanSubscription objects
      :rtype: List[PlanSubscription]

   .. method:: convert_note_to_md()

      Convert notes to markdown format (synchronous).

      :return: List of converted note data
      :rtype: List[Dict[str, Any]]

   .. method:: close()

      Manually close the HTTP client.

Usage Example
~~~~~~~~~~~~~

.. code-block:: python

   from youversion import Client

   with Client() as client:
       # Get verse of the day
       votd = client.verse_of_the_day()
       print(f"Today's verse: {votd.usfm}")

       # Get highlights
       highlights = client.highlights()
       for highlight in highlights[:5]:  # First 5 highlights
           print(f"Highlight: {highlight.moment_title}")

Authentication
--------------

Both clients support OAuth2 authentication using YouVersion's authentication system. Credentials can be provided in several ways:

1. **Environment Variables**: Set ``YOUVERSION_USERNAME`` and ``YOUVERSION_PASSWORD``
2. **Constructor Parameters**: Pass credentials directly to the client
3. **Environment File**: Create a ``.env`` file in your project root

.. code-block:: bash

   # .env file
   YOUVERSION_USERNAME=your_username
   YOUVERSION_PASSWORD=your_password

Error Handling
--------------

Both clients raise appropriate exceptions for various error conditions:

* ``ValueError``: Missing or invalid credentials
* ``httpx.HTTPStatusError``: HTTP errors from the API
* ``RuntimeError``: Invalid usage patterns (e.g., using SyncClient in async context)

.. code-block:: python

   from youversion import AsyncClient
   import httpx

   async def main():
       try:
           async with AsyncClient() as client:
               votd = await client.verse_of_the_day()
               print(f"Success: {votd.usfm}")
       except ValueError as e:
           print(f"Authentication error: {e}")
       except httpx.HTTPStatusError as e:
           print(f"API error: {e}")

   asyncio.run(main())
