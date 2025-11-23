"""Interfaces for YouVersion Bible API client components."""

from abc import ABC, abstractmethod
from typing import Any, Optional, Union

import httpx

from ..models.base import Moment


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
        """Perform GET request.

        Args:
            url: URL to request
            **kwargs: Additional arguments for the request
        """
        pass

    @abstractmethod
    async def post(self, url: str, **kwargs) -> dict[str, Any]:
        """Perform POST request.

        Args:
            url: URL to request
            **kwargs: Additional arguments for the request
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """Close the HTTP client."""
        pass


class IDataProcessor(ABC):
    """Interface for data processing operations."""

    @abstractmethod
    def process_moments(self, raw_data: list[dict[str, Any]]) -> list[Moment]:
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

    @abstractmethod
    def process_bible_version(self, raw_data: dict[str, Any]) -> Any:
        """Process raw Bible version data."""
        pass

    @abstractmethod
    def process_bible_versions(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw Bible versions data."""
        pass

    @abstractmethod
    def process_bible_chapter(self, raw_data: dict[str, Any]) -> Any:
        """Process raw Bible chapter data."""
        pass

    @abstractmethod
    def process_audio_chapter(
        self, raw_data: Union[dict[str, Any], list[dict[str, Any]]]
    ) -> Any:
        """Process raw audio chapter data."""
        pass

    @abstractmethod
    def process_audio_version(self, raw_data: dict[str, Any]) -> Any:
        """Process raw audio version data."""
        pass

    @abstractmethod
    def process_bible_configuration(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw Bible configuration data."""
        pass

    @abstractmethod
    def process_recommended_languages(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw recommended languages data."""
        pass

    @abstractmethod
    def process_search_plans(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw plan search results data."""
        pass

    @abstractmethod
    def process_search_users(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw user search results data."""
        pass

    @abstractmethod
    def process_videos(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw videos data."""
        pass

    @abstractmethod
    def process_video_details(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw video details data."""
        pass

    @abstractmethod
    def process_image_upload_url(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw image upload URL data."""
        pass

    @abstractmethod
    def process_search_events(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw event search results data."""
        pass

    @abstractmethod
    def process_event_details(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw event details data."""
        pass

    @abstractmethod
    def process_saved_events(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw saved events data."""
        pass

    @abstractmethod
    def process_moments_list(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw moments list data."""
        pass

    @abstractmethod
    def process_moment_details(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw moment details data."""
        pass

    @abstractmethod
    def process_moment_colors(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw moment colors data."""
        pass

    @abstractmethod
    def process_moment_labels(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw moment labels data."""
        pass

    @abstractmethod
    def process_verse_colors(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw verse colors data."""
        pass

    @abstractmethod
    def process_moments_configuration(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw moments configuration data."""
        pass

    @abstractmethod
    def process_themes(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw themes data."""
        pass

    @abstractmethod
    def process_theme_description(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw theme description data."""
        pass

    @abstractmethod
    def process_event_configuration(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw event configuration data."""
        pass

    @abstractmethod
    def process_all_saved_event_ids(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw all saved event IDs data."""
        pass


class IClient(ABC):
    """Interface for YouVersion API client."""

    @property
    @abstractmethod
    def user_id(self) -> Optional[int]:
        """Get the authenticated user ID."""
        pass

    @abstractmethod
    async def moments(self, page: int = 1) -> list[Moment]:
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
    async def plan_completions(self, page: int = 1) -> list[Any]:
        """Get plan completions."""
        pass

    @abstractmethod
    async def convert_note_to_md(self) -> list[Any]:
        """Convert notes to markdown."""
        pass

    @abstractmethod
    async def send_friend_request(self, user_id: int) -> dict[str, Any]:
        """Send a friend request to a user."""
        pass
