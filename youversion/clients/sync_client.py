"""Synchronous client for YouVersion Bible API."""

import asyncio
from typing import Any, Optional

from ..core.base_client import BaseClient


class SyncClient(BaseClient):
    """Synchronous wrapper for BaseClient."""

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        """Initialize sync client.

        Args:
            username: Username for authentication
            password: Password for authentication
        """
        # Call BaseClient.__init__ with explicit self for easier test patching
        BaseClient.__init__(self, username, password)
        # Preserve provided username for tests where BaseClient is mocked
        self._username = username
        self._loop = None
        self._loop_owner = False

    def _get_loop(self) -> asyncio.AbstractEventLoop:
        """Get or create an event loop for running async operations.

        Returns:
            Event loop for async operations

        Raises:
            RuntimeError: If called within an async context
        """
        try:
            # Try to get the current event loop
            asyncio.get_running_loop()
            # If we're already in an async context, we can't run sync operations
            raise RuntimeError(
                "Cannot use synchronous SyncClient within an async context. "
                "Use AsyncClient instead or run this code outside of an async function."
            )
        except RuntimeError as e:
            if "Cannot use synchronous SyncClient" in str(e):
                raise
            # No running loop, create a new one
            if self._loop is None or self._loop.is_closed():
                self._loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self._loop)
                self._loop_owner = True
            return self._loop

    def _run_async(self, coro):
        """Run an async coroutine in the event loop.

        Args:
            coro: Async coroutine to run

        Returns:
            Result of the coroutine
        """
        loop = self._get_loop()

        # Ensure the client is initialized
        async def _ensure_client_initialized():
            await self._ensure_authenticated()
            return await coro

        return loop.run_until_complete(_ensure_client_initialized())

    def __enter__(self):
        """Context manager entry."""
        self._run_async(self.__aenter__())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self._run_async(self.__aexit__(exc_type, exc_val, exc_tb))
        if self._loop_owner and self._loop and not self._loop.is_closed():
            self._loop.close()

    async def __aenter__(self):
        """Async context manager entry."""
        await self._ensure_authenticated()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await super().close()

    def close(self):
        """Manually close the client."""

        async def _close_async():
            await super().close()

        # Run close coroutine depending on loop ownership
        if self._loop and not self._loop.is_closed():
            self._loop.run_until_complete(_close_async())
        elif self._loop_owner:
            # Create and assign a loop we own
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._loop.run_until_complete(_close_async())
        else:
            # Create a temporary loop but do not close it (not owner)
            temp_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(temp_loop)
            temp_loop.run_until_complete(_close_async())

        # Close the stored loop only if we own it
        if self._loop_owner and self._loop and not self._loop.is_closed():
            self._loop.close()

    @property
    def username(self) -> Optional[str]:
        """Get the username, tolerant of BaseClient being mocked in tests."""
        auth = getattr(self, "_authenticator", None)
        if auth is not None and hasattr(auth, "username"):
            return auth.username
        return getattr(self, "_username", None)

    # Synchronous wrapper methods
    def moments(self, page: int = 1) -> list[Any]:
        """Get moments (synchronous)."""
        return self._run_async(super().moments(page))

    def highlights(self, page: int = 1) -> list[Any]:
        """Get highlights (synchronous)."""
        return self._run_async(super().highlights(page))

    def verse_of_the_day(self, day: Optional[int] = None) -> Any:
        """Get verse of the day (synchronous)."""
        return self._run_async(super().verse_of_the_day(day))

    def notes(self, page: int = 1) -> list[Any]:
        """Get notes (synchronous)."""
        return self._run_async(super().notes(page))

    def bookmarks(self, page: int = 1) -> list[Any]:
        """Get bookmarks (synchronous)."""
        return self._run_async(super().bookmarks(page))

    def my_images(self, page: int = 1) -> list[Any]:
        """Get images (synchronous)."""
        return self._run_async(super().my_images(page))

    def plan_progress(self, page: int = 1) -> list[Any]:
        """Get plan progress (synchronous)."""
        return self._run_async(super().plan_progress(page))

    def plan_subscriptions(self, page: int = 1) -> list[Any]:
        """Get plan subscriptions (synchronous)."""
        return self._run_async(super().plan_subscriptions(page))

    def convert_note_to_md(self) -> list[Any]:
        """Convert notes to markdown (synchronous)."""
        return self._run_async(super().convert_note_to_md())
