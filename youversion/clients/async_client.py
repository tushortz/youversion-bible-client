"""Asynchronous client for YouVersion Bible API."""

from ..core.base_client import BaseClient


class AsyncClient(BaseClient):
    """Asynchronous client for YouVersion Bible API."""

    def __init__(self, username: str | None = None, password: str | None = None):
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
