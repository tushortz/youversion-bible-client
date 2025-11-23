"""Synchronous client for YouVersion Bible API."""

import asyncio
from typing import Any, Optional, Union

from ..core.base_client import BaseClient
from ..models.moments import CreateMoment


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
        """Get moments.

        Args:
            page: Page number

        Returns:
            List of dynamically created Moment objects conforming to
            MomentProtocol
        """
        return self._run_async(super().moments(page))

    def highlights(self, page: int = 1) -> list[Any]:
        """Get highlights.

        Args:
            page: Page number

        Returns:
            List of Highlight objects
        """
        return self._run_async(super().highlights(page))

    def verse_of_the_day(self, day: Optional[int] = None) -> Any:
        """Get verse of the day.

        Args:
            day: Specific day number (optional)

        Returns:
            Votd object
        """
        return self._run_async(super().verse_of_the_day(day))

    def notes(self, page: int = 1) -> list[Any]:
        """Get notes.

        Args:
            page: Page number

        Returns:
            List of note data
        """
        return self._run_async(super().notes(page))

    def bookmarks(self, page: int = 1) -> list[Any]:
        """Get bookmarks.

        Args:
            page: Page number

        Returns:
            List of bookmark data
        """
        return self._run_async(super().bookmarks(page))

    def my_images(self, page: int = 1) -> list[Any]:
        """Get images.

        Args:
            page: Page number

        Returns:
            List of image data
        """
        return self._run_async(super().my_images(page))

    def plan_progress(self, page: int = 1) -> list[Any]:
        """Get plan progress.

        Args:
            page: Page number

        Returns:
            List of plan progress data
        """
        return self._run_async(super().plan_progress(page))

    def plan_subscriptions(self, page: int = 1) -> list[Any]:
        """Get plan subscriptions.

        Args:
            page: Page number

        Returns:
            List of plan subscription data
        """
        return self._run_async(super().plan_subscriptions(page))

    def plan_completions(self, page: int = 1) -> list[Any]:
        """Get plan completions.

        Args:
            page: Page number

        Returns:
            List of plan completion data
        """
        return self._run_async(super().plan_completions(page))

    def convert_note_to_md(self) -> list[Any]:
        """Convert notes to markdown.

        Returns:
            List of converted note data
        """
        return self._run_async(super().convert_note_to_md())

    def send_friend_request(self, user_id: int) -> dict[str, Any]:
        """Send a friend request to a user.

        Args:
            user_id: User ID to send friend request to

        Returns:
            Friend request response data with incoming and outgoing lists
        """
        return self._run_async(super().send_friend_request(user_id))

    # Bible API methods
    def get_bible_configuration(self) -> dict[str, Any]:
        """Get Bible configuration.

        Returns:
            Bible configuration data
        """
        return self._run_async(super().get_bible_configuration())

    def get_bible_versions(
        self,
        language_tag: str = "eng",
        version_type: str = "all"
    ) -> dict[str, Any]:
        """Get Bible versions for a language.

        Args:
            language_tag: Language tag (e.g., 'eng', 'spa')
            version_type: Type of versions ('all', 'text', 'audio')

        Returns:
            Bible versions data
        """
        return self._run_async(
            super().get_bible_versions(language_tag, version_type)
        )

    def get_bible_version(self, version_id: int) -> dict[str, Any]:
        """Get specific Bible version details.

        Args:
            version_id: Version ID

        Returns:
            Bible version data
        """
        return self._run_async(
            super().get_bible_version(version_id)
        )

    def get_bible_chapter(
        self,
        reference: str,
        version_id: int = 1,
    ) -> dict[str, Any]:
        """Get Bible chapter content.

        Args:
            reference: USFM reference (e.g., 'GEN.1')
            version_id: Version ID

        Returns:
            Chapter content data
        """
        return self._run_async(
            super().get_bible_chapter(reference, version_id)
        )

    def get_recommended_languages(
        self, country: str = "US"
    ) -> dict[str, Any]:
        """Get recommended languages for a country.

        Args:
            country: Country code (e.g., 'US', 'CA')

        Returns:
            Recommended languages data
        """
        return self._run_async(
            super().get_recommended_languages(country)
        )

    # Audio Bible API methods
    def get_audio_chapter(
        self,
        reference: str,
        version_id: int = 1,
    ) -> dict[str, Any]:
        """Get audio chapter information.

        Args:
            reference: USFM reference (e.g., 'GEN.1')
            version_id: Audio version ID

        Returns:
            Audio chapter data
        """
        return self._run_async(
            super().get_audio_chapter(reference, version_id)
        )

    def get_audio_version(self, audio_id: int) -> dict[str, Any]:
        """Get audio version details.

        Args:
            audio_id: Audio version ID

        Returns:
            Audio version data
        """
        return self._run_async(super().get_audio_version(audio_id))

    # Search API methods
    def search_bible(
        self,
        query: str,
        version_id: Optional[int] = None,
        book: Optional[str] = None,
        page: int = 1
    ) -> dict[str, Any]:
        """Search Bible text.

        Args:
            query: Search query
            version_id: Version ID (optional)
            book: Book filter (optional)
            page: Page number

        Returns:
            Search results data
        """
        return self._run_async(
            super().search_bible(query, version_id, book, page)
        )

    def search_plans(
        self,
        query: str,
        language_tag: str = "en",
        page: int = 1
    ) -> dict[str, Any]:
        """Search reading plans.

        Args:
            query: Search query
            language_tag: Language tag
            page: Page number

        Returns:
            Plan search results data
        """
        return self._run_async(super().search_plans(query, language_tag, page))

    def search_users(
        self,
        query: str,
        language_tag: str = "eng",
        page: int = 1
    ) -> dict[str, Any]:
        """Search users.

        Args:
            query: Search query
            language_tag: Language tag
            page: Page number

        Returns:
            User search results data
        """
        return self._run_async(super().search_users(query, language_tag, page))

    # Videos API methods
    def get_videos(self, language_tag: str = "eng") -> dict[str, Any]:
        """Get videos list.

        Args:
            language_tag: Language tag

        Returns:
            Videos data
        """
        return self._run_async(super().get_videos(language_tag))

    def get_video_details(self, video_id: int) -> dict[str, Any]:
        """Get video details.

        Args:
            video_id: Video ID

        Returns:
            Video details data
        """
        return self._run_async(super().get_video_details(video_id))

    # Badges API methods
    def badges(self, page: int = 1) -> list[Any]:
        """Get badges.

        Args:
            page: Page number

        Returns:
            List of badge data
        """
        return self._run_async(super().badges(page))

    # Images API methods
    def get_images(
        self,
        reference: str,
        language_tag: str = "eng",
        page: int = 1
    ) -> dict[str, Any]:
        """Get images for a reference.

        Args:
            reference: USFM reference
            language_tag: Language tag
            page: Page number

        Returns:
            Images data
        """
        return self._run_async(
            super().get_images(reference, language_tag, page)
        )

    def get_image_upload_url(self) -> dict[str, Any]:
        """Get image upload URL and parameters.

        Returns:
            Upload URL data
        """
        return self._run_async(super().get_image_upload_url())

    # Events API methods
    def search_events(
        self,
        query: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        page: int = 1
    ) -> dict[str, Any]:
        """Search events.

        Args:
            query: Search query
            latitude: Latitude (optional)
            longitude: Longitude (optional)
            page: Page number

        Returns:
            Event search results data
        """
        return self._run_async(
            super().search_events(query, latitude, longitude, page)
        )

    def get_event_details(self, event_id: int) -> dict[str, Any]:
        """Get event details.

        Args:
            event_id: Event ID

        Returns:
            Event details data
        """
        return self._run_async(super().get_event_details(event_id))

    def get_saved_events(self, page: int = 1) -> dict[str, Any]:
        """Get saved events.

        Args:
            page: Page number

        Returns:
            Saved events data
        """
        return self._run_async(super().get_saved_events(page))

    def save_event(
        self,
        event_id: int,
        comments: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Save event.

        Args:
            event_id: Event ID
            comments: Comments (optional)

        Returns:
            Save result data
        """
        return self._run_async(super().save_event(event_id, comments))

    def delete_saved_event(self, event_id: int) -> dict[str, Any]:
        """Delete saved event.

        Args:
            event_id: Event ID

        Returns:
            Delete result data
        """
        return self._run_async(super().delete_saved_event(event_id))

    def get_all_saved_event_ids(self) -> dict[str, Any]:
        """Get all saved event IDs.

        Returns:
            All saved event IDs data
        """
        return self._run_async(super().get_all_saved_event_ids())

    def get_event_configuration(self) -> dict[str, Any]:
        """Get event configuration.

        Returns:
            Event configuration data
        """
        return self._run_async(super().get_event_configuration())

    # Moments API methods
    def get_moments(
        self,
        page: int = 1,
        user_id: Optional[int] = None,
        kind: Optional[str] = None,
        version_id: Optional[int] = None,
        usfm: Optional[str] = None
    ) -> dict[str, Any]:
        """Get moments list.

        Args:
            page: Page number
            user_id: User ID (optional)
            kind: Kind of moment (optional)
            version_id: Bible version ID (optional)
            usfm: USFM reference (optional)

        Returns:
            Moments data
        """
        return self._run_async(
            super().get_moments(page, user_id, kind, version_id, usfm)
        )

    def get_moment_details(self, moment_id: int) -> dict[str, Any]:
        """Get moment details.

        Args:
            moment_id: Moment ID

        Returns:
            Moment details data
        """
        return self._run_async(super().get_moment_details(moment_id))

    def create_moment(
        self, data: Union[CreateMoment, dict[str, Any]]
    ) -> dict[str, Any]:
        """Create a new moment.

        Args:
            data: Moment data as CreateMoment model or dict

        Returns:
            Created moment data
        """
        return self._run_async(super().create_moment(data))

    def update_moment(self, data: dict[str, Any]) -> dict[str, Any]:
        """Update an existing moment.

        Args:
            data: Moment data

        Returns:
            Updated moment data
        """
        return self._run_async(super().update_moment(data))

    def delete_moment(self, moment_id: int) -> dict[str, Any]:
        """Delete a moment.

        Args:
            moment_id: Moment ID

        Returns:
            Delete result data
        """
        return self._run_async(super().delete_moment(moment_id))

    def get_moment_colors(self) -> dict[str, Any]:
        """Get available highlight colors.

        Returns:
            Colors data
        """
        return self._run_async(super().get_moment_colors())

    def get_moment_labels(self) -> dict[str, Any]:
        """Get moment labels.

        Returns:
            Labels data
        """
        return self._run_async(super().get_moment_labels())

    def get_verse_colors(
        self,
        usfm: str,
        version_id: int
    ) -> dict[str, Any]:
        """Get verse highlight colors.

        Args:
            usfm: USFM reference
            version_id: Bible version ID

        Returns:
            Verse colors data
        """
        return self._run_async(super().get_verse_colors(usfm, version_id))

    def hide_verse_colors(self, data: dict[str, Any]) -> dict[str, Any]:
        """Hide verse highlight colors.

        Args:
            data: Hide colors data

        Returns:
            Hide result data
        """
        return self._run_async(super().hide_verse_colors(data))

    def get_moments_configuration(self) -> dict[str, Any]:
        """Get moments configuration.

        Returns:
            Moments configuration data
        """
        return self._run_async(super().get_moments_configuration())

    # Comments API methods
    def create_comment(
        self,
        moment_id: int,
        comment: str
    ) -> dict[str, Any]:
        """Create a comment on a moment.

        Args:
            moment_id: Moment ID
            comment: Comment text

        Returns:
            Created comment data
        """
        return self._run_async(super().create_comment(moment_id, comment))

    def delete_comment(self, comment_id: int) -> dict[str, Any]:
        """Delete a comment.

        Args:
            comment_id: Comment ID

        Returns:
            Delete result data
        """
        return self._run_async(super().delete_comment(comment_id))

    # Likes API methods
    def like_moment(self, moment_id: int) -> dict[str, Any]:
        """Like a moment.

        Args:
            moment_id: Moment ID

        Returns:
            Like result data
        """
        return self._run_async(super().like_moment(moment_id))

    def unlike_moment(self, moment_id: int) -> dict[str, Any]:
        """Unlike a moment.

        Args:
            moment_id: Moment ID

        Returns:
            Unlike result data
        """
        return self._run_async(super().unlike_moment(moment_id))

    # Messaging API methods
    def register_device(
        self,
        device_id: str,
        device_type: str = "android",
        user_id: Optional[int] = None,
        old_device_id: Optional[str] = None,
        tags: Optional[str] = None
    ) -> dict[str, Any]:
        """Register device for push notifications.

        Args:
            device_id: Device ID
            device_type: Device type
            user_id: User ID (optional)
            old_device_id: Previous device ID (optional)
            tags: Device tags (optional)

        Returns:
            Registration result data
        """
        return self._run_async(
            super().register_device(
                device_id, device_type, user_id, old_device_id, tags
            )
        )

    def unregister_device(self, device_id: str) -> dict[str, Any]:
        """Unregister device from push notifications.

        Args:
            device_id: Device ID

        Returns:
            Unregistration result data
        """
        return self._run_async(super().unregister_device(device_id))

    # Themes API methods
    def get_themes(
        self,
        page: int = 1,
        language_tag: str = "eng"
    ) -> dict[str, Any]:
        """Get available themes.

        Args:
            page: Page number
            language_tag: Language tag

        Returns:
            Themes data
        """
        return self._run_async(super().get_themes(page, language_tag))

    def add_theme(
        self,
        theme_id: int,
        available_locales: list[str],
        colors: dict[str, Any],
        cta_urls: dict[str, Any],
        msgid_suffix: str,
        version_ids: dict[str, int]
    ) -> dict[str, Any]:
        """Add a theme to user's collection.

        Args:
            theme_id: Theme ID
            available_locales: List of available locale codes
            colors: Theme colors dictionary
            cta_urls: Call-to-action URLs dictionary
            msgid_suffix: Message ID suffix
            version_ids: Dictionary of version IDs by locale code

        Returns:
            Add result data
        """
        return self._run_async(
            super().add_theme(
                theme_id,
                available_locales,
                colors,
                cta_urls,
                msgid_suffix,
                version_ids
            )
        )

    def remove_theme(self, theme_id: int) -> dict[str, Any]:
        """Remove a theme from user's collection.

        Args:
            theme_id: Theme ID

        Returns:
            Remove result data
        """
        return self._run_async(super().remove_theme(theme_id))

    def set_theme(
        self,
        theme_id: int,
        previous_theme_id: Optional[int] = None
    ) -> dict[str, Any]:
        """Set active theme.

        Args:
            theme_id: Theme ID
            previous_theme_id: Previous theme ID (optional)

        Returns:
            Set result data
        """
        return self._run_async(super().set_theme(theme_id, previous_theme_id))

    def get_theme_description(
        self,
        theme_id: int,
        language_tag: str = "eng"
    ) -> dict[str, Any]:
        """Get theme description.

        Args:
            theme_id: Theme ID
            language_tag: Language tag

        Returns:
            Theme description data
        """
        return self._run_async(
            super().get_theme_description(theme_id, language_tag)
        )

    # Localization API methods
    def get_localization_items(self, language_tag: str = "eng") -> str:
        """Get localization strings for a language.

        Args:
            language_tag: Language tag

        Returns:
            Localization strings (PO file format)
        """
        return self._run_async(super().get_localization_items(language_tag))
