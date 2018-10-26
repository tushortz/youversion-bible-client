"""Unit tests for SyncClient class."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from youversion.clients.sync_client import SyncClient


class TestSyncClient:
    """Test cases for SyncClient class."""

    def test_init(self):
        """Test SyncClient initialization."""
        username = "testuser"
        password = "testpass"

        with patch(
            "youversion.clients.sync_client.BaseClient.__init__"
        ) as mock_base_init:
            mock_base_init.return_value = None

            client = SyncClient(username=username, password=password)

            mock_base_init.assert_called_once_with(client, username, password)
            assert client._loop is None
            assert client._loop_owner is False

    def test_init_without_credentials(self):
        """Test SyncClient initialization without credentials."""
        with patch(
            "youversion.clients.sync_client.BaseClient.__init__"
        ) as mock_base_init:
            mock_base_init.return_value = None

            client = SyncClient()

            mock_base_init.assert_called_once_with(client, None, None)

    def test_get_loop_no_running_loop(self):
        """Test getting event loop when no loop is running."""
        with patch(
            "youversion.clients.sync_client.BaseClient"
        ) as mock_base_class, patch(
            "asyncio.get_running_loop"
        ) as mock_get_running, patch(
            "asyncio.new_event_loop"
        ) as mock_new_loop, patch(
            "asyncio.set_event_loop"
        ) as mock_set_loop:
            mock_base_client = MagicMock()
            mock_base_class.return_value = mock_base_client

            # Mock no running loop
            mock_get_running.side_effect = RuntimeError("No running loop")

            mock_loop = MagicMock()
            mock_loop.is_closed.return_value = False
            mock_new_loop.return_value = mock_loop

            client = SyncClient()

            result = client._get_loop()

            assert result == mock_loop
            assert client._loop == mock_loop
            assert client._loop_owner is True
            mock_new_loop.assert_called_once()
            mock_set_loop.assert_called_once_with(mock_loop)

    def test_get_loop_existing_loop(self):
        """Test getting event loop when loop already exists."""
        with patch(
            "youversion.clients.sync_client.BaseClient"
        ) as mock_base_class, patch("asyncio.get_running_loop") as mock_get_running:
            mock_base_client = MagicMock()
            mock_base_class.return_value = mock_base_client

            # Mock no running loop
            mock_get_running.side_effect = RuntimeError("No running loop")

            client = SyncClient()
            client._loop = MagicMock()
            client._loop.is_closed.return_value = False

            result = client._get_loop()

            assert result == client._loop

    def test_get_loop_closed_loop(self):
        """Test getting event loop when existing loop is closed."""
        with patch(
            "youversion.clients.sync_client.BaseClient"
        ) as mock_base_class, patch(
            "asyncio.get_running_loop"
        ) as mock_get_running, patch(
            "asyncio.new_event_loop"
        ) as mock_new_loop, patch(
            "asyncio.set_event_loop"
        ) as mock_set_loop:
            mock_base_client = MagicMock()
            mock_base_class.return_value = mock_base_client

            # Mock no running loop
            mock_get_running.side_effect = RuntimeError("No running loop")

            client = SyncClient()
            client._loop = MagicMock()
            client._loop.is_closed.return_value = True

            mock_new_loop.return_value = MagicMock()

            client._get_loop()

            mock_new_loop.assert_called_once()

    def test_get_loop_running_loop_error(self):
        """Test getting event loop when already in async context."""
        with patch(
            "youversion.clients.sync_client.BaseClient"
        ) as mock_base_class, patch("asyncio.get_running_loop") as mock_get_running:
            mock_base_client = MagicMock()
            mock_base_class.return_value = mock_base_client

            # Mock running loop
            mock_get_running.return_value = MagicMock()

            client = SyncClient()

            with pytest.raises(
                RuntimeError,
                match="Cannot use synchronous SyncClient within an async context",
            ):
                client._get_loop()

    def test_run_async_success(self):
        """Test running async coroutine successfully."""
        with patch(
            "youversion.clients.sync_client.BaseClient"
        ) as mock_base_class, patch(
            "asyncio.get_running_loop"
        ) as mock_get_running, patch(
            "asyncio.new_event_loop"
        ) as mock_new_loop, patch(
            "asyncio.set_event_loop"
        ) as mock_set_loop:
            mock_base_client = MagicMock()
            # Mock _ensure_authenticated as a regular mock since it's awaited in _run_async
            mock_base_client._ensure_authenticated = MagicMock()
            mock_base_class.return_value = mock_base_client

            # Mock no running loop
            mock_get_running.side_effect = RuntimeError("No running loop")

            mock_loop = MagicMock()
            mock_loop.run_until_complete.return_value = "test_result"
            mock_new_loop.return_value = mock_loop

            client = SyncClient()
            client._authenticator = mock_base_client

            # Mock the coroutine to avoid creating real async objects
            mock_coro = MagicMock()
            mock_coro.__await__ = lambda self: iter([])

            result = client._run_async(mock_coro)

            assert result == "test_result"
            mock_loop.run_until_complete.assert_called_once()

    def test_enter_exit_context_manager(self):
        """Test using SyncClient as context manager."""
        with patch(
            "youversion.clients.sync_client.BaseClient"
        ) as mock_base_class, patch(
            "asyncio.get_running_loop"
        ) as mock_get_running, patch(
            "asyncio.new_event_loop"
        ) as mock_new_loop, patch(
            "asyncio.set_event_loop"
        ) as mock_set_loop:
            mock_base_client = MagicMock()
            # Mock _ensure_authenticated as AsyncMock since it's awaited in _ensure_client_initialized
            mock_base_client._ensure_authenticated = AsyncMock()
            # Mock close as a regular mock since SyncClient.close is synchronous
            mock_base_client.close = MagicMock()
            mock_base_class.return_value = mock_base_client

            # Mock no running loop
            mock_get_running.side_effect = RuntimeError("No running loop")

            mock_loop = MagicMock()
            mock_loop.run_until_complete.return_value = None
            mock_loop.is_closed.return_value = False
            mock_new_loop.return_value = mock_loop

            client = SyncClient()
            client._authenticator = mock_base_client

            # Mock _run_async to avoid creating real coroutines
            client._run_async = MagicMock(side_effect=lambda coro: None)

            # Mock the async context manager methods to avoid creating coroutines
            client.__aenter__ = MagicMock(return_value=client)
            client.__aexit__ = MagicMock(return_value=None)

            with client as ctx_client:
                assert ctx_client == client

            # Verify context manager methods were called
            assert client._run_async.call_count == 2  # __enter__ and __exit__
            # Note: mock_loop.close() is not called when _run_async is mocked

    def test_close_manual(self):
        """Test manual client closure."""
        with patch(
            "youversion.clients.sync_client.BaseClient"
        ) as mock_base_class, patch(
            "asyncio.get_running_loop"
        ) as mock_get_running, patch(
            "asyncio.new_event_loop"
        ) as mock_new_loop, patch(
            "asyncio.set_event_loop"
        ) as mock_set_loop:
            mock_base_client = MagicMock()
            # Mock close as a regular mock since SyncClient.close is synchronous
            mock_base_client.close = MagicMock()
            mock_base_class.return_value = mock_base_client

            # Mock no running loop
            mock_get_running.side_effect = RuntimeError("No running loop")

            mock_loop = MagicMock()
            mock_loop.run_until_complete.return_value = None
            mock_loop.is_closed.return_value = False
            mock_new_loop.return_value = mock_loop

            client = SyncClient()
            client._loop_owner = True

            client.close()

            mock_loop.run_until_complete.assert_called_once()
            mock_loop.close.assert_called_once()

    def test_close_no_loop_owner(self):
        """Test client closure when not loop owner."""
        with patch(
            "youversion.clients.sync_client.BaseClient"
        ) as mock_base_class, patch(
            "asyncio.get_running_loop"
        ) as mock_get_running, patch(
            "asyncio.new_event_loop"
        ) as mock_new_loop, patch(
            "asyncio.set_event_loop"
        ) as mock_set_loop:
            mock_base_client = MagicMock()
            # Mock _ensure_authenticated as a regular mock since it's awaited in _run_async
            mock_base_client._ensure_authenticated = MagicMock()
            mock_base_class.return_value = mock_base_client

            # Mock no running loop
            mock_get_running.side_effect = RuntimeError("No running loop")

            mock_loop = MagicMock()
            mock_loop.run_until_complete.return_value = None
            mock_loop.is_closed.return_value = False
            mock_new_loop.return_value = mock_loop

            client = SyncClient()
            client._loop_owner = False
            client._async_client = MagicMock()
            client._async_client.close = MagicMock()

            client.close()

            mock_loop.run_until_complete.assert_called_once()
            mock_loop.close.assert_not_called()

    def test_close_closed_loop(self):
        """Test client closure when loop is already closed."""
        with patch(
            "youversion.clients.sync_client.BaseClient"
        ) as mock_base_class, patch(
            "asyncio.get_running_loop"
        ) as mock_get_running, patch(
            "asyncio.new_event_loop"
        ) as mock_new_loop, patch(
            "asyncio.set_event_loop"
        ) as mock_set_loop:
            mock_base_client = MagicMock()
            # Mock close as a regular mock since SyncClient.close is synchronous
            mock_base_client.close = MagicMock()
            mock_base_class.return_value = mock_base_client

            # Mock no running loop
            mock_get_running.side_effect = RuntimeError("No running loop")

            mock_loop = MagicMock()
            mock_loop.run_until_complete.return_value = None
            mock_loop.is_closed.return_value = True
            mock_new_loop.return_value = mock_loop

            client = SyncClient()
            client._loop_owner = True

            client.close()

            mock_loop.run_until_complete.assert_called_once()
            mock_loop.close.assert_not_called()

    def test_sync_methods(self):
        """Test that all sync wrapper methods work correctly."""
        with patch(
            "youversion.clients.sync_client.BaseClient"
        ) as mock_base_class, patch(
            "asyncio.get_running_loop"
        ) as mock_get_running, patch(
            "asyncio.new_event_loop"
        ) as mock_new_loop, patch(
            "asyncio.set_event_loop"
        ) as mock_set_loop:
            mock_base_client = MagicMock()
            # Mock _ensure_authenticated as a regular mock since it's awaited in _run_async
            mock_base_client._ensure_authenticated = MagicMock()
            mock_base_client.moments = MagicMock(return_value=[])
            mock_base_client.highlights = MagicMock(return_value=[])
            mock_base_client.verse_of_the_day = MagicMock(return_value=MagicMock())
            mock_base_client.notes = MagicMock(return_value=[])
            mock_base_client.bookmarks = MagicMock(return_value=[])
            mock_base_client.my_images = MagicMock(return_value=[])
            mock_base_client.plan_progress = MagicMock(return_value=[])
            mock_base_client.plan_subscriptions = MagicMock(return_value=[])
            mock_base_client.convert_note_to_md = MagicMock(return_value=[])
            mock_base_class.return_value = mock_base_client

            # Mock no running loop
            mock_get_running.side_effect = RuntimeError("No running loop")

            mock_loop = MagicMock()
            mock_loop.run_until_complete.return_value = []
            mock_new_loop.return_value = mock_loop

            client = SyncClient()
            client._authenticator = mock_base_client

            # Test all sync methods
            client.moments()
            client.highlights()
            client.verse_of_the_day()
            client.notes()
            client.bookmarks()
            client.my_images()
            client.plan_progress()
            client.plan_subscriptions()
            client.convert_note_to_md()

            # Verify all methods were called
            assert mock_loop.run_until_complete.call_count == 9

    def test_username_property(self):
        """Test username property access."""
        username = "testuser"
        password = "testpass"

        with patch("youversion.clients.sync_client.BaseClient") as mock_base_class:
            mock_base_client = MagicMock()
            mock_base_client.username = username
            mock_base_class.return_value = mock_base_client

            client = SyncClient(username=username, password=password)

            assert client.username == username

    @pytest.mark.asyncio
    async def test_aenter_aexit_async_context_manager(self):
        """Test using SyncClient as async context manager."""
        with patch(
            "youversion.clients.sync_client.BaseClient.__init__"
        ) as mock_base_init, patch(
            "youversion.clients.sync_client.BaseClient.close", new_callable=AsyncMock
        ) as mock_close:
            mock_base_init.return_value = None

            client = SyncClient()

            # Mock the _ensure_authenticated method as AsyncMock since it's awaited directly in async context manager
            client._ensure_authenticated = AsyncMock()

            async with client as ctx_client:
                assert ctx_client == client

            client._ensure_authenticated.assert_called_once()
            mock_close.assert_called_once()

    @pytest.mark.asyncio
    async def test_aexit_with_exception(self):
        """Test async context manager exit with exception."""
        with patch(
            "youversion.clients.sync_client.BaseClient.__init__"
        ) as mock_base_init, patch(
            "youversion.clients.sync_client.BaseClient.close", new_callable=AsyncMock
        ) as mock_close:
            mock_base_init.return_value = None

            client = SyncClient()

            # Mock the _ensure_authenticated method as AsyncMock since it's awaited directly in async context manager
            client._ensure_authenticated = AsyncMock()

            with pytest.raises(ValueError):
                async with client as ctx_client:
                    assert ctx_client == client
                    raise ValueError("Test error")

            client._ensure_authenticated.assert_called_once()
            mock_close.assert_called_once()
