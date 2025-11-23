Dynamic Pydantic Models
======================

The YouVersion Bible Client uses dynamic Pydantic model generation to automatically create type-safe models from API responses.

How It Works
------------

Instead of pre-defining models for every possible API response structure, the client dynamically generates Pydantic models at runtime based on the actual API response data.

Benefits
--------

* **Flexibility**: Automatically adapts to API response changes
* **Type Safety**: Still provides type checking and validation
* **No Manual Updates**: Models update automatically with API changes
* **Memory Efficient**: Models are cached and reused

Model Generation Process
------------------------

1. **API Response**: Receive raw JSON from API
2. **Type Inference**: Analyze response structure
3. **Model Creation**: Generate Pydantic model class
4. **Instance Creation**: Create validated model instance
5. **Caching**: Cache model classes for reuse

Example
-------

When you call an API method:

.. code-block:: python

   from youversion.clients import SyncClient

   with SyncClient() as client:
       # API returns raw JSON
       # Client automatically creates a Pydantic model
       moment = client.moments()[0]

       # moment is a dynamically created Pydantic model
       print(type(moment))  # <class 'pydantic.main.Moment_...'>
       print(moment.id)
       print(moment.moment_title)

Model Naming
------------

Models are named based on their context:

* **List Elements**: Field names are converted to PascalCase
  * ``verses`` → ``Verse`` model
  * ``download_urls`` → ``DownloadUrl`` model
  * ``user_ids`` → ``UserId`` model

* **Nested Models**: Created recursively for nested structures

Example:

.. code-block:: python

   # API response structure:
   {
       "results": [
           {
               "verses": [
                   {"text": "...", "reference": "..."}
               ]
           }
       ]
   }

   # Generated models:
   # - Results (for list items)
   # - Verse (for verses list items)
   # - Each with proper type hints

Accessing Dynamic Models
------------------------

Dynamic models behave like regular Pydantic models:

.. code-block:: python

   from youversion.clients import SyncClient

   with SyncClient() as client:
       moments = client.moments()

       for moment in moments:
           # Access attributes
           print(moment.id)
           print(moment.moment_title)

           # Convert to dict
           data = moment.model_dump()

           # Convert to JSON
           json_data = moment.model_dump_json()

           # Validate (already validated on creation)
           assert isinstance(moment, type(moment))

Type Checking
-------------

While models are dynamic, you can still use type hints:

.. code-block:: python

   from typing import Any, List
   from youversion.clients import AsyncClient

   async def process_moments() -> List[Any]:
       async with AsyncClient() as client:
           moments = await client.moments()
           return moments

   # Or use Protocols for better type checking
   from youversion.models.base import Moment

   async def process_moments() -> List[Moment]:
       async with AsyncClient() as client:
           moments = await client.moments()
           return moments

Model Caching
-------------

Models are cached to improve performance:

.. code-block:: python

   from youversion.clients import SyncClient

   with SyncClient() as client:
       # First call - creates and caches model
       moments1 = client.moments(page=1)

       # Second call - reuses cached model
       moments2 = client.moments(page=2)

       # Same model class is used
       assert type(moments1[0]) == type(moments2[0])

Nested Structures
-----------------

Dynamic models handle nested structures automatically:

.. code-block:: python

   from youversion.clients import SyncClient

   with SyncClient() as client:
       # Search results with nested verses
       results = client.search_bible("love")

       # Nested models are created automatically
       for result in results.get("results", []):
           for verse in result.get("verses", []):
               # verse is a dynamically created Pydantic model
               print(verse.text)
               print(verse.reference)

Validation
----------

Dynamic models still provide Pydantic validation:

.. code-block:: python

   from youversion.clients import SyncClient
   from pydantic import ValidationError

   with SyncClient() as client:
       try:
           moments = client.moments()
           # All moments are validated
       except ValidationError as e:
           print(f"Validation error: {e}")

Serialization
-------------

Dynamic models support all Pydantic serialization methods:

.. code-block:: python

   from youversion.clients import SyncClient

   with SyncClient() as client:
       moment = client.moments()[0]

       # Convert to dict
       data = moment.model_dump()

       # Convert to JSON string
       json_str = moment.model_dump_json()

       # Convert with exclusions
       minimal = moment.model_dump(exclude={'user', 'actions'})

       # Convert with only specific fields
       limited = moment.model_dump(include={'id', 'moment_title'})

Limitations
-----------

* **No Static Type Checking**: Models are created at runtime
* **IDE Support**: Limited autocomplete for dynamic models
* **Documentation**: Model structure not known until runtime

Workarounds
-----------

Use Protocols for Better IDE Support
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Define Protocols for better type hints:

.. code-block:: python

   from typing import Protocol
   from youversion.models.base import MomentProtocol

   def process_moment(moment: MomentProtocol) -> str:
       """Process a moment with type checking."""
       return f"{moment.id}: {moment.moment_title}"

   from youversion.clients import SyncClient
   with SyncClient() as client:
       moments = client.moments()
       for moment in moments:
           result = process_moment(moment)  # Type checked!

Inspect Model Structure
~~~~~~~~~~~~~~~~~~~~~~~

Inspect model fields at runtime:

.. code-block:: python

   from youversion.clients import SyncClient

   with SyncClient() as client:
       moment = client.moments()[0]

       # Get model fields
       fields = moment.model_fields
       for field_name, field_info in fields.items():
           print(f"{field_name}: {field_info.annotation}")

Best Practices
--------------

1. **Use Protocols**: Define Protocols for better type checking
2. **Handle Missing Fields**: Use optional access for dynamic fields
3. **Validate Early**: Check data structure before processing
4. **Cache Results**: Cache processed data to avoid re-processing
5. **Document Assumptions**: Document expected model structure

Example: Working with Dynamic Models
-------------------------------------

.. code-block:: python

   from youversion.clients import SyncClient
   from typing import Any

   def process_dynamic_moment(moment: Any) -> dict:
       """Process a dynamically created moment model."""
       # Safely access fields
       data = {
           'id': getattr(moment, 'id', None),
           'title': getattr(moment, 'moment_title', 'Untitled'),
           'kind': getattr(moment, 'kind_id', 'unknown'),
       }

       # Convert to dict for easier manipulation
       full_data = moment.model_dump()

       # Merge with custom data
       return {**full_data, **data}

   with SyncClient() as client:
       moments = client.moments()
       processed = [process_dynamic_moment(m) for m in moments]

