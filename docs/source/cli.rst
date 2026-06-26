Command Line Interface
=======================

The YouVersion Bible Client includes a comprehensive command-line interface for easy access to all features.

Installation
------------

The CLI is automatically available when you install the package:

.. code-block:: bash

   # Using uv (recommended)
   uv sync
   uv run youversion --help

   # Or using pip
   pip install -e .
   youversion --help

Basic Usage
-----------

The CLI provides several commands for accessing different types of data:

.. code-block:: bash

   # Get verse of the day
   uv run youversion votd

   # Get moments
   uv run youversion moments

   # Get highlights
   uv run youversion highlights

   # Get notes
   uv run youversion notes

   # Get bookmarks
   uv run youversion bookmarks

   # Get images
   uv run youversion images

   # Get plan progress
   uv run youversion plan-progress

   # Get plan subscriptions
   uv run youversion plan-subscriptions

   # Convert notes to markdown
   uv run youversion convert-notes

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

   uv run youversion votd [--day DAY] [--json]

Options:
   ``--day DAY``: Specific day number (1-365)
   ``--json``: Output as JSON

Examples:
   :code:`uv run youversion votd`

   :code:`uv run youversion votd --day 100`

   :code:`uv run youversion votd --json`

moments
~~~~~~~

Get user moments.

.. code-block:: bash

   uv run youversion moments [--page PAGE] [--limit LIMIT] [--json]

Options:
   ``--page PAGE``: Page number (default: 1)
   ``--limit LIMIT``: Number of items to display (default: 10)
   :option:`--json`: Output as JSON

Examples:
   :code:`uv run youversion moments`
   :code:`uv run youversion moments --page 2`
   :code:`uv run youversion moments --limit 5 --json`

highlights
~~~~~~~~~~

Get user highlights.

.. code-block:: bash

   uv run youversion highlights [--page PAGE] [--limit LIMIT] [--json]

Options:
   ``--page PAGE``: Page number (default: 1)
   ``--limit LIMIT``: Number of items to display (default: 10)
   :option:`--json`: Output as JSON

Examples:
   :code:`uv run youversion highlights`
   :code:`uv run youversion highlights --page 2 --limit 5`

notes
~~~~~

Get user notes.

.. code-block:: bash

   uv run youversion notes [--page PAGE] [--limit LIMIT] [--json]

Options:
   ``--page PAGE``: Page number (default: 1)
   ``--limit LIMIT``: Number of items to display (default: 10)
   :option:`--json`: Output as JSON

Examples:
   :code:`uv run youversion notes`
   :code:`uv run youversion notes --json`

bookmarks
~~~~~~~~~

Get user bookmarks.

.. code-block:: bash

   uv run youversion bookmarks [--page PAGE] [--limit LIMIT] [--json]

Options:
   ``--page PAGE``: Page number (default: 1)
   ``--limit LIMIT``: Number of items to display (default: 10)
   :option:`--json`: Output as JSON

Examples:
   :code:`uv run youversion bookmarks`
   :code:`uv run youversion bookmarks --page 1`

images
~~~~~~

Get user images.

.. code-block:: bash

   uv run youversion images [--page PAGE] [--limit LIMIT] [--json]

Options:
   ``--page PAGE``: Page number (default: 1)
   ``--limit LIMIT``: Number of items to display (default: 10)
   :option:`--json`: Output as JSON

Examples:
   :code:`uv run youversion images`
   :code:`uv run youversion images --json`

plan-progress
~~~~~~~~~~~~~

Get reading plan progress.

.. code-block:: bash

   uv run youversion plan-progress [--page PAGE] [--limit LIMIT] [--json]

Options:
   ``--page PAGE``: Page number (default: 1)
   ``--limit LIMIT``: Number of items to display (default: 10)
   :option:`--json`: Output as JSON

Examples:
   :code:`uv run youversion plan-progress`
   :code:`uv run youversion plan-progress --limit 5`

plan-subscriptions
~~~~~~~~~~~~~~~~~~

Get reading plan subscriptions.

.. code-block:: bash

   uv run youversion plan-subscriptions [--page PAGE] [--limit LIMIT] [--json]

Options:
   ``--page PAGE``: Page number (default: 1)
   ``--limit LIMIT``: Number of items to display (default: 10)
   :option:`--json`: Output as JSON

Examples:
   :code:`uv run youversion plan-subscriptions`
   :code:`uv run youversion plan-subscriptions --json`

convert-notes
~~~~~~~~~~~~~

Convert notes to markdown format.

.. code-block:: bash

   uv run youversion convert-notes [--json]

Options:
   :option:`--json`: Output as JSON

Examples:
   :code:`uv run youversion convert-notes`
   :code:`uv run youversion convert-notes --json`

badges
~~~~~~

Get user badges.

.. code-block:: bash

   uv run youversion badges [--page PAGE] [--limit LIMIT] [--json]

Options:
   ``--page PAGE``: Page number (default: 1)
   ``--limit LIMIT``: Number of items to display (default: 10)
   :option:`--json`: Output as JSON

Examples:
   :code:`uv run youversion badges`
   :code:`uv run youversion badges --page 1`

create-moment
~~~~~~~~~~~~~

Create a new moment (note, highlight, etc.).

.. code-block:: bash

   uv run youversion create-moment --kind KIND --content CONTENT --title TITLE [options]

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
   :code:`uv run youversion create-moment --kind note --content "My note" --title "Title"`
   :code:`uv run youversion create-moment --kind highlight --content "Text" --title "Title" --color ff0000`

get-bible-configuration
~~~~~~~~~~~~~~~~~~~~~~~~

Get Bible configuration.

.. code-block:: bash

   uv run youversion get-bible-configuration [--json]

Options:
   :option:`--json`: Output as JSON

Examples:
   :code:`uv run youversion get-bible-configuration`

get-bible-versions
~~~~~~~~~~~~~~~~~~

Get Bible versions for a language.

.. code-block:: bash

   uv run youversion get-bible-versions [--language-tag TAG] [--json]

Options:
   ``--language-tag TAG``: Language tag (default: 'eng')
   :option:`--json`: Output as JSON

Examples:
   :code:`uv run youversion get-bible-versions`
   :code:`uv run youversion get-bible-versions --language-tag spa`

get-bible-version
~~~~~~~~~~~~~~~~~

Get specific Bible version details.

.. code-block:: bash

   uv run youversion get-bible-version VERSION_ID [--json]

Arguments:
   ``VERSION_ID``: Version ID (required)

Options:
   :option:`--json`: Output as JSON

Examples:
   :code:`uv run youversion get-bible-version 1`

get-bible-chapter
~~~~~~~~~~~~~~~~~

Get Bible chapter content.

.. code-block:: bash

   uv run youversion get-bible-chapter REFERENCE [--version-id ID] [--json]

Arguments:
   ``REFERENCE``: USFM reference (e.g., 'GEN.1', 'JHN.3.16') (required)

Options:
   ``--version-id ID``: Version ID (default: 1)
   :option:`--json`: Output as JSON

Examples:
   :code:`uv run youversion get-bible-chapter GEN.1`
   :code:`uv run youversion get-bible-chapter JHN.3.16 --version-id 1`

search-bible
~~~~~~~~~~~~

Search Bible text.

.. code-block:: bash

   uv run youversion search-bible QUERY [--version-id ID] [--book BOOK] [--json]

Arguments:
   ``QUERY``: Search query (required)

Options:
   ``--version-id ID``: Version ID to search in
   ``--book BOOK``: Book filter (e.g., 'JHN', 'GEN')
   :option:`--json`: Output as JSON

Examples:
   :code:`uv run youversion search-bible "love"`
   :code:`uv run youversion search-bible "love" --version-id 1`
   :code:`uv run youversion search-bible "love" --book JHN`

get-themes
~~~~~~~~~~

Get available themes.

.. code-block:: bash

   uv run youversion get-themes [--language-tag TAG] [--json]

Options:
   ``--language-tag TAG``: Language tag (default: 'eng')
   :option:`--json`: Output as JSON

Examples:
   :code:`uv run youversion get-themes`
   :code:`uv run youversion get-themes --language-tag spa`

send-friend-request
~~~~~~~~~~~~~~~~~~~

Send a friend request to a user.

.. code-block:: bash

   uv run youversion send-friend-request USER_ID [--json]

Arguments:
   ``USER_ID``: User ID to send friend request to (required)

Options:
   :option:`--json`: Output as JSON

Examples:
   :code:`uv run youversion send-friend-request 123456`

.. note::

   For a complete list of all 47+ commands, run:

   .. code-block:: bash

      uv run youversion --help

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

Console Scripts
--------------

All 47+ CLI commands are available as console scripts after ``uv sync``:

**Moments & Content:**
.. code-block:: bash

   uv run votd                    # Get verse of the day
   uv run moments                 # Get moments
   uv run highlights              # Get highlights
   uv run notes                   # Get notes
   uv run bookmarks               # Get bookmarks
   uv run images                  # Get images
   uv run badges                  # Get badges
   uv run create-moment           # Create a moment
   uv run convert-notes           # Convert notes to markdown

**Plans:**
.. code-block:: bash

   uv run plan-progress           # Get plan progress
   uv run plan-subscriptions     # Get plan subscriptions
   uv run plan-completions       # Get plan completions

**Bible & Audio:**
.. code-block:: bash

   uv run get-bible-configuration # Get Bible configuration
   uv run get-bible-versions      # Get Bible versions
   uv run get-bible-version       # Get Bible version by ID
   uv run get-bible-chapter       # Get Bible chapter
   uv run get-recommended-languages # Get recommended languages
   uv run get-audio-chapter       # Get audio chapter
   uv run get-audio-version       # Get audio version

**Search:**
.. code-block:: bash

   uv run search-bible            # Search Bible
   uv run search-plans            # Search plans
   uv run search-users            # Search users

**Videos & Images:**
.. code-block:: bash

   uv run get-videos              # Get videos
   uv run get-video-details       # Get video details
   uv run get-images              # Get images
   uv run get-image-upload-url    # Get image upload URL

**Events:**
.. code-block:: bash

   uv run search-events           # Search events
   uv run get-event-details       # Get event details
   uv run get-saved-events        # Get saved events
   uv run save-event              # Save event
   uv run delete-saved-event      # Delete saved event
   uv run get-all-saved-event-ids # Get all saved event IDs
   uv run get-event-configuration # Get event configuration

**Moments Management:**
.. code-block:: bash

   uv run get-moments             # Get moments
   uv run get-moment-details      # Get moment details
   uv run update-moment           # Update moment
   uv run delete-moment           # Delete moment
   uv run get-moment-colors       # Get moment colors
   uv run get-moment-labels       # Get moment labels
   uv run get-verse-colors        # Get verse colors
   uv run hide-verse-colors      # Hide verse colors
   uv run get-moments-configuration # Get moments configuration

**Comments & Likes:**
.. code-block:: bash

   uv run create-comment          # Create comment
   uv run delete-comment          # Delete comment
   uv run like-moment             # Like moment
   uv run unlike-moment           # Unlike moment

**Devices:**
.. code-block:: bash

   uv run register-device         # Register device
   uv run unregister-device       # Unregister device

**Themes:**
.. code-block:: bash

   uv run get-themes              # Get themes
   uv run add-theme               # Add theme
   uv run remove-theme            # Remove theme
   uv run set-theme               # Set theme
   uv run get-theme-description   # Get theme description

**Social:**
.. code-block:: bash

   uv run send-friend-request     # Send friend request

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

   Verse of the Day
   Day: 1
   USFM: JHN.3.16
   Image ID: None

   Moments (Page 1)
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

   Error: Missing credentials
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
   uv run youversion votd

   # Get first 5 highlights
   uv run youversion highlights --limit 5

   # Get moments from page 2 as JSON
   uv run youversion moments --page 2 --json

Advanced Usage
~~~~~~~~~~~~~~

.. code-block:: bash

   # Get verse for day 100
   uv run youversion votd --day 100

   # Get all notes as JSON for processing
   uv run youversion notes --json > notes.json

   # Convert notes to markdown
   uv run youversion convert-notes --json > notes.md
