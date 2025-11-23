"""Unit tests for BaseClient class."""

from unittest.mock import MagicMock, patch

from youversion.core.base_client import BaseClient


class TestBaseClient:
    """Test cases for BaseClient class."""

    def test_init_with_credentials(self):
        """Test initializing base client with explicit credentials."""
        username = "testuser"
        password = "testpass"

        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ) as mock_processor_class:
            mock_auth = MagicMock()
            mock_auth.username = username
            mock_auth.password = password
            mock_auth_class.return_value = mock_auth

            mock_processor = MagicMock()
            mock_processor_class.return_value = mock_processor

            client = BaseClient(username=username, password=password)

            assert client._authenticator == mock_auth
            assert client._data_processor == mock_processor
            assert client._http_client is None
            mock_auth_class.assert_called_once_with(username, password)

    def test_init_without_credentials(self):
        """Test initializing base client without explicit credentials."""
        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ) as mock_processor_class:
            mock_auth = MagicMock()
            mock_auth_class.return_value = mock_auth

            mock_processor = MagicMock()
            mock_processor_class.return_value = mock_processor

            client = BaseClient()

            assert client._authenticator == mock_auth
            assert client._data_processor == mock_processor
            assert client._http_client is None
            mock_auth_class.assert_called_once_with(None, None)

    def test_username_property(self):
        """Test username property."""
        username = "testuser"
        password = "testpass"

        with patch("youversion.core.base_client.Authenticator"), patch(
            "youversion.core.base_client.DataProcessor"
        ) as mock_processor_class:
            mock_auth = MagicMock()
            mock_auth.username = username
            mock_auth.password = password

            mock_processor = MagicMock()
            mock_processor_class.return_value = mock_processor

            client = BaseClient(username=username, password=password)
            client._authenticator = mock_auth

            assert client.username == username
