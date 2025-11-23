Quick Start Guide
=================

This guide will help you get started with the YouVersion Bible Client in just a few minutes.

Prerequisites
-------------

Before you begin, make sure you have:

1. Python 3.9 or higher installed
2. YouVersion account credentials
3. The package installed (see :doc:`installation`)

Setting Up Credentials
----------------------

Create a ``.env`` file in your project root:

.. code-block:: bash

   YOUVERSION_USERNAME=your_username
   YOUVERSION_PASSWORD=your_password

Or set environment variables:

.. code-block:: bash

   export YOUVERSION_USERNAME="your_username"
   export YOUVERSION_PASSWORD="your_password"

Your First Script
-----------------

Create a file named ``example.py``:

Asynchronous Example
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from youversion.clients import AsyncClient

   async def main():
       async with AsyncClient() as client:
           # Get verse of the day
           votd = await client.verse_of_the_day()
           print(f"📖 Verse of the Day (Day {votd.day})")
           print(f"Reference: {votd.usfm}")

           # Get highlights
           highlights = await client.highlights(page=1)
           print(f"\n✨ Found {len(highlights)} highlights")

           # Get notes
           notes = await client.notes(page=1)
           print(f"📝 Found {len(notes)} notes")

   if __name__ == "__main__":
       asyncio.run(main())

Synchronous Example
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from youversion.clients import SyncClient

   with SyncClient() as client:
       # Get verse of the day
       votd = client.verse_of_the_day()
       print(f"📖 Verse of the Day (Day {votd.day})")
       print(f"Reference: {votd.usfm}")

       # Get highlights
       highlights = client.highlights(page=1)
       print(f"\n✨ Found {len(highlights)} highlights")

       # Get notes
       notes = client.notes(page=1)
       print(f"📝 Found {len(notes)} notes")

Run Your Script
---------------

.. code-block:: bash

   python example.py

Common Operations
----------------

Getting Moments
~~~~~~~~~~~~~~~

Moments are user-generated content including highlights, notes, bookmarks, images, and badges.

.. code-block:: python

   from youversion.clients import SyncClient

   with SyncClient() as client:
       # Get all moments
       moments = client.moments(page=1)

       # Get specific types
       highlights = client.highlights(page=1)
       notes = client.notes(page=1)
       bookmarks = client.bookmarks(page=1)
       images = client.my_images(page=1)
       badges = client.badges(page=1)

       # Access moment properties
       for moment in moments:
           print(f"ID: {moment.id}")
           print(f"Title: {moment.moment_title}")
           print(f"Kind: {moment.kind_id}")

Searching the Bible
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from youversion.clients import SyncClient

   with SyncClient() as client:
       # Search Bible text
       results = client.search_bible("love", version_id=1)

       # Get Bible chapter
       chapter = client.get_bible_chapter("GEN.1", version_id=1)

       # Get Bible versions
       versions = client.get_bible_versions("eng", "all")

Working with Reading Plans
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from youversion.clients import SyncClient

   with SyncClient() as client:
       # Get plan progress
       progress = client.plan_progress(page=1)

       # Get plan subscriptions
       subscriptions = client.plan_subscriptions(page=1)

       # Get completed plans
       completions = client.plan_completions(page=1)

       # Search plans
       plans = client.search_plans("daily", language_tag="en")

Creating Moments
~~~~~~~~~~~~~~~~

.. code-block:: python

   from youversion.clients import SyncClient
   from youversion.models.moments import CreateMoment, ReferenceCreate
   from youversion.enums import MomentKinds, StatusEnum

   with SyncClient() as client:
       # Create a note
       moment_data = CreateMoment(
           kind=MomentKinds.NOTE,
           content="This is my study note",
           title="My Note",
           references=[
               ReferenceCreate(
                   version_id=1,
                   human="John 3:16",
                   usfm=["JHN.3.16"]
               )
           ],
           status=StatusEnum.PRIVATE,
           body="This is my study note",
           color="ff0000",
           labels=["study"],
           language_tag="en"
       )

       result = client.create_moment(moment_data)
       print(f"Created moment: {result}")

Next Steps
----------

* Read the :doc:`api` reference for all available methods
* Check out :doc:`examples` for more complex use cases
* Learn about :doc:`authentication` and security best practices
* Explore the :doc:`cli` for command-line usage

