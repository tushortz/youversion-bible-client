Installation
============

Install with pip or uv.

Requirements
------------

* Python 3.9 or higher

Using pip
---------

From PyPI:

.. code-block:: bash

   pip install youversion-bible-client

From source:

.. code-block:: bash

   git clone https://github.com/tushortz/youversion-bible-client.git
   cd youversion-bible-client
   pip install -e .

Using uv
--------

From PyPI:

.. code-block:: bash

   uv add youversion-bible-client

For development:

.. code-block:: bash

   git clone https://github.com/tushortz/youversion-bible-client.git
   cd youversion-bible-client
   uv sync

Verify Installation
-------------------

.. code-block:: python

   from youversion.clients import AsyncClient, SyncClient
   print("Installation successful!")

.. code-block:: bash

   python -c "import youversion; print(youversion.__version__)"

Development dependencies
------------------------

Dev tools (pytest, ruff, black, sphinx) install with ``uv sync``. Production-only install:

.. code-block:: bash

   uv sync --no-dev

Troubleshooting
---------------

**ImportError: No module named 'youversion'**

Use the project virtualenv:

.. code-block:: bash

   uv sync
   uv run python -c "import youversion"

**Install uv**

.. code-block:: bash

   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv --version
