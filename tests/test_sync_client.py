"""Unit tests for SyncClient class."""

from unittest.mock import MagicMock, patch

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
        import asyncio

        with patch(
            "youversion.clients.sync_client.BaseClient"
        ) as mock_base_class, patch(
            "asyncio.get_running_loop"
        ) as mock_get_running, patch(
            "asyncio.set_event_loop"
        ) as mock_set_loop:
            mock_base_client = MagicMock()
            mock_base_class.return_value = mock_base_client

            # Mock no running loop
            mock_get_running.side_effect = RuntimeError("No running loop")

            client = SyncClient()
            # Create a real closed loop
            old_loop = asyncio.new_event_loop()
            old_loop.close()
            client._loop = old_loop

            # Create a new real loop
            new_loop = asyncio.new_event_loop()

            # Mock new_event_loop to return our new loop
            with patch("asyncio.new_event_loop", return_value=new_loop):
                result = client._get_loop()

            mock_set_loop.assert_called_once_with(new_loop)
            assert result == new_loop

            # Clean up
            new_loop.close()

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
                match=("Cannot use synchronous SyncClient within an async context"),
            ):
                client._get_loop()

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
