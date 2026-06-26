Usage Examples
==============

See the ``examples/`` directory for runnable scripts. This page covers the most common patterns.

Quick example
-------------

.. code-block:: python

   import asyncio
   from youversion.clients import AsyncClient

   async def main():
       async with AsyncClient() as client:
           votd = await client.verse_of_the_day()
           print(votd.usfm)

           chapter = await client.get_bible_chapter("GEN.1", version_id=1)
           print(chapter["reference"]["human"])

   asyncio.run(main())

Moments
-------

.. code-block:: python

   from youversion.clients import SyncClient

   with SyncClient() as client:
       for fn in (client.highlights, client.notes, client.bookmarks, client.badges):
           items = fn(page=1)
           print(fn.__name__, len(items))

Bible and audio
---------------

.. code-block:: python

   with SyncClient() as client:
       results = client.search_bible("love", version_id=1)
       chapter = client.get_bible_chapter("GEN.1", version_id=1)
       audio = client.get_audio_chapter("GEN.1", version_id=1)

Friends
-------

Friend suggestions require ISO 639-1 ``language_tag="en"``:

.. code-block:: python

   with SyncClient() as client:
       suggestions = client.get_friend_suggestions(page=1, language_tag="en")

Concurrent requests
-------------------

.. code-block:: python

   import asyncio
   from youversion.clients import AsyncClient

   async def main():
       async with AsyncClient() as client:
           votd, highlights, notes = await asyncio.gather(
               client.verse_of_the_day(),
               client.highlights(page=1),
               client.notes(page=1),
           )
           print(len(highlights), len(notes))

   asyncio.run(main())

Integration tests
-----------------

Live API tests (requires ``.env`` credentials):

.. code-block:: bash

   pytest tests/test_api_integration.py -m integration

Captured responses are written to ``results/integration/<timestamp>/``.

Further reading
---------------

* :doc:`quickstart`
* :doc:`api`
* :doc:`cli`
* `DOCS.md <https://github.com/tushortz/youversion-bible-client/blob/main/DOCS.md>`_ in the repository root
