"""Interfaces for YouVersion Bible API client components."""

from abc import ABC, abstractmethod
from typing import Any, Optional

import httpx


class IAuthenticator(ABC):
    """Interface for authentication handling."""

    @abstractmethod
    async def authenticate(self, username: str, password: str) -> httpx.AsyncClient:
        """Authenticate and return an HTTP client."""
        pass


class IHttpClient(ABC):
    """Interface for HTTP operations."""

    @abstractmethod
    async def get(self, url: str, **kwargs) -> dict[str, Any]:
        """Perform GET request."""
        pass

    @abstractmethod
    async def post(self, url: str, **kwargs) -> dict[str, Any]:
        """Perform POST request."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Close the HTTP client."""
        pass


class IDataProcessor(ABC):
    """Interface for data processing operations."""

    @abstractmethod
    def process_moments(self, raw_data: list[dict[str, Any]]) -> list[Any]:
        """Process raw moments data."""
        pass

    @abstractmethod
    def process_highlights(self, raw_data: list[dict[str, Any]]) -> list[Any]:
        """Process raw highlights data."""
        pass

    @abstractmethod
    def process_verse_of_the_day(
        self, raw_data: dict[str, Any], day: Optional[int] = None
    ) -> Any:
        """Process verse of the day data."""
        pass


class IClient(ABC):
    """Interface for YouVersion API client."""

    @property
    @abstractmethod
    def user_id(self) -> Optional[int]:
        """Get the authenticated user ID."""
        pass

    @abstractmethod
    async def moments(self, page: int = 1) -> list[Any]:
        """Get moments."""
        pass

    @abstractmethod
    async def highlights(self, page: int = 1) -> list[Any]:
        """Get highlights."""
        pass

    @abstractmethod
    async def verse_of_the_day(self, day: Optional[int] = None) -> Any:
        """Get verse of the day."""
        pass

    @abstractmethod
    async def notes(self, page: int = 1) -> list[Any]:
        """Get notes."""
        pass

    @abstractmethod
    async def bookmarks(self, page: int = 1) -> list[Any]:
        """Get bookmarks."""
        pass

    @abstractmethod
    async def my_images(self, page: int = 1) -> list[Any]:
        """Get images."""
        pass

    @abstractmethod
    async def plan_progress(self, page: int = 1) -> list[Any]:
        """Get plan progress."""
        pass

    @abstractmethod
    async def plan_subscriptions(self, page: int = 1) -> list[Any]:
        """Get plan subscriptions."""
        pass

    @abstractmethod
    async def convert_note_to_md(self) -> list[Any]:
        """Convert notes to markdown."""
        pass
