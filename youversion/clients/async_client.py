"""Asynchronous client for YouVersion Bible API."""

from typing import Optional

from ..core.base_client import BaseClient


class AsyncClient(BaseClient):
    """Asynchronous client for YouVersion Bible API."""

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        """Initialize async client.

        Args:
            username: Username for authentication
            password: Password for authentication
        """
        super().__init__(username, password)

    async def __aenter__(self):
        """Async context manager entry."""
        await self._ensure_authenticated()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
