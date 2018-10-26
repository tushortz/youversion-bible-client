"""Base client class implementing common functionality."""

from typing import Any, Dict, Optional

from ..enums import MomentKinds
from .authenticator import Authenticator
from .data_processor import DataProcessor
from .http_client import HttpClient
from .interfaces import IClient, IHttpClient


class BaseClient(IClient):
    """Base client implementing common API operations."""

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        """Initialize base client.

        Args:
            username: Username for authentication
            password: Password for authentication
        """
        self._authenticator = Authenticator(username, password)
        self._http_client: Optional[IHttpClient] = None
        self._data_processor = DataProcessor()

    async def _ensure_authenticated(self) -> None:
        """Ensure client is authenticated."""
        if self._http_client is None:
            client = await self._authenticator.authenticate(
                self._authenticator.username, self._authenticator.password
            )
            self._http_client = HttpClient(client)

    async def _get_cards_data(
        self, kind: str = "", page: int = 1
    ) -> list[dict[str, Any]]:
        """Get cards data from API.

        Args:
            kind: Kind of data to retrieve
            page: Page number

        Returns:
            Raw cards data
        """
        await self._ensure_authenticated()
        data = await self._http_client.get_cards(
            self._authenticator.username, page=page, kind=kind
        )
        return data

    async def moments(self, page: int = 1) -> list[Any]:
        """Get moments.

        Args:
            page: Page number

        Returns:
            List of Moment objects
        """
        raw_data = await self._get_cards_data(page=page)
        return self._data_processor.process_moments(raw_data)

    async def highlights(self, page: int = 1) -> list[Any]:
        """Get highlights.

        Args:
            page: Page number

        Returns:
            List of Highlight objects
        """
        raw_data = await self._get_cards_data(
            kind=MomentKinds.HIGHLIGHT.value, page=page
        )
        return self._data_processor.process_highlights(raw_data)

    async def verse_of_the_day(self, day: Optional[int] = None) -> Any:
        """Get verse of the day.

        Args:
            day: Specific day number (optional)

        Returns:
            Votd object
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_verse_of_the_day()
        return self._data_processor.process_verse_of_the_day(raw_data, day)

    async def notes(self, page: int = 1) -> list[Any]:
        """Get notes.

        Args:
            page: Page number

        Returns:
            List of note data
        """
        return await self._get_cards_data(kind=MomentKinds.NOTE.value, page=page)

    async def bookmarks(self, page: int = 1) -> list[Any]:
        """Get bookmarks.

        Args:
            page: Page number

        Returns:
            List of bookmark data
        """
        return await self._get_cards_data(kind=MomentKinds.BOOKMARK.value, page=page)

    async def my_images(self, page: int = 1) -> list[Any]:
        """Get images.

        Args:
            page: Page number

        Returns:
            List of image data
        """
        return await self._get_cards_data(kind=MomentKinds.IMAGE.value, page=page)

    async def plan_progress(self, page: int = 1) -> list[Any]:
        """Get plan progress.

        Args:
            page: Page number

        Returns:
            List of plan progress data
        """
        return await self._get_cards_data(
            kind=MomentKinds.PLAN_SEGMENT_COMPLETION.value, page=page
        )

    async def plan_subscriptions(self, page: int = 1) -> list[Any]:
        """Get plan subscriptions.

        Args:
            page: Page number

        Returns:
            List of plan subscription data
        """
        return await self._get_cards_data(
            kind=MomentKinds.PLAN_SUBSCRIPTION.value, page=page
        )

    async def convert_note_to_md(self) -> list[Any]:
        """Convert notes to markdown.

        Returns:
            List of converted note data
        """
        return await self.notes()

    async def close(self) -> None:
        """Close the client and cleanup resources."""
        if self._http_client:
            await self._http_client.close()

    @property
    def username(self) -> str:
        """Get the username."""
        return self._authenticator.username

    # Bible API methods
    async def get_bible_configuration(self) -> Dict[str, Any]:
        """Get Bible configuration.

        Returns:
            Bible configuration data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_bible_configuration()

    async def get_bible_versions(
        self,
        language_tag: str = "eng",
        version_type: str = "all"
    ) -> Dict[str, Any]:
        """Get Bible versions for a language.

        Args:
            language_tag: Language tag (e.g., 'eng', 'spa')
            version_type: Type of versions ('all', 'text', 'audio')

        Returns:
            Bible versions data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_bible_versions(language_tag, version_type)

    async def get_bible_version(self, version_id: int) -> Dict[str, Any]:
        """Get specific Bible version details.

        Args:
            version_id: Version ID

        Returns:
            Bible version data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_bible_version(version_id)

    async def get_bible_chapter(
        self,
        version_id: int,
        reference: str
    ) -> Dict[str, Any]:
        """Get Bible chapter content.

        Args:
            version_id: Version ID
            reference: USFM reference (e.g., 'GEN.1')

        Returns:
            Chapter content data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_bible_chapter(version_id, reference)

    async def get_recommended_languages(self, country: str = "US") -> Dict[str, Any]:
        """Get recommended languages for a country.

        Args:
            country: Country code (e.g., 'US', 'CA')

        Returns:
            Recommended languages data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_recommended_languages(country)

    # Audio Bible API methods
    async def get_audio_chapter(
        self,
        version_id: int,
        reference: str
    ) -> Dict[str, Any]:
        """Get audio chapter information.

        Args:
            version_id: Audio version ID
            reference: USFM reference (e.g., 'GEN.1')

        Returns:
            Audio chapter data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_audio_chapter(version_id, reference)

    async def get_audio_version(self, audio_id: int) -> Dict[str, Any]:
        """Get audio version details.

        Args:
            audio_id: Audio version ID

        Returns:
            Audio version data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_audio_version(audio_id)

    # Search API methods
    async def search_bible(
        self,
        query: str,
        version_id: Optional[int] = None,
        book: Optional[str] = None,
        page: int = 1
    ) -> Dict[str, Any]:
        """Search Bible text.

        Args:
            query: Search query
            version_id: Version ID (optional)
            book: Book filter (optional)
            page: Page number

        Returns:
            Search results data
        """
        await self._ensure_authenticated()
        return await self._http_client.search_bible(query, version_id, book, page)

    async def search_plans(
        self,
        query: str,
        language_tag: str = "eng",
        page: int = 1
    ) -> Dict[str, Any]:
        """Search reading plans.

        Args:
            query: Search query
            language_tag: Language tag
            page: Page number

        Returns:
            Plan search results data
        """
        await self._ensure_authenticated()
        return await self._http_client.search_plans(query, language_tag, page)

    async def search_users(
        self,
        query: str,
        language_tag: str = "eng",
        page: int = 1
    ) -> Dict[str, Any]:
        """Search users.

        Args:
            query: Search query
            language_tag: Language tag
            page: Page number

        Returns:
            User search results data
        """
        await self._ensure_authenticated()
        return await self._http_client.search_users(query, language_tag, page)

    # Videos API methods
    async def get_videos(self, language_tag: str = "eng") -> Dict[str, Any]:
        """Get videos list.

        Args:
            language_tag: Language tag

        Returns:
            Videos data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_videos(language_tag)

    async def get_video_details(self, video_id: int) -> Dict[str, Any]:
        """Get video details.

        Args:
            video_id: Video ID

        Returns:
            Video details data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_video_details(video_id)

    # Badges API methods
    async def get_badges(self, user_id: int, page: int = 1) -> Dict[str, Any]:
        """Get user badges.

        Args:
            user_id: User ID
            page: Page number

        Returns:
            Badges data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_badges(user_id, page)

    # Images API methods
    async def get_images(
        self,
        reference: str,
        language_tag: str = "eng",
        page: int = 1
    ) -> Dict[str, Any]:
        """Get images for a reference.

        Args:
            reference: USFM reference
            language_tag: Language tag
            page: Page number

        Returns:
            Images data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_images(reference, language_tag, page)

    async def get_image_upload_url(self) -> Dict[str, Any]:
        """Get image upload URL and parameters.

        Returns:
            Upload URL data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_image_upload_url()

    # Events API methods
    async def search_events(
        self,
        query: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        page: int = 1
    ) -> Dict[str, Any]:
        """Search events.

        Args:
            query: Search query
            latitude: Latitude (optional)
            longitude: Longitude (optional)
            page: Page number

        Returns:
            Event search results data
        """
        await self._ensure_authenticated()
        return await self._http_client.search_events(query, latitude, longitude, page)

    async def get_event_details(self, event_id: int) -> Dict[str, Any]:
        """Get event details.

        Args:
            event_id: Event ID

        Returns:
            Event details data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_event_details(event_id)

    async def get_saved_events(self, page: int = 1) -> Dict[str, Any]:
        """Get saved events.

        Args:
            page: Page number

        Returns:
            Saved events data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_saved_events(page)

    async def save_event(
        self,
        event_id: int,
        comments: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Save event.

        Args:
            event_id: Event ID
            comments: Comments (optional)

        Returns:
            Save result data
        """
        await self._ensure_authenticated()
        return await self._http_client.save_event(event_id, comments)

    async def delete_saved_event(self, event_id: int) -> Dict[str, Any]:
        """Delete saved event.

        Args:
            event_id: Event ID

        Returns:
            Delete result data
        """
        await self._ensure_authenticated()
        return await self._http_client.delete_saved_event(event_id)

    async def get_all_saved_event_ids(self) -> Dict[str, Any]:
        """Get all saved event IDs.

        Returns:
            All saved event IDs data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_all_saved_event_ids()

    async def get_event_configuration(self) -> Dict[str, Any]:
        """Get event configuration.

        Returns:
            Event configuration data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_event_configuration()

    # Moments API methods
    async def get_moments(
        self,
        page: int = 1,
        user_id: Optional[int] = None,
        kind: Optional[str] = None,
        version_id: Optional[int] = None,
        usfm: Optional[str] = None
    ) -> Dict[str, Any]:
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
        await self._ensure_authenticated()
        return await self._http_client.get_moments(page, user_id, kind, version_id, usfm)

    async def get_moment_details(self, moment_id: int) -> Dict[str, Any]:
        """Get moment details.

        Args:
            moment_id: Moment ID

        Returns:
            Moment details data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_moment_details(moment_id)

    async def create_moment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new moment.

        Args:
            data: Moment data

        Returns:
            Created moment data
        """
        await self._ensure_authenticated()
        return await self._http_client.create_moment(data)

    async def update_moment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing moment.

        Args:
            data: Moment data

        Returns:
            Updated moment data
        """
        await self._ensure_authenticated()
        return await self._http_client.update_moment(data)

    async def delete_moment(self, moment_id: int) -> Dict[str, Any]:
        """Delete a moment.

        Args:
            moment_id: Moment ID

        Returns:
            Delete result data
        """
        await self._ensure_authenticated()
        return await self._http_client.delete_moment(moment_id)

    async def get_moment_colors(self) -> Dict[str, Any]:
        """Get available highlight colors.

        Returns:
            Colors data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_moment_colors()

    async def get_moment_labels(self) -> Dict[str, Any]:
        """Get moment labels.

        Returns:
            Labels data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_moment_labels()

    async def get_verse_colors(
        self,
        usfm: str,
        version_id: int
    ) -> Dict[str, Any]:
        """Get verse highlight colors.

        Args:
            usfm: USFM reference
            version_id: Bible version ID

        Returns:
            Verse colors data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_verse_colors(usfm, version_id)

    async def hide_verse_colors(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Hide verse highlight colors.

        Args:
            data: Hide colors data

        Returns:
            Hide result data
        """
        await self._ensure_authenticated()
        return await self._http_client.hide_verse_colors(data)

    async def get_verse_of_the_day_new(
        self,
        language_tag: str = "eng"
    ) -> Dict[str, Any]:
        """Get verse of the day (new API).

        Args:
            language_tag: Language tag

        Returns:
            Verse of the day data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_verse_of_the_day_new(language_tag)

    async def get_moments_configuration(self) -> Dict[str, Any]:
        """Get moments configuration.

        Returns:
            Moments configuration data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_moments_configuration()

    # Comments API methods
    async def create_comment(
        self,
        moment_id: int,
        comment: str
    ) -> Dict[str, Any]:
        """Create a comment on a moment.

        Args:
            moment_id: Moment ID
            comment: Comment text

        Returns:
            Created comment data
        """
        await self._ensure_authenticated()
        return await self._http_client.create_comment(moment_id, comment)

    async def delete_comment(self, comment_id: int) -> Dict[str, Any]:
        """Delete a comment.

        Args:
            comment_id: Comment ID

        Returns:
            Delete result data
        """
        await self._ensure_authenticated()
        return await self._http_client.delete_comment(comment_id)

    # Likes API methods
    async def like_moment(self, moment_id: int) -> Dict[str, Any]:
        """Like a moment.

        Args:
            moment_id: Moment ID

        Returns:
            Like result data
        """
        await self._ensure_authenticated()
        return await self._http_client.like_moment(moment_id)

    async def unlike_moment(self, moment_id: int) -> Dict[str, Any]:
        """Unlike a moment.

        Args:
            moment_id: Moment ID

        Returns:
            Unlike result data
        """
        await self._ensure_authenticated()
        return await self._http_client.unlike_moment(moment_id)

    # Messaging API methods
    async def register_device(
        self,
        device_id: str,
        device_type: str = "android",
        user_id: Optional[int] = None,
        old_device_id: Optional[str] = None,
        tags: Optional[str] = None
    ) -> Dict[str, Any]:
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
        await self._ensure_authenticated()
        return await self._http_client.register_device(
            device_id, device_type, user_id, old_device_id, tags
        )

    async def unregister_device(self, device_id: str) -> Dict[str, Any]:
        """Unregister device from push notifications.

        Args:
            device_id: Device ID

        Returns:
            Unregistration result data
        """
        await self._ensure_authenticated()
        return await self._http_client.unregister_device(device_id)

    # Themes API methods
    async def get_themes(
        self,
        page: int = 1,
        language_tag: str = "eng"
    ) -> Dict[str, Any]:
        """Get available themes.

        Args:
            page: Page number
            language_tag: Language tag

        Returns:
            Themes data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_themes(page, language_tag)

    async def add_theme(self, theme_id: int) -> Dict[str, Any]:
        """Add a theme to user's collection.

        Args:
            theme_id: Theme ID

        Returns:
            Add result data
        """
        await self._ensure_authenticated()
        return await self._http_client.add_theme(theme_id)

    async def remove_theme(self, theme_id: int) -> Dict[str, Any]:
        """Remove a theme from user's collection.

        Args:
            theme_id: Theme ID

        Returns:
            Remove result data
        """
        await self._ensure_authenticated()
        return await self._http_client.remove_theme(theme_id)

    async def set_theme(
        self,
        theme_id: int,
        previous_theme_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Set active theme.

        Args:
            theme_id: Theme ID
            previous_theme_id: Previous theme ID (optional)

        Returns:
            Set result data
        """
        await self._ensure_authenticated()
        return await self._http_client.set_theme(theme_id, previous_theme_id)

    async def get_theme_description(
        self,
        theme_id: int,
        language_tag: str = "eng"
    ) -> Dict[str, Any]:
        """Get theme description.

        Args:
            theme_id: Theme ID
            language_tag: Language tag

        Returns:
            Theme description data
        """
        await self._ensure_authenticated()
        return await self._http_client.get_theme_description(theme_id, language_tag)

    # Localization API methods
    async def get_localization_items(self, language_tag: str = "eng") -> str:
        """Get localization strings for a language.

        Args:
            language_tag: Language tag

        Returns:
            Localization strings (PO file format)
        """
        await self._ensure_authenticated()
        return await self._http_client.get_localization_items(language_tag)
