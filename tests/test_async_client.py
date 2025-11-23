"""Unit tests for AsyncClient class."""

from unittest.mock import MagicMock, patch

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

            AsyncClient()

            mock_base_init.assert_called_once_with(None, None)

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
