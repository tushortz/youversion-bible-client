"""Unit tests for AsyncClient class."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from youversion.clients.async_client import AsyncClient


class TestAsyncClient:
    """Test cases for AsyncClient class."""

    def test_init(self):
        """Test AsyncClient initialization."""
        username = "testuser"
        password = "testpass"

        with patch(
            "youversion.clients.async_client.BaseClient.__init__"
        ) as mock_base_init:
            mock_base_init.return_value = None

            client = AsyncClient(username=username, password=password)

            mock_base_init.assert_called_once_with(username, password)
            assert hasattr(client, "_ensure_authenticated")
            assert hasattr(client, "close")

    def test_init_without_credentials(self):
        """Test AsyncClient initialization without credentials."""
        with patch(
            "youversion.clients.async_client.BaseClient.__init__"
        ) as mock_base_init:
            mock_base_init.return_value = None

            client = AsyncClient()

            mock_base_init.assert_called_once_with(None, None)

    @pytest.mark.asyncio
    async def test_aenter_success(self):
        """Test successful async context manager entry."""
        username = "testuser"
        password = "testpass"

        with patch(
            "youversion.clients.async_client.BaseClient.__init__"
        ) as mock_base_init, patch.object(
            AsyncClient, "_ensure_authenticated", new_callable=AsyncMock
        ) as mock_auth:
            mock_base_init.return_value = None

            client = AsyncClient(username=username, password=password)

            result = await client.__aenter__()

            assert result == client
            mock_auth.assert_called_once()

    @pytest.mark.asyncio
    async def test_aexit_success(self):
        """Test successful async context manager exit."""
        username = "testuser"
        password = "testpass"

        with patch(
            "youversion.clients.async_client.BaseClient.__init__"
        ) as mock_base_init, patch.object(
            AsyncClient, "close", new_callable=AsyncMock
        ) as mock_close:
            mock_base_init.return_value = None

            client = AsyncClient(username=username, password=password)

            await client.__aexit__(None, None, None)

            mock_close.assert_called_once()

    @pytest.mark.asyncio
    async def test_aexit_with_exception(self):
        """Test async context manager exit with exception."""
        username = "testuser"
        password = "testpass"

        with patch(
            "youversion.clients.async_client.BaseClient.__init__"
        ) as mock_base_init, patch.object(
            AsyncClient, "close", new_callable=AsyncMock
        ) as mock_close:
            mock_base_init.return_value = None

            client = AsyncClient(username=username, password=password)

            # Test with exception
            exc_type = ValueError
            exc_val = ValueError("Test error")
            exc_tb = None

            await client.__aexit__(exc_type, exc_val, exc_tb)

            mock_close.assert_called_once()

    @pytest.mark.asyncio
    async def test_context_manager_usage(self):
        """Test using AsyncClient as async context manager."""
        username = "testuser"
        password = "testpass"

        with patch(
            "youversion.clients.async_client.BaseClient.__init__"
        ) as mock_base_init, patch.object(
            AsyncClient, "_ensure_authenticated", new_callable=AsyncMock
        ) as mock_auth, patch.object(
            AsyncClient, "close", new_callable=AsyncMock
        ) as mock_close:
            mock_base_init.return_value = None

            client = AsyncClient(username=username, password=password)

            async with client as ctx_client:
                assert ctx_client == client
                mock_auth.assert_called_once()

            mock_close.assert_called_once()

    @pytest.mark.asyncio
    async def test_context_manager_with_exception(self):
        """Test async context manager with exception."""
        username = "testuser"
        password = "testpass"

        with patch(
            "youversion.clients.async_client.BaseClient.__init__"
        ) as mock_base_init, patch.object(
            AsyncClient, "_ensure_authenticated", new_callable=AsyncMock
        ) as mock_auth, patch.object(
            AsyncClient, "close", new_callable=AsyncMock
        ) as mock_close:
            mock_base_init.return_value = None

            client = AsyncClient(username=username, password=password)

            with pytest.raises(ValueError):
                async with client as ctx_client:
                    assert ctx_client == client
                    mock_auth.assert_called_once()
                    raise ValueError("Test error")

            mock_close.assert_called_once()

    @pytest.mark.asyncio
    async def test_inherited_methods(self):
        """Test that AsyncClient inherits methods from BaseClient."""
        username = "testuser"
        password = "testpass"

        with patch(
            "youversion.clients.async_client.BaseClient.__init__"
        ) as mock_base_init, patch.object(
            AsyncClient, "moments", new_callable=AsyncMock
        ) as mock_moments, patch.object(
            AsyncClient, "highlights", new_callable=AsyncMock
        ) as mock_highlights, patch.object(
            AsyncClient, "verse_of_the_day", new_callable=AsyncMock
        ) as mock_votd, patch.object(
            AsyncClient, "notes", new_callable=AsyncMock
        ) as mock_notes, patch.object(
            AsyncClient, "bookmarks", new_callable=AsyncMock
        ) as mock_bookmarks, patch.object(
            AsyncClient, "my_images", new_callable=AsyncMock
        ) as mock_images, patch.object(
            AsyncClient, "plan_progress", new_callable=AsyncMock
        ) as mock_progress, patch.object(
            AsyncClient, "plan_subscriptions", new_callable=AsyncMock
        ) as mock_subs, patch.object(
            AsyncClient, "convert_note_to_md", new_callable=AsyncMock
        ) as mock_convert:
            mock_base_init.return_value = None

            client = AsyncClient(username=username, password=password)

            # Mock the _authenticator attribute since __init__ is mocked
            mock_auth = MagicMock()
            mock_auth.username = username
            client._authenticator = mock_auth

            # Test that all inherited methods are available
            assert hasattr(client, "moments")
            assert hasattr(client, "highlights")
            assert hasattr(client, "verse_of_the_day")
            assert hasattr(client, "notes")
            assert hasattr(client, "bookmarks")
            assert hasattr(client, "my_images")
            assert hasattr(client, "plan_progress")
            assert hasattr(client, "plan_subscriptions")
            assert hasattr(client, "convert_note_to_md")
            assert hasattr(client, "username")

            # Test that methods can be called
            await client.moments()
            await client.highlights()
            await client.verse_of_the_day()
            await client.notes()
            await client.bookmarks()
            await client.my_images()
            await client.plan_progress()
            await client.plan_subscriptions()
            await client.convert_note_to_md()

            # Verify all methods were called
            mock_moments.assert_called_once()
            mock_highlights.assert_called_once()
            mock_votd.assert_called_once()
            mock_notes.assert_called_once()
            mock_bookmarks.assert_called_once()
            mock_images.assert_called_once()
            mock_progress.assert_called_once()
            mock_subs.assert_called_once()
            mock_convert.assert_called_once()

    def test_username_property(self):
        """Test username property access."""
        username = "testuser"
        password = "testpass"

        with patch(
            "youversion.clients.async_client.BaseClient.__init__"
        ) as mock_base_init:
            mock_base_init.return_value = None

            client = AsyncClient(username=username, password=password)

            # Mock the _authenticator attribute since __init__ is mocked
            mock_auth = MagicMock()
            mock_auth.username = username
            client._authenticator = mock_auth

            assert client.username == username
