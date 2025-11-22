"""Synchronous client for YouVersion Bible API."""

import asyncio
from typing import Any, Dict, Optional

from ..core.base_client import BaseClient


class SyncClient(BaseClient):
    """Synchronous wrapper for BaseClient."""

    def __init__(
        self, username: Optional[str] = None, password: Optional[str] = None
    ):
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
            # If we're already in an async context, we can't run sync ops
            raise RuntimeError(
                "Cannot use synchronous SyncClient within an async context. "
                "Use AsyncClient instead or run this code outside of an "
                "async function."
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

    # Bible API methods
    def get_bible_configuration(self) -> Dict[str, Any]:
        """Get Bible configuration (synchronous)."""
        return self._run_async(super().get_bible_configuration())

    def get_bible_versions(
        self,
        language_tag: str = "eng",
        version_type: str = "all"
    ) -> Dict[str, Any]:
        """Get Bible versions for a language (synchronous)."""
        return self._run_async(
            super().get_bible_versions(language_tag, version_type)
        )

    def get_bible_version(self, version_id: int) -> Dict[str, Any]:
        """Get specific Bible version details (synchronous)."""
        return self._run_async(
            super().get_bible_version(version_id)
        )

    def get_bible_chapter(
        self,
        version_id: int,
        reference: str
    ) -> Dict[str, Any]:
        """Get Bible chapter content (synchronous)."""
        return self._run_async(
            super().get_bible_chapter(version_id, reference)
        )

    def get_recommended_languages(
        self, country: str = "US"
    ) -> Dict[str, Any]:
        """Get recommended languages for a country (synchronous)."""
        return self._run_async(
            super().get_recommended_languages(country)
        )

    # Audio Bible API methods
    def get_audio_chapter(
        self,
        version_id: int,
        reference: str
    ) -> Dict[str, Any]:
        """Get audio chapter information (synchronous)."""
        return self._run_async(
            super().get_audio_chapter(version_id, reference)
        )

    def get_audio_version(self, audio_id: int) -> Dict[str, Any]:
        """Get audio version details (synchronous)."""
        return self._run_async(super().get_audio_version(audio_id))

    # Search API methods
    def search_bible(
        self,
        query: str,
        version_id: Optional[int] = None,
        book: Optional[str] = None,
        page: int = 1
    ) -> Dict[str, Any]:
        """Search Bible text (synchronous)."""
        return self._run_async(
            super().search_bible(query, version_id, book, page)
        )

    def search_plans(
        self,
        query: str,
        language_tag: str = "eng",
        page: int = 1
    ) -> Dict[str, Any]:
        """Search reading plans (synchronous)."""
        return self._run_async(super().search_plans(query, language_tag, page))

    def search_users(
        self,
        query: str,
        language_tag: str = "eng",
        page: int = 1
    ) -> Dict[str, Any]:
        """Search users (synchronous)."""
        return self._run_async(super().search_users(query, language_tag, page))

    # Videos API methods
    def get_videos(self, language_tag: str = "eng") -> Dict[str, Any]:
        """Get videos list (synchronous)."""
        return self._run_async(super().get_videos(language_tag))

    def get_video_details(self, video_id: int) -> Dict[str, Any]:
        """Get video details (synchronous)."""
        return self._run_async(super().get_video_details(video_id))

    # Badges API methods
    def get_badges(self, user_id: int, page: int = 1) -> Dict[str, Any]:
        """Get user badges (synchronous)."""
        return self._run_async(super().get_badges(user_id, page))

    # Images API methods
    def get_images(
        self,
        reference: str,
        language_tag: str = "eng",
        page: int = 1
    ) -> Dict[str, Any]:
        """Get images for a reference (synchronous)."""
        return self._run_async(
            super().get_images(reference, language_tag, page)
        )

    def get_image_upload_url(self) -> Dict[str, Any]:
        """Get image upload URL and parameters (synchronous)."""
        return self._run_async(super().get_image_upload_url())

    # Events API methods
    def search_events(
        self,
        query: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        page: int = 1
    ) -> Dict[str, Any]:
        """Search events (synchronous)."""
        return self._run_async(
            super().search_events(query, latitude, longitude, page)
        )

    def get_event_details(self, event_id: int) -> Dict[str, Any]:
        """Get event details (synchronous)."""
        return self._run_async(super().get_event_details(event_id))

    def get_saved_events(self, page: int = 1) -> Dict[str, Any]:
        """Get saved events (synchronous)."""
        return self._run_async(super().get_saved_events(page))

    def save_event(
        self,
        event_id: int,
        comments: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Save event (synchronous)."""
        return self._run_async(super().save_event(event_id, comments))

    def delete_saved_event(self, event_id: int) -> Dict[str, Any]:
        """Delete saved event (synchronous)."""
        return self._run_async(super().delete_saved_event(event_id))

    def get_all_saved_event_ids(self) -> Dict[str, Any]:
        """Get all saved event IDs (synchronous)."""
        return self._run_async(super().get_all_saved_event_ids())

    def get_event_configuration(self) -> Dict[str, Any]:
        """Get event configuration (synchronous)."""
        return self._run_async(super().get_event_configuration())

    # Moments API methods
    def get_moments(
        self,
        page: int = 1,
        user_id: Optional[int] = None,
        kind: Optional[str] = None,
        version_id: Optional[int] = None,
        usfm: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get moments list (synchronous)."""
        return self._run_async(
            super().get_moments(page, user_id, kind, version_id, usfm)
        )

    def get_moment_details(self, moment_id: int) -> Dict[str, Any]:
        """Get moment details (synchronous)."""
        return self._run_async(super().get_moment_details(moment_id))

    def create_moment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new moment (synchronous)."""
        return self._run_async(super().create_moment(data))

    def update_moment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing moment (synchronous)."""
        return self._run_async(super().update_moment(data))

    def delete_moment(self, moment_id: int) -> Dict[str, Any]:
        """Delete a moment (synchronous)."""
        return self._run_async(super().delete_moment(moment_id))

    def get_moment_colors(self) -> Dict[str, Any]:
        """Get available highlight colors (synchronous)."""
        return self._run_async(super().get_moment_colors())

    def get_moment_labels(self) -> Dict[str, Any]:
        """Get moment labels (synchronous)."""
        return self._run_async(super().get_moment_labels())

    def get_verse_colors(
        self,
        usfm: str,
        version_id: int
    ) -> Dict[str, Any]:
        """Get verse highlight colors (synchronous)."""
        return self._run_async(super().get_verse_colors(usfm, version_id))

    def hide_verse_colors(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Hide verse highlight colors (synchronous)."""
        return self._run_async(super().hide_verse_colors(data))

    def get_verse_of_the_day_new(
        self,
        language_tag: str = "eng"
    ) -> Dict[str, Any]:
        """Get verse of the day (new API) (synchronous)."""
        return self._run_async(super().get_verse_of_the_day_new(language_tag))

    def get_moments_configuration(self) -> Dict[str, Any]:
        """Get moments configuration (synchronous)."""
        return self._run_async(super().get_moments_configuration())

    # Comments API methods
    def create_comment(
        self,
        moment_id: int,
        comment: str
    ) -> Dict[str, Any]:
        """Create a comment on a moment (synchronous)."""
        return self._run_async(super().create_comment(moment_id, comment))

    def delete_comment(self, comment_id: int) -> Dict[str, Any]:
        """Delete a comment (synchronous)."""
        return self._run_async(super().delete_comment(comment_id))

    # Likes API methods
    def like_moment(self, moment_id: int) -> Dict[str, Any]:
        """Like a moment (synchronous)."""
        return self._run_async(super().like_moment(moment_id))

    def unlike_moment(self, moment_id: int) -> Dict[str, Any]:
        """Unlike a moment (synchronous)."""
        return self._run_async(super().unlike_moment(moment_id))

    # Messaging API methods
    def register_device(
        self,
        device_id: str,
        device_type: str = "android",
        user_id: Optional[int] = None,
        old_device_id: Optional[str] = None,
        tags: Optional[str] = None
    ) -> Dict[str, Any]:
        """Register device for push notifications (synchronous)."""
        return self._run_async(
            super().register_device(
                device_id, device_type, user_id, old_device_id, tags
            )
        )

    def unregister_device(self, device_id: str) -> Dict[str, Any]:
        """Unregister device from push notifications (synchronous)."""
        return self._run_async(super().unregister_device(device_id))

    # Themes API methods
    def get_themes(
        self,
        page: int = 1,
        language_tag: str = "eng"
    ) -> Dict[str, Any]:
        """Get available themes (synchronous)."""
        return self._run_async(super().get_themes(page, language_tag))

    def add_theme(self, theme_id: int) -> Dict[str, Any]:
        """Add a theme to user's collection (synchronous)."""
        return self._run_async(super().add_theme(theme_id))

    def remove_theme(self, theme_id: int) -> Dict[str, Any]:
        """Remove a theme from user's collection (synchronous)."""
        return self._run_async(super().remove_theme(theme_id))

    def set_theme(
        self,
        theme_id: int,
        previous_theme_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Set active theme (synchronous)."""
        return self._run_async(super().set_theme(theme_id, previous_theme_id))

    def get_theme_description(
        self,
        theme_id: int,
        language_tag: str = "eng"
    ) -> Dict[str, Any]:
        """Get theme description (synchronous)."""
        return self._run_async(
            super().get_theme_description(theme_id, language_tag)
        )

    # Localization API methods
    def get_localization_items(self, language_tag: str = "eng") -> str:
        """Get localization strings for a language (synchronous)."""
        return self._run_async(super().get_localization_items(language_tag))
