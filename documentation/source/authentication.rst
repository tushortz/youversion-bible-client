Authentication
==============

The YouVersion Bible Client uses OAuth2 authentication to securely access the YouVersion API.

How Authentication Works
-------------------------

1. **OAuth2 Token Request**: The client sends credentials to YouVersion's OAuth2 endpoint
2. **Token Response**: YouVersion returns an access token (JWT)
3. **Token Decoding**: The client decodes the JWT to extract user information
4. **Authenticated Requests**: All subsequent requests include the Bearer token

Authentication Flow
--------------------

.. code-block:: python

   from youversion.clients import AsyncClient

   async with AsyncClient() as client:
       # Authentication happens automatically on first API call
       # The client:
       # 1. Gets OAuth2 token
       # 2. Decodes JWT to extract user_id
       # 3. Stores token for subsequent requests

       votd = await client.verse_of_the_day()
       # Token is automatically included in request headers

Token Management
----------------

The client automatically manages authentication tokens:

* **Automatic Authentication**: Tokens are obtained on first API call
* **Token Caching**: Tokens are cached for the client instance lifetime
* **Automatic Refresh**: Tokens are refreshed as needed
* **Cleanup**: Tokens are cleared when client is closed

Accessing User Information
---------------------------

After authentication, you can access user information:

.. code-block:: python

   from youversion.clients import SyncClient

   with SyncClient() as client:
       # Get username
       username = client.username
       print(f"Authenticated as: {username}")

       # Get user ID (available after first API call)
       # Make any API call first
       client.verse_of_the_day()
       user_id = client.user_id
       print(f"User ID: {user_id}")

Authentication Errors
---------------------

Common authentication errors and solutions:

ValueError: Missing Credentials
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error:**
.. code-block:: text

   ValueError: Username and password must be provided either as arguments
   or as YOUVERSION_USERNAME and YOUVERSION_PASSWORD environment variables

**Solution:**
Provide credentials via environment variables, `.env` file, or constructor arguments.

HTTP 401: Unauthorized
~~~~~~~~~~~~~~~~~~~~~~

**Error:**
.. code-block:: text

   httpx.HTTPStatusError: 401 Unauthorized

**Solution:**
Check that your credentials are correct:

.. code-block:: python

   from youversion.clients import SyncClient

   try:
       with SyncClient() as client:
           client.verse_of_the_day()
   except httpx.HTTPStatusError as e:
       if e.response.status_code == 401:
           print("Invalid credentials. Please check your username and password.")

HTTP 403: Forbidden
~~~~~~~~~~~~~~~~~~~

**Error:**
.. code-block:: text

   httpx.HTTPStatusError: 403 Forbidden

**Solution:**
Your account may not have access to the requested resource. Check your account permissions.

Token Expiration
----------------

Access tokens may expire. The client handles this automatically:

.. code-block:: python

   from youversion.clients import AsyncClient
   import asyncio

   async def long_running_task():
       async with AsyncClient() as client:
           # Token obtained here
           votd1 = await client.verse_of_the_day()

           # Wait a long time...
           await asyncio.sleep(3600)  # 1 hour

           # If token expired, client will re-authenticate automatically
           votd2 = await client.verse_of_the_day()

   asyncio.run(long_running_task())

Best Practices
--------------

1. **Reuse Client Instances**: Create one client and reuse it for multiple requests
2. **Use Context Managers**: Always use ``async with`` or ``with`` for automatic cleanup
3. **Handle Errors Gracefully**: Catch and handle authentication errors appropriately
4. **Don't Share Tokens**: Each client instance manages its own tokens
5. **Secure Credentials**: Never log or expose credentials in error messages

Example: Secure Authentication
-------------------------------

.. code-block:: python

   import os
   from youversion.clients import AsyncClient
   import httpx

   async def secure_authenticate():
       # Get credentials from secure source
       username = os.getenv("YOUVERSION_USERNAME")
       password = os.getenv("YOUVERSION_PASSWORD")

       if not username or not password:
           raise ValueError("Credentials not found in environment")

       try:
           async with AsyncClient(username=username, password=password) as client:
               # Verify authentication works
               votd = await client.verse_of_the_day()
               print(f"Authenticated successfully as: {client.username}")
               return client
       except httpx.HTTPStatusError as e:
           if e.response.status_code == 401:
               raise ValueError("Invalid credentials")
           raise

   # Usage
   import asyncio
   client = asyncio.run(secure_authenticate())

