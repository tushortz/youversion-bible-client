YouVersion Bible Client Documentation
====================================

A modern Python client for accessing YouVersion Bible data with both synchronous and asynchronous support.

.. warning::

   **Important Notice**: YouVersion has made their API private, so some functions may not work anymore. This client is maintained for educational and legacy purposes.

Features
--------

* **Dual Client Support**: Both synchronous (`Client`) and asynchronous (`AsyncClient`) implementations
* **OAuth2 Authentication**: Secure authentication using YouVersion's OAuth2 system
* **Comprehensive Data Access**: Access to verses, moments, highlights, notes, bookmarks, and more
* **Modern Python**: Built with Python 3.10+ using modern async/await patterns
* **Type Safety**: Full type hints and Pydantic models for data validation
* **CLI Support**: Command-line interface for easy access to all features
* **Poetry Integration**: Modern dependency management and script execution

Quick Start
-----------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   # Using Poetry (recommended)
   poetry install
   poetry shell

   # Or using pip
   pip install -e .

Basic Usage
~~~~~~~~~~~

Asynchronous Client
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import asyncio
   from youversion import AsyncClient

   async def main():
       async with AsyncClient() as client:
           # Get verse of the day
           votd = await client.verse_of_the_day()
           print(f"Verse: {votd.usfm}")

           # Get moments
           moments = await client.moments()
           print(f"Found {len(moments)} moments")

   asyncio.run(main())

Synchronous Client
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from youversion import Client

   with Client() as client:
       # Get verse of the day
       votd = client.verse_of_the_day()
       print(f"Verse: {votd.usfm}")

       # Get highlights
       highlights = client.highlights()
       print(f"Found {len(highlights)} highlights")

Command Line Interface
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Get verse of the day
   poetry run youversion votd

   # Get moments with JSON output
   poetry run youversion moments --json

   # Get highlights with limit
   poetry run youversion highlights --limit 5

   # Discover API endpoints
   poetry run youversion discover-endpoints

Configuration
-------------

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Create a `.env` file in your project root:

.. code-block:: bash

   YOUVERSION_USERNAME=your_username
   YOUVERSION_PASSWORD=your_password

API Reference
-------------

.. toctree::
   :maxdepth: 2
   :caption: Complete API Reference:

   api

Clients
~~~~~~~

.. toctree::
   :maxdepth: 2
   :caption: Client Documentation:

   clients

Models
~~~~~~

.. toctree::
   :maxdepth: 2
   :caption: Data Models:

   models

CLI Reference
~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 2
   :caption: Command Line Interface:

   cli

Examples
--------

.. toctree::
   :maxdepth: 2
   :caption: Usage Examples:

   examples

Development
-----------

Testing
~~~~~~~

.. code-block:: bash

   # Run all tests
   poetry run pytest

   # Run tests with coverage
   poetry run pytest --cov=youversion

   # Run specific test file
   poetry run pytest tests/test_cli.py -v

Code Quality
~~~~~~~~~~~~

.. code-block:: bash

   # Format code
   poetry run black .

   # Lint code
   poetry run ruff check . --fix

   # Type checking
   poetry run mypy youversion/

Project Structure
-----------------

.. code-block::

   youversion-bible-client/
   ├── youversion/                 # Main package
   │   ├── clients/               # Client implementations
   │   ├── core/                  # Core functionality
   │   ├── models/                # Data models
   │   ├── cli.py                 # Command-line interface
   │   └── __init__.py
   ├── tests/                     # Test suite
   ├── examples/                  # Usage examples
   ├── documentation/             # Sphinx documentation
   ├── pyproject.toml             # Project configuration
   └── README.md                  # Project overview

Changelog
---------

Version 0.3.0
~~~~~~~~~~~~~

* Fixed RuntimeWarnings in test suite
* Improved async mocking in tests
* Updated dependencies

Version 0.2.0
~~~~~~~~~~~~~

* Added dual client support (sync/async)
* Implemented OAuth2 authentication
* Added comprehensive CLI
* Restructured codebase with SOLID principles
* Added URL discovery functionality

Version 0.1.x
~~~~~~~~~~~~~

* Initial release
* Basic YouVersion API access
* Pydantic data models

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
