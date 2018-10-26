Command Line Interface
=======================

The YouVersion Bible Client includes a comprehensive command-line interface for easy access to all features.

Installation
------------

The CLI is automatically available when you install the package:

.. code-block:: bash

   # Using Poetry (recommended)
   poetry install
   poetry run youversion --help

   # Or using pip
   pip install -e .
   youversion --help

Basic Usage
-----------

The CLI provides several commands for accessing different types of data:

.. code-block:: bash

   # Get verse of the day
   poetry run youversion votd

   # Get moments
   poetry run youversion moments

   # Get highlights
   poetry run youversion highlights

   # Get notes
   poetry run youversion notes

   # Get bookmarks
   poetry run youversion bookmarks

   # Get images
   poetry run youversion images

   # Get plan progress
   poetry run youversion plan-progress

   # Get plan subscriptions
   poetry run youversion plan-subscriptions

   # Convert notes to markdown
   poetry run youversion convert-notes

   # Discover API endpoints
   poetry run youversion discover-endpoints

Global Options
--------------

All commands support these global options:

.. option:: --json

   Output results in JSON format instead of human-readable format.

.. option:: --limit LIMIT

   Limit the number of items displayed (default: 10).

Command Reference
-----------------

votd
~~~~

Get the verse of the day.

.. code-block:: bash

   poetry run youversion votd [--day DAY] [--json]

Options:
   ``--day DAY``: Specific day number (1-365)
   ``--json``: Output as JSON

Examples:
   :code:`poetry run youversion votd`

   :code:`poetry run youversion votd --day 100`

   :code:`poetry run youversion votd --json`

moments
~~~~~~~

Get user moments.

.. code-block:: bash

   poetry run youversion moments [--page PAGE] [--limit LIMIT] [--json]

Options:
   ``--page PAGE``: Page number (default: 1)
   ``--limit LIMIT``: Number of items to display (default: 10)
   :option:`--json`: Output as JSON

Examples:
   :code:`poetry run youversion moments`
   :code:`poetry run youversion moments --page 2`
   :code:`poetry run youversion moments --limit 5 --json`

highlights
~~~~~~~~~~

Get user highlights.

.. code-block:: bash

   poetry run youversion highlights [--page PAGE] [--limit LIMIT] [--json]

Options:
   ``--page PAGE``: Page number (default: 1)
   ``--limit LIMIT``: Number of items to display (default: 10)
   :option:`--json`: Output as JSON

Examples:
   :code:`poetry run youversion highlights`
   :code:`poetry run youversion highlights --page 2 --limit 5`

notes
~~~~~

Get user notes.

.. code-block:: bash

   poetry run youversion notes [--page PAGE] [--limit LIMIT] [--json]

Options:
   ``--page PAGE``: Page number (default: 1)
   ``--limit LIMIT``: Number of items to display (default: 10)
   :option:`--json`: Output as JSON

Examples:
   :code:`poetry run youversion notes`
   :code:`poetry run youversion notes --json`

bookmarks
~~~~~~~~~

Get user bookmarks.

.. code-block:: bash

   poetry run youversion bookmarks [--page PAGE] [--limit LIMIT] [--json]

Options:
   ``--page PAGE``: Page number (default: 1)
   ``--limit LIMIT``: Number of items to display (default: 10)
   :option:`--json`: Output as JSON

Examples:
   :code:`poetry run youversion bookmarks`
   :code:`poetry run youversion bookmarks --page 1`

images
~~~~~~

Get user images.

.. code-block:: bash

   poetry run youversion images [--page PAGE] [--limit LIMIT] [--json]

Options:
   ``--page PAGE``: Page number (default: 1)
   ``--limit LIMIT``: Number of items to display (default: 10)
   :option:`--json`: Output as JSON

Examples:
   :code:`poetry run youversion images`
   :code:`poetry run youversion images --json`

plan-progress
~~~~~~~~~~~~~

Get reading plan progress.

.. code-block:: bash

   poetry run youversion plan-progress [--page PAGE] [--limit LIMIT] [--json]

Options:
   ``--page PAGE``: Page number (default: 1)
   ``--limit LIMIT``: Number of items to display (default: 10)
   :option:`--json`: Output as JSON

Examples:
   :code:`poetry run youversion plan-progress`
   :code:`poetry run youversion plan-progress --limit 5`

plan-subscriptions
~~~~~~~~~~~~~~~~~~

Get reading plan subscriptions.

.. code-block:: bash

   poetry run youversion plan-subscriptions [--page PAGE] [--limit LIMIT] [--json]

Options:
   ``--page PAGE``: Page number (default: 1)
   ``--limit LIMIT``: Number of items to display (default: 10)
   :option:`--json`: Output as JSON

Examples:
   :code:`poetry run youversion plan-subscriptions`
   :code:`poetry run youversion plan-subscriptions --json`

convert-notes
~~~~~~~~~~~~~

Convert notes to markdown format.

.. code-block:: bash

   poetry run youversion convert-notes [--json]

Options:
   :option:`--json`: Output as JSON

Examples:
   :code:`poetry run youversion convert-notes`
   :code:`poetry run youversion convert-notes --json`

discover-endpoints
~~~~~~~~~~~~~~~~~~

Discover available API endpoints and build ID.

.. code-block:: bash

   poetry run youversion discover-endpoints [--username USERNAME]

Options:
   ``--username USERNAME``: Specify username for endpoint discovery

Examples:
   :code:`poetry run youversion discover-endpoints`
   :code:`poetry run youversion discover-endpoints --username myuser`

Configuration
-------------

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

The CLI reads credentials from environment variables:

.. code-block:: bash

   export YOUVERSION_USERNAME=your_username
   export YOUVERSION_PASSWORD=your_password

Or create a ``.env`` file in your project root:

.. code-block:: bash

   YOUVERSION_USERNAME=your_username
   YOUVERSION_PASSWORD=your_password

Poetry Scripts
--------------

The CLI commands are also available as Poetry scripts for easier access:

.. code-block:: bash

   # Verse of the day
   poetry run votd
   poetry run votd --day 100

   # Moments
   poetry run moments
   poetry run moments --page 2

   # Highlights
   poetry run highlights
   poetry run highlights --limit 5

   # Notes
   poetry run notes
   poetry run notes --json

   # Bookmarks
   poetry run bookmarks
   poetry run bookmarks --page 1

   # Images
   poetry run images
   poetry run images --json

   # Plan progress
   poetry run plan-progress
   poetry run plan-progress --limit 5

   # Plan subscriptions
   poetry run plan-subscriptions
   poetry run plan-subscriptions --json

   # Convert notes
   poetry run convert-notes
   poetry run convert-notes --json

   # Discover endpoints
   poetry run discover-endpoints
   poetry run discover-endpoints --username myuser

Output Formats
--------------

Human-Readable Format
~~~~~~~~~~~~~~~~~~~~~

By default, the CLI outputs data in a human-readable format:

.. code-block:: text

   📖 Verse of the Day
   Day: 1
   USFM: JHN.3.16
   Image ID: None

   📋 Moments (Page 1)
   Found 5 moments
   --------------------------------------------------
     1. HIGHLIGHT
        Title: John 3:16
        Time: 2 hours ago
        Owned by me: True

JSON Format
~~~~~~~~~~~

Use the ``--json`` flag for machine-readable output:

.. code-block:: json

   {
     "day": 1,
     "usfm": ["JHN.3.16"],
     "image_id": null
   }

Error Handling
--------------

The CLI provides clear error messages for common issues:

.. code-block:: text

   ❌ Error: Missing credentials
   Please set YOUVERSION_USERNAME and YOUVERSION_PASSWORD environment variables
   Or create a .env file with your credentials:

   YOUVERSION_USERNAME=your_username
   YOUVERSION_PASSWORD=your_password

Exit Codes
----------

* ``0``: Success
* ``1``: Error (authentication, API, or other errors)

Examples
--------

Basic Usage
~~~~~~~~~~~

.. code-block:: bash

   # Get today's verse
   poetry run youversion votd

   # Get first 5 highlights
   poetry run youversion highlights --limit 5

   # Get moments from page 2 as JSON
   poetry run youversion moments --page 2 --json

Advanced Usage
~~~~~~~~~~~~~~

.. code-block:: bash

   # Get verse for day 100
   poetry run youversion votd --day 100

   # Get all notes as JSON for processing
   poetry run youversion notes --json > notes.json

   # Discover API endpoints
   poetry run youversion discover-endpoints --username myuser

   # Convert notes to markdown
   poetry run youversion convert-notes --json > notes.md
