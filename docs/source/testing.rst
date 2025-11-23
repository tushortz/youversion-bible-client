Testing
=======

This guide covers testing strategies for applications using the YouVersion Bible Client.

Unit Testing
------------

Mocking API Calls
~~~~~~~~~~~~~~~~~

Mock the client for unit tests:

.. code-block:: python

   from unittest.mock import AsyncMock, patch
   import pytest
   from youversion.clients import AsyncClient

   @pytest.mark.asyncio
   async def test_verse_of_the_day():
       with patch('youversion.clients.AsyncClient') as mock_client_class:
           # Create mock client
           mock_client = AsyncMock()
           mock_votd = type('Votd', (), {
               'day': 1,
               'usfm': ['JHN.3.16'],
               'image_id': None
           })()

           mock_client.verse_of_the_day.return_value = mock_votd
           mock_client_class.return_value.__aenter__.return_value = mock_client

           # Test
           async with AsyncClient() as client:
               votd = await client.verse_of_the_day()
               assert votd.day == 1
               assert votd.usfm == ['JHN.3.16']

Testing SyncClient
~~~~~~~~~~~~~~~~~~

Test synchronous client:

.. code-block:: python

   from unittest.mock import patch, MagicMock
   from youversion.clients import SyncClient

   def test_sync_client():
       with patch('youversion.clients.SyncClient') as mock_client_class:
           mock_client = MagicMock()
           mock_votd = type('Votd', (), {
               'day': 1,
               'usfm': ['JHN.3.16']
           })()

           mock_client.verse_of_the_day.return_value = mock_votd
           mock_client_class.return_value.__enter__.return_value = mock_client

           with SyncClient() as client:
               votd = client.verse_of_the_day()
               assert votd.day == 1

Integration Testing
-------------------

Testing with Real API
~~~~~~~~~~~~~~~~~~~~~

For integration tests, use real API calls:

.. code-block:: python

   import pytest
   from youversion.clients import AsyncClient

   @pytest.mark.integration
   @pytest.mark.asyncio
   async def test_real_api_call():
       """Test with real API (requires valid credentials)."""
       async with AsyncClient() as client:
           votd = await client.verse_of_the_day()
           assert votd is not None
           assert votd.day is not None
           assert votd.usfm is not None

Fixtures
--------

Create Pytest Fixtures
~~~~~~~~~~~~~~~~~~~~~~~

Create reusable test fixtures:

.. code-block:: python

   import pytest
   from unittest.mock import AsyncMock
   from youversion.clients import AsyncClient

   @pytest.fixture
   def mock_async_client():
       """Create a mock AsyncClient."""
       mock_client = AsyncMock()
       mock_votd = type('Votd', (), {
           'day': 1,
           'usfm': ['JHN.3.16']
       })()
       mock_client.verse_of_the_day.return_value = mock_votd
       return mock_client

   @pytest.mark.asyncio
   async def test_with_fixture(mock_async_client):
       with patch('youversion.clients.AsyncClient') as mock_class:
           mock_class.return_value.__aenter__.return_value = mock_async_client
           async with AsyncClient() as client:
               votd = await client.verse_of_the_day()
               assert votd.day == 1

Test Data
---------

Create Test Data Helpers
~~~~~~~~~~~~~~~~~~~~~~~~~

Create helpers for test data:

.. code-block:: python

   def create_mock_moment(**kwargs):
       """Create a mock moment for testing."""
       defaults = {
           'id': '123',
           'kind_id': 'highlight',
           'moment_title': 'Test Highlight',
           'time_ago': 'just now',
           'owned_by_me': True
       }
       defaults.update(kwargs)
       return type('Moment', (), defaults)()

   def test_moment_processing():
       moment = create_mock_moment(id='456', moment_title='Custom')
       assert moment.id == '456'
       assert moment.moment_title == 'Custom'

Best Practices
--------------

1. **Mock External Dependencies**: Always mock API calls in unit tests
2. **Test Error Cases**: Test error handling and edge cases
3. **Use Fixtures**: Create reusable test fixtures
4. **Separate Unit and Integration Tests**: Mark integration tests appropriately
5. **Test Both Clients**: Test both AsyncClient and SyncClient

