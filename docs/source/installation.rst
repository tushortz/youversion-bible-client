Installation
============

The YouVersion Bible Client can be installed using pip or Poetry.

Requirements
------------

* Python 3.9 or higher
* pip or Poetry for package management

Using pip
---------

Install from PyPI:

.. code-block:: bash

   pip install youversion-bible-client

Install from source:

.. code-block:: bash

   git clone https://github.com/tushortz/youversion-bible-client.git
   cd youversion-bible-client
   pip install -e .

Using Poetry
------------

Install using Poetry (recommended):

.. code-block:: bash

   poetry add youversion-bible-client

Or for development:

.. code-block:: bash

   git clone https://github.com/tushortz/youversion-bible-client.git
   cd youversion-bible-client
   poetry install

Verify Installation
-------------------

Verify the installation by importing the package:

.. code-block:: python

   from youversion.clients import AsyncClient, SyncClient
   print("Installation successful!")

Or check the version:

.. code-block:: bash

   python -c "import youversion; print(youversion.__version__)"

Dependencies
-----------

The package has the following runtime dependencies:

* `httpx` (>=0.25.0) - HTTP client for async requests
* `python-dotenv` (>=0.19.0) - Environment variable management
* `pydantic` (>=2.5.0) - Data validation and models
* `pyjwt` (>=2.10.1) - JWT token handling
* `typing-extensions` (>=4.0.0) - Type hints for Python 3.9

Optional Development Dependencies
----------------------------------

For development, the following packages are recommended:

* `pytest` - Testing framework
* `pytest-cov` - Coverage reporting
* `pytest-asyncio` - Async test support
* `black` - Code formatting
* `ruff` - Linting
* `mypy` - Type checking
* `sphinx` - Documentation generation

Install development dependencies:

.. code-block:: bash

   poetry install --with dev

Troubleshooting
--------------

Common Installation Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~

**ImportError: No module named 'youversion'**

Make sure the package is installed in the correct Python environment:

.. code-block:: bash

   # Check Python version
   python --version

   # Verify installation
   pip list | grep youversion-bible-client

**Permission Denied Errors**

Use a virtual environment:

.. code-block:: bash

   # Create virtual environment
   python -m venv venv

   # Activate (Linux/Mac)
   source venv/bin/activate

   # Activate (Windows)
   venv\Scripts\activate

   # Install package
   pip install youversion-bible-client

**Poetry Installation Issues**

Ensure Poetry is properly installed:

.. code-block:: bash

   # Install Poetry
   curl -sSL https://install.python-poetry.org | python3 -

   # Verify installation
   poetry --version

