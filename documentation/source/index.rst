YouVersion Bible Client Documentation
====================================

Welcome to the comprehensive documentation for the YouVersion Bible Client library. This library provides both synchronous and asynchronous Python interfaces to interact with all YouVersion API endpoints.

.. warning::

   **Important Notice**: YouVersion has made their API private, so some functions may not work anymore. This client is maintained for educational and legacy purposes. Please use responsibly.

Overview
--------

The YouVersion Bible Client is a modern Python library that provides:

* **Dual Client Support**: Both synchronous (`SyncClient`) and asynchronous (`AsyncClient`) implementations
* **OAuth2 Authentication**: Secure authentication using YouVersion's OAuth2 system
* **Comprehensive API Coverage**: Access to 55+ API endpoints including:
  - Bible content and versions
  - Audio Bible
  - Moments (highlights, notes, bookmarks, images, badges)
  - Reading plans
  - Events
  - Videos
  - Friendships
  - Themes
  - And much more
* **Dynamic Pydantic Models**: Automatically generated models from API responses
* **Type Safety**: Full type hints throughout the codebase
* **CLI Support**: Command-line interface for easy access to all features
* **Python 3.9+**: Compatible with Python 3.9 and above

Quick Start
-----------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   # Using pip
   pip install youversion-bible-client

   # Using Poetry
   poetry add youversion-bible-client

Basic Usage
~~~~~~~~~~~

Asynchronous Client
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import asyncio
   from youversion.clients import AsyncClient

   async def main():
       async with AsyncClient() as client:
           # Get verse of the day
           votd = await client.verse_of_the_day()
           print(f"Verse: {votd.usfm}")

           # Get moments
           moments = await client.moments(page=1)
           print(f"Found {len(moments)} moments")

   asyncio.run(main())

Synchronous Client
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from youversion.clients import SyncClient

   with SyncClient() as client:
       # Get verse of the day
       votd = client.verse_of_the_day()
       print(f"Verse: {votd.usfm}")

       # Get highlights
       highlights = client.highlights(page=1)
       print(f"Found {len(highlights)} highlights")

Configuration
-------------

The client requires YouVersion API credentials. You can provide them in several ways:

1. **Environment Variables** (Recommended for production):

.. code-block:: bash

   export YOUVERSION_USERNAME="your_username"
   export YOUVERSION_PASSWORD="your_password"

2. **`.env` File** (Recommended for development):

.. code-block:: bash

   # Create .env file in project root
   YOUVERSION_USERNAME=your_username
   YOUVERSION_PASSWORD=your_password

3. **Constructor Arguments**:

.. code-block:: python

   client = AsyncClient(username="user", password="pass")

Documentation Contents
----------------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started:

   installation
   quickstart
   configuration

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   api
   clients
   models

.. toctree::
   :maxdepth: 2
   :caption: Guides:

   examples
   cli
   authentication
   error_handling
   best_practices

.. toctree::
   :maxdepth: 2
   :caption: Advanced Topics:

   dynamic_models
   concurrency
   testing
   deployment

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
