Configuration
=============

The YouVersion Bible Client supports multiple ways to configure authentication and behavior.

Authentication Methods
----------------------

The client supports three methods for providing credentials:

1. Environment Variables (Recommended for Production)
2. `.env` File (Recommended for Development)
3. Constructor Arguments (For Scripts)

Environment Variables
----------------------

Set the following environment variables:

.. code-block:: bash

   export YOUVERSION_USERNAME="your_username"
   export YOUVERSION_PASSWORD="your_password"

For Windows (PowerShell):

.. code-block:: powershell

   $env:YOUVERSION_USERNAME="your_username"
   $env:YOUVERSION_PASSWORD="your_password"

For Windows (CMD):

.. code-block:: cmd

   set YOUVERSION_USERNAME=your_username
   set YOUVERSION_PASSWORD=your_password

.env File
---------

Create a ``.env`` file in your project root:

.. code-block:: bash

   # .env file
   YOUVERSION_USERNAME=your_username
   YOUVERSION_PASSWORD=your_password

The client automatically loads this file using ``python-dotenv``.

Constructor Arguments
---------------------

Pass credentials directly to the client:

.. code-block:: python

   from youversion.clients import AsyncClient

   client = AsyncClient(
       username="your_username",
       password="your_password"
   )

Priority Order
--------------

Credentials are resolved in the following order:

1. Constructor arguments (highest priority)
2. Environment variables
3. `.env` file (lowest priority)

Configuration Options
---------------------

Client Configuration
~~~~~~~~~~~~~~~~~~~~~

The client uses default configuration from ``youversion.config.Config``:

.. code-block:: python

   from youversion.config import Config

   # API base URLs
   print(Config.BIBLE_API_BASE)
   print(Config.MOMENTS_API_BASE)

   # HTTP timeout
   print(Config.HTTP_TIMEOUT)  # 30.0 seconds

   # Default headers
   print(Config.DEFAULT_HEADERS)

Custom Configuration
---------------------

You can customize behavior by modifying the Config class or using environment variables:

.. code-block:: python

   import os
   from youversion.clients import AsyncClient

   # Set custom timeout via environment
   os.environ["YOUVERSION_TIMEOUT"] = "60.0"

   # Or modify Config directly (not recommended for production)
   from youversion.config import Config
   Config.HTTP_TIMEOUT = 60.0

Error Handling
--------------

The client provides clear error messages for configuration issues:

.. code-block:: python

   from youversion.clients import AsyncClient

   try:
       client = AsyncClient()
   except ValueError as e:
       print(f"Configuration error: {e}")
       # Output: "Username and password must be provided..."

Security Best Practices
-----------------------

1. **Never commit credentials to version control**
   - Add ``.env`` to ``.gitignore``
   - Use environment variables in production

2. **Use environment variables in production**
   - Set via your deployment platform
   - Use secrets management systems

3. **Rotate credentials regularly**
   - Update passwords periodically
   - Revoke old tokens if applicable

4. **Limit access to credentials**
   - Use least privilege principle
   - Restrict file permissions on ``.env`` files

Example: Production Configuration
---------------------------------

For production deployments, use environment variables:

.. code-block:: python

   import os
   from youversion.clients import AsyncClient

   # Credentials from environment (set by deployment system)
   username = os.getenv("YOUVERSION_USERNAME")
   password = os.getenv("YOUVERSION_PASSWORD")

   if not username or not password:
       raise ValueError("Missing YouVersion credentials")

   client = AsyncClient(username=username, password=password)

Example: Development Configuration
----------------------------------

For development, use a ``.env`` file:

.. code-block:: bash

   # .env (in .gitignore)
   YOUVERSION_USERNAME=dev_user
   YOUVERSION_PASSWORD=dev_password

.. code-block:: python

   from youversion.clients import SyncClient

   # Automatically loads from .env
   with SyncClient() as client:
       # Use client...
       pass

