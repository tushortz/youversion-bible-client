Deployment
==========

This guide covers deploying applications that use the YouVersion Bible Client.

Production Considerations
-------------------------

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Always use environment variables in production:

.. code-block:: bash

   # Set in your deployment platform
   export YOUVERSION_USERNAME="production_user"
   export YOUVERSION_PASSWORD="production_password"

Docker Deployment
----------------

Dockerfile Example
~~~~~~~~~~~~~~~~~~

.. code-block:: dockerfile

   FROM python:3.11-slim

   WORKDIR /app

   # Install dependencies
   COPY pyproject.toml poetry.lock ./
   RUN pip install poetry && \
       poetry config virtualenvs.create false && \
       poetry install --no-dev

   # Copy application
   COPY . .

   # Set environment variables (or use docker-compose)
   ENV YOUVERSION_USERNAME=""
   ENV YOUVERSION_PASSWORD=""

   CMD ["python", "app.py"]

Docker Compose Example
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   version: '3.8'
   services:
     app:
       build: .
       environment:
         - YOUVERSION_USERNAME=${YOUVERSION_USERNAME}
         - YOUVERSION_PASSWORD=${YOUVERSION_PASSWORD}
       env_file:
         - .env.production

Cloud Deployment
---------------

AWS Lambda
~~~~~~~~~~

Example Lambda function:

.. code-block:: python

   import json
   import os
   from youversion.clients import SyncClient

   def lambda_handler(event, context):
       username = os.environ['YOUVERSION_USERNAME']
       password = os.environ['YOUVERSION_PASSWORD']

       with SyncClient(username=username, password=password) as client:
           votd = client.verse_of_the_day()
           return {
               'statusCode': 200,
               'body': json.dumps({
                   'day': votd.day,
                   'usfm': votd.usfm
               })
           }

Monitoring
----------

Add Logging
~~~~~~~~~~~

Implement comprehensive logging:

.. code-block:: python

   import logging
   from youversion.clients import AsyncClient

   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)

   async def monitored_api_call():
       logger.info("Starting API call")
       try:
           async with AsyncClient() as client:
               result = await client.verse_of_the_day()
               logger.info(f"API call successful: {result.usfm}")
               return result
       except Exception as e:
           logger.error(f"API call failed: {e}", exc_info=True)
           raise

Performance Monitoring
---------------------

Monitor API call performance:

.. code-block:: python

   import time
   import logging
   from youversion.clients import AsyncClient

   logger = logging.getLogger(__name__)

   async def monitored_call():
       start_time = time.time()
       try:
           async with AsyncClient() as client:
               result = await client.verse_of_the_day()
               duration = time.time() - start_time
               logger.info(f"API call completed in {duration:.2f}s")
               return result
       except Exception as e:
           duration = time.time() - start_time
           logger.error(f"API call failed after {duration:.2f}s: {e}")
           raise

