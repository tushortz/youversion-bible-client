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

badges
~~~~~~

Get user badges.

.. code-block:: bash

   poetry run youversion badges [--page PAGE] [--limit LIMIT] [--json]

Options:
   ``--page PAGE``: Page number (default: 1)
   ``--limit LIMIT``: Number of items to display (default: 10)
   :option:`--json`: Output as JSON

Examples:
   :code:`poetry run youversion badges`
   :code:`poetry run youversion badges --page 1`

create-moment
~~~~~~~~~~~~~

Create a new moment (note, highlight, etc.).

.. code-block:: bash

   poetry run youversion create-moment --kind KIND --content CONTENT --title TITLE [options]

Options:
   ``--kind KIND``: Moment kind (note, highlight, bookmark, etc.)
   ``--content CONTENT``: Moment content (required)
   ``--title TITLE``: Moment title (required)
   ``--status STATUS``: Status (private, draft, public)
   ``--body BODY``: Body text
   ``--color COLOR``: Highlight color (hex code)
   ``--language-tag TAG``: Language tag (e.g., 'en')
   ``--references REFS``: Bible references
   ``--labels LABELS``: Labels/tags
   :option:`--json`: Output as JSON

Examples:
   :code:`poetry run youversion create-moment --kind note --content "My note" --title "Title"`
   :code:`poetry run youversion create-moment --kind highlight --content "Text" --title "Title" --color ff0000`

get-bible-configuration
~~~~~~~~~~~~~~~~~~~~~~~~

Get Bible configuration.

.. code-block:: bash

   poetry run youversion get-bible-configuration [--json]

Options:
   :option:`--json`: Output as JSON

Examples:
   :code:`poetry run youversion get-bible-configuration`

get-bible-versions
~~~~~~~~~~~~~~~~~~

Get Bible versions for a language.

.. code-block:: bash

   poetry run youversion get-bible-versions [--language-tag TAG] [--json]

Options:
   ``--language-tag TAG``: Language tag (default: 'eng')
   :option:`--json`: Output as JSON

Examples:
   :code:`poetry run youversion get-bible-versions`
   :code:`poetry run youversion get-bible-versions --language-tag spa`

get-bible-version
~~~~~~~~~~~~~~~~~

Get specific Bible version details.

.. code-block:: bash

   poetry run youversion get-bible-version VERSION_ID [--json]

Arguments:
   ``VERSION_ID``: Version ID (required)

Options:
   :option:`--json`: Output as JSON

Examples:
   :code:`poetry run youversion get-bible-version 1`

get-bible-chapter
~~~~~~~~~~~~~~~~~

Get Bible chapter content.

.. code-block:: bash

   poetry run youversion get-bible-chapter REFERENCE [--version-id ID] [--json]

Arguments:
   ``REFERENCE``: USFM reference (e.g., 'GEN.1', 'JHN.3.16') (required)

Options:
   ``--version-id ID``: Version ID (default: 1)
   :option:`--json`: Output as JSON

Examples:
   :code:`poetry run youversion get-bible-chapter GEN.1`
   :code:`poetry run youversion get-bible-chapter JHN.3.16 --version-id 1`

search-bible
~~~~~~~~~~~~

Search Bible text.

.. code-block:: bash

   poetry run youversion search-bible QUERY [--version-id ID] [--book BOOK] [--json]

Arguments:
   ``QUERY``: Search query (required)

Options:
   ``--version-id ID``: Version ID to search in
   ``--book BOOK``: Book filter (e.g., 'JHN', 'GEN')
   :option:`--json`: Output as JSON

Examples:
   :code:`poetry run youversion search-bible "love"`
   :code:`poetry run youversion search-bible "love" --version-id 1`
   :code:`poetry run youversion search-bible "love" --book JHN`

get-themes
~~~~~~~~~~

Get available themes.

.. code-block:: bash

   poetry run youversion get-themes [--language-tag TAG] [--json]

Options:
   ``--language-tag TAG``: Language tag (default: 'eng')
   :option:`--json`: Output as JSON

Examples:
   :code:`poetry run youversion get-themes`
   :code:`poetry run youversion get-themes --language-tag spa`

send-friend-request
~~~~~~~~~~~~~~~~~~~

Send a friend request to a user.

.. code-block:: bash

   poetry run youversion send-friend-request USER_ID [--json]

Arguments:
   ``USER_ID``: User ID to send friend request to (required)

Options:
   :option:`--json`: Output as JSON

Examples:
   :code:`poetry run youversion send-friend-request 123456`

.. note::

   For a complete list of all 47+ commands, run:

   .. code-block:: bash

      poetry run youversion --help

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

All 47+ CLI commands are available as Poetry scripts for easier access:

**Moments & Content:**
.. code-block:: bash

   poetry run votd                    # Get verse of the day
   poetry run moments                 # Get moments
   poetry run highlights              # Get highlights
   poetry run notes                   # Get notes
   poetry run bookmarks               # Get bookmarks
   poetry run images                  # Get images
   poetry run badges                  # Get badges
   poetry run create-moment           # Create a moment
   poetry run convert-notes           # Convert notes to markdown

**Plans:**
.. code-block:: bash

   poetry run plan-progress           # Get plan progress
   poetry run plan-subscriptions     # Get plan subscriptions
   poetry run plan-completions       # Get plan completions

**Bible & Audio:**
.. code-block:: bash

   poetry run get-bible-configuration # Get Bible configuration
   poetry run get-bible-versions      # Get Bible versions
   poetry run get-bible-version       # Get Bible version by ID
   poetry run get-bible-chapter       # Get Bible chapter
   poetry run get-recommended-languages # Get recommended languages
   poetry run get-audio-chapter       # Get audio chapter
   poetry run get-audio-version       # Get audio version

**Search:**
.. code-block:: bash

   poetry run search-bible            # Search Bible
   poetry run search-plans            # Search plans
   poetry run search-users            # Search users

**Videos & Images:**
.. code-block:: bash

   poetry run get-videos              # Get videos
   poetry run get-video-details       # Get video details
   poetry run get-images              # Get images
   poetry run get-image-upload-url    # Get image upload URL

**Events:**
.. code-block:: bash

   poetry run search-events           # Search events
   poetry run get-event-details       # Get event details
   poetry run get-saved-events        # Get saved events
   poetry run save-event              # Save event
   poetry run delete-saved-event      # Delete saved event
   poetry run get-all-saved-event-ids # Get all saved event IDs
   poetry run get-event-configuration # Get event configuration

**Moments Management:**
.. code-block:: bash

   poetry run get-moments             # Get moments
   poetry run get-moment-details      # Get moment details
   poetry run update-moment           # Update moment
   poetry run delete-moment           # Delete moment
   poetry run get-moment-colors       # Get moment colors
   poetry run get-moment-labels       # Get moment labels
   poetry run get-verse-colors        # Get verse colors
   poetry run hide-verse-colors      # Hide verse colors
   poetry run get-moments-configuration # Get moments configuration

**Comments & Likes:**
.. code-block:: bash

   poetry run create-comment          # Create comment
   poetry run delete-comment          # Delete comment
   poetry run like-moment             # Like moment
   poetry run unlike-moment           # Unlike moment

**Devices:**
.. code-block:: bash

   poetry run register-device         # Register device
   poetry run unregister-device       # Unregister device

**Themes:**
.. code-block:: bash

   poetry run get-themes              # Get themes
   poetry run add-theme               # Add theme
   poetry run remove-theme            # Remove theme
   poetry run set-theme               # Set theme
   poetry run get-theme-description   # Get theme description

**Social:**
.. code-block:: bash

   poetry run send-friend-request     # Send friend request

**Localization:**
.. code-block:: bash

   poetry run get-localization-items  # Get localization items

Makefile Commands
-----------------

All commands are also available via Makefile targets:

.. code-block:: bash

   # Moments & Content
   make cli-votd
   make cli-moments
   make cli-highlights
   make cli-notes
   make cli-bookmarks
   make cli-images
   make cli-badges
   make cli-create-moment KIND='note' CONTENT='...' TITLE='...'
   make cli-convert-notes

   # Plans
   make cli-plan-progress
   make cli-plan-subscriptions
   make cli-plan-completions

   # Bible & Audio
   make cli-get-bible-configuration
   make cli-get-bible-versions
   make cli-get-bible-version ID=1
   make cli-get-bible-chapter REFERENCE='GEN.1' VERSION_ID=1
   make cli-get-recommended-languages
   make cli-get-audio-chapter REFERENCE='GEN.1' VERSION_ID=1
   make cli-get-audio-version ID=1

   # Search
   make cli-search-bible QUERY='love' VERSION_ID=1
   make cli-search-plans QUERY='daily' LANGUAGE_TAG='en'
   make cli-search-users QUERY='john'

   # See all commands: make help

Output Formats
--------------

Standardized Format
~~~~~~~~~~~~~~~~~~~

All CLI commands use a standardized output format that displays:
- **ID**: Item identifier
- **Kind**: Item type (e.g., NOTE, HIGHLIGHT, PLAN_SEGMENT_COMPLETION.V1)
- **Metadata**: Key-value pairs from ``base/title/l_args`` (e.g., Segment, Title, etc.)
- **Time**: Creation timestamp

All fields are consistently aligned for easy reading:

.. code-block:: text

   1. PLAN_SEGMENT_COMPLETION.V1
      ID         : 4892085495582558077
      Kind       : PLAN_SEGMENT_COMPLETION.V1
      Segment    : 1
      Title      : Teach Us To Pray
      Time       : 2025-11-22T19:00:35+00:00

   2. NOTE
      ID         : 1234567890
      Kind       : NOTE
      Content    : This is my note
      Time       : 2025-11-22T18:00:00+00:00

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
     1. PLAN_SEGMENT_COMPLETION.V1
        ID         : 4892085495582558077
        Kind       : PLAN_SEGMENT_COMPLETION.V1
        Segment    : 1
        Title      : Teach Us To Pray
        Time       : 2025-11-22T19:00:35+00:00

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

   # Convert notes to markdown
   poetry run youversion convert-notes --json > notes.md
