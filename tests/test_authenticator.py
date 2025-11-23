"""Unit tests for Authenticator class."""

import os
from unittest.mock import patch

import pytest

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
