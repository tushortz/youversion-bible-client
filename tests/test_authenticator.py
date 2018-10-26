"""Unit tests for Authenticator class."""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from youversion.config import Config
from youversion.core.authenticator import Authenticator


class TestAuthenticator:
    """Test cases for Authenticator class."""

    def test_init_with_credentials(self):
        """Test initializing authenticator with explicit credentials."""
        username = "testuser"
        password = "testpass"

        with patch("dotenv.load_dotenv"):
            auth = Authenticator(username=username, password=password)

            assert auth.username == username
            assert auth.password == password

    @patch.dict(
        os.environ, {"YOUVERSION_USERNAME": "envuser", "YOUVERSION_PASSWORD": "envpass"}
    )
    def test_init_with_env_vars(self):
        """Test initializing authenticator with environment variables."""
        with patch("dotenv.load_dotenv"):
            auth = Authenticator()

            assert auth.username == "envuser"
            assert auth.password == "envpass"

    def test_init_missing_password(self):
        """Test initializing authenticator with missing password."""
        with patch("dotenv.load_dotenv"), patch("os.getenv") as mock_getenv:
            # Mock os.getenv to return None for environment variables
            mock_getenv.return_value = None
            with pytest.raises(
                ValueError,
                match="Username and password must be provided either as arguments",
            ):
                # Explicitly set password to None
                Authenticator(username="testuser", password=None)

    def test_init_missing_username(self):
        """Test initializing authenticator with missing username."""
        with patch("dotenv.load_dotenv"), patch("os.getenv") as mock_getenv:
            # Mock os.getenv to return None for environment variables
            mock_getenv.return_value = None
            with pytest.raises(
                ValueError,
                match="Username and password must be provided either as arguments",
            ):
                # Explicitly set username to None
                Authenticator(username=None, password="testpass")

    def test_credentials_properties(self):
        """Test accessing username and password properties."""
        username = "testuser"
        password = "testpass"

        with patch("dotenv.load_dotenv"):
            auth = Authenticator(username=username, password=password)

            assert auth.username == username
            assert auth.password == password

    @pytest.mark.asyncio
    async def test_authenticate_success(self):
        """Test successful authentication."""
        username = "testuser"
        password = "testpass"
        access_token = "test_access_token"

        mock_token_response = {"access_token": access_token}

        with patch("dotenv.load_dotenv"), patch(
            "httpx.AsyncClient"
        ) as mock_client_class:
            # Mock the token request
            mock_token_client = AsyncMock()
            mock_token_response_obj = MagicMock()
            mock_token_response_obj.json.return_value = mock_token_response
            mock_token_response_obj.raise_for_status.return_value = None
            mock_token_client.post.return_value = mock_token_response_obj

            # Mock the authenticated client
            mock_auth_client = AsyncMock()

            # Configure the mock to return different clients for different calls
            mock_client_class.side_effect = [
                mock_token_client,  # First call for token request
                mock_auth_client,  # Second call for authenticated client
            ]

            # Mock the context manager behavior
            mock_token_client.__aenter__.return_value = mock_token_client
            mock_token_client.__aexit__.return_value = None

            auth = Authenticator(username=username, password=password)
            client = await auth.authenticate(username, password)

            # Verify token request was made
            mock_token_client.post.assert_called_once_with(
                Config.AUTH_URL,
                data={
                    "client_id": Config.CLIENT_ID,
                    "client_secret": Config.CLIENT_SECRET,
                    "grant_type": "password",
                    "username": username,
                    "password": password,
                },
            )

            # Verify authenticated client was created
            mock_client_class.assert_called_with(
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=Config.HTTP_TIMEOUT,
            )

            assert client == mock_auth_client

    @pytest.mark.asyncio
    async def test_authenticate_token_request_failure(self):
        """Test authentication when token request fails."""
        username = "testuser"
        password = "testpass"

        with patch("dotenv.load_dotenv"), patch(
            "httpx.AsyncClient"
        ) as mock_client_class:
            # Mock the token request failure
            mock_token_client = AsyncMock()
            mock_token_client.post.side_effect = Exception("Token request failed")

            # Mock the context manager behavior
            mock_token_client.__aenter__.return_value = mock_token_client
            mock_token_client.__aexit__.return_value = None

            mock_client_class.return_value = mock_token_client

            auth = Authenticator(username=username, password=password)

            with pytest.raises(Exception, match="Token request failed"):
                await auth.authenticate(username, password)

    @pytest.mark.asyncio
    async def test_authenticate_invalid_response(self):
        """Test authentication with invalid token response."""
        username = "testuser"
        password = "testpass"

        mock_token_response = {"error": "invalid_grant"}

        with patch("dotenv.load_dotenv"), patch(
            "httpx.AsyncClient"
        ) as mock_client_class:
            # Mock the token request
            mock_token_client = AsyncMock()
            mock_token_response_obj = MagicMock()
            mock_token_response_obj.json.return_value = mock_token_response
            mock_token_response_obj.raise_for_status.return_value = None
            mock_token_client.post.return_value = mock_token_response_obj

            # Mock the context manager behavior
            mock_token_client.__aenter__.return_value = mock_token_client
            mock_token_client.__aexit__.return_value = None

            mock_client_class.return_value = mock_token_client

            auth = Authenticator(username=username, password=password)

            with pytest.raises(KeyError):
                await auth.authenticate(username, password)

    @pytest.mark.asyncio
    async def test_get_oauth2_token_success(self):
        """Test successful OAuth2 token retrieval."""
        username = "testuser"
        password = "testpass"
        access_token = "test_access_token"

        mock_token_response = {"access_token": access_token}

        with patch("dotenv.load_dotenv"), patch(
            "httpx.AsyncClient"
        ) as mock_client_class:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.json.return_value = mock_token_response
            mock_response.raise_for_status.return_value = None
            mock_client.post.return_value = mock_response

            mock_client_class.return_value.__aenter__.return_value = mock_client

            auth = Authenticator(username=username, password=password)
            token = await auth._get_oauth2_token(username, password)

            assert token == access_token

            # Verify the request was made correctly
            mock_client.post.assert_called_once_with(
                Config.AUTH_URL,
                data={
                    "client_id": Config.CLIENT_ID,
                    "client_secret": Config.CLIENT_SECRET,
                    "grant_type": "password",
                    "username": username,
                    "password": password,
                },
            )

    @pytest.mark.asyncio
    async def test_get_oauth2_token_http_error(self):
        """Test OAuth2 token retrieval with HTTP error."""
        username = "testuser"
        password = "testpass"

        with patch("dotenv.load_dotenv"), patch(
            "httpx.AsyncClient"
        ) as mock_client_class:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = Exception("HTTP 401")
            mock_client.post.return_value = mock_response

            mock_client_class.return_value.__aenter__.return_value = mock_client

            auth = Authenticator(username=username, password=password)

            with pytest.raises(Exception, match="HTTP 401"):
                await auth._get_oauth2_token(username, password)

    @pytest.mark.asyncio
    async def test_get_oauth2_token_missing_access_token(self):
        """Test OAuth2 token retrieval with missing access_token."""
        username = "testuser"
        password = "testpass"

        mock_token_response = {
            "error": "invalid_grant",
            "error_description": "Invalid credentials",
        }

        with patch("dotenv.load_dotenv"), patch(
            "httpx.AsyncClient"
        ) as mock_client_class:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.json.return_value = mock_token_response
            mock_response.raise_for_status.return_value = None
            mock_client.post.return_value = mock_response

            mock_client_class.return_value.__aenter__.return_value = mock_client

            auth = Authenticator(username=username, password=password)

            with pytest.raises(KeyError):
                await auth._get_oauth2_token(username, password)
