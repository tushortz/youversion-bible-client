"""Extended unit tests for BaseClient class to improve coverage."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from youversion.core.base_client import BaseClient


class TestBaseClientExtended:
    """Extended test cases for BaseClient class."""

    @pytest.mark.asyncio
    async def test_ensure_authenticated(self):
        """Test _ensure_authenticated method."""
        username = "testuser"
        password = "testpass"

        mock_http_client = MagicMock()
        mock_auth = MagicMock()
        mock_auth.username = username
        mock_auth.password = password
        mock_auth.user_id = 12345
        mock_auth.access_token = "test_token"
        mock_auth.authenticate = AsyncMock(return_value=mock_http_client)

        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ), patch(
            "youversion.core.base_client.HttpClient"
        ) as mock_http_class:
            mock_auth_class.return_value = mock_auth
            mock_http_class.return_value = MagicMock()

            client = BaseClient(username=username, password=password)
            await client._ensure_authenticated()

            assert client._http_client is not None
            assert client._user_id == 12345
            assert client._access_token == "test_token"

    @pytest.mark.asyncio
    async def test_ensure_authenticated_already_authenticated(self):
        """Test _ensure_authenticated when already authenticated."""
        username = "testuser"
        password = "testpass"

        mock_http_client = MagicMock()
        mock_auth = MagicMock()
        mock_auth.username = username
        mock_auth.password = password

        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ):
            mock_auth_class.return_value = mock_auth

            client = BaseClient(username=username, password=password)
            client._http_client = mock_http_client

            # Should not call authenticate again
            await client._ensure_authenticated()
            mock_auth.authenticate.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_cards_data(self):
        """Test _get_cards_data method."""
        username = "testuser"
        password = "testpass"

        mock_http_client = MagicMock()
        mock_http_client.get_cards = AsyncMock(
            return_value={
                "response": {
                    "data": {"moments": [{"id": 1, "kind_id": "note"}]}
                }
            }
        )

        mock_auth = MagicMock()
        mock_auth.username = username
        mock_auth.password = password

        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ):
            mock_auth_class.return_value = mock_auth

            client = BaseClient(username=username, password=password)
            client._http_client = mock_http_client

            result = await client._get_cards_data(kind="note", page=1)

            assert isinstance(result, list)
            assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_cards_data_no_response_key(self):
        """Test _get_cards_data when response key is missing."""
        username = "testuser"
        password = "testpass"

        mock_http_client = MagicMock()
        mock_http_client.get_cards = AsyncMock(return_value={"moments": []})

        mock_auth = MagicMock()
        mock_auth.username = username
        mock_auth.password = password

        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ):
            mock_auth_class.return_value = mock_auth

            client = BaseClient(username=username, password=password)
            client._http_client = mock_http_client

            result = await client._get_cards_data()

            assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_user_id_property(self):
        """Test user_id property."""
        username = "testuser"
        password = "testpass"

        with patch("youversion.core.base_client.Authenticator"), patch(
            "youversion.core.base_client.DataProcessor"
        ):
            client = BaseClient(username=username, password=password)
            client._user_id = 12345

            assert client.user_id == 12345

    @pytest.mark.asyncio
    async def test_close(self):
        """Test close method."""
        username = "testuser"
        password = "testpass"

        mock_http_client = MagicMock()
        mock_http_client.close = AsyncMock()

        with patch("youversion.core.base_client.Authenticator"), patch(
            "youversion.core.base_client.DataProcessor"
        ):
            client = BaseClient(username=username, password=password)
            client._http_client = mock_http_client

            await client.close()

            mock_http_client.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_close_no_http_client(self):
        """Test close method when http_client is None."""
        username = "testuser"
        password = "testpass"

        with patch("youversion.core.base_client.Authenticator"), patch(
            "youversion.core.base_client.DataProcessor"
        ):
            client = BaseClient(username=username, password=password)
            client._http_client = None

            # Should not raise an error
            await client.close()

    @pytest.mark.asyncio
    async def test_convert_note_to_md(self):
        """Test convert_note_to_md method."""
        username = "testuser"
        password = "testpass"

        mock_http_client = MagicMock()
        mock_http_client.get_cards = AsyncMock(
            return_value={
                "moments": [{"id": 1, "kind_id": "note"}],
            }
        )

        mock_auth = MagicMock()
        mock_auth.username = username
        mock_auth.password = password

        mock_processor = MagicMock()
        mock_processor.process_notes = MagicMock(
            return_value=[{"id": 1, "kind_id": "note"}]
        )

        with patch(
            "youversion.core.base_client.Authenticator"
        ) as mock_auth_class, patch(
            "youversion.core.base_client.DataProcessor"
        ) as mock_processor_class:
            mock_auth_class.return_value = mock_auth
            mock_processor_class.return_value = mock_processor

            client = BaseClient(username=username, password=password)
            client._http_client = mock_http_client

            result = await client.convert_note_to_md()

            assert isinstance(result, list)

