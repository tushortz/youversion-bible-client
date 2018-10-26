"""Authentication handler for YouVersion API."""

import os
from typing import Optional

import httpx
from dotenv import load_dotenv

from ..config import Config
from .interfaces import IAuthenticator


class Authenticator(IAuthenticator):
    """Handles authentication for YouVersion API using OAuth2."""

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        """Initialize authenticator with credentials.

        Args:
            username: Username for authentication
            password: Password for authentication
        """
        load_dotenv()

        self.username = username or os.getenv("YOUVERSION_USERNAME")
        self.password = password or os.getenv("YOUVERSION_PASSWORD")

        if not self.username or not self.password:
            raise ValueError(
                "Username and password must be provided either as arguments "
                "or as YOUVERSION_USERNAME and YOUVERSION_PASSWORD environment variables"
            )

    async def authenticate(self, username: str, password: str) -> httpx.AsyncClient:
        """Authenticate using OAuth2 and return an HTTP client with Bearer token.

        Args:
            username: Username for authentication
            password: Password for authentication

        Returns:
            Authenticated httpx.AsyncClient with Bearer token
        """
        # Get OAuth2 token
        token = await self._get_oauth2_token(username, password)

        # Create HTTP client with Bearer token
        client = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {token}"}, timeout=Config.HTTP_TIMEOUT
        )

        return client

    async def _get_oauth2_token(self, username: str, password: str) -> str:
        """Get OAuth2 access token from YouVersion API.

        Args:
            username: Username for authentication
            password: Password for authentication

        Returns:
            OAuth2 access token

        Raises:
            httpx.HTTPStatusError: If authentication fails
        """
        async with httpx.AsyncClient(timeout=Config.HTTP_TIMEOUT) as client:
            response = await client.post(
                Config.AUTH_URL,
                data={
                    "client_id": Config.CLIENT_ID,
                    "client_secret": Config.CLIENT_SECRET,
                    "grant_type": "password",
                    "username": username,
                    "password": password,
                },
            )
            response.raise_for_status()
            token_data = response.json()
            if hasattr(token_data, "__await__"):
                token_data = await token_data
            return token_data["access_token"]
