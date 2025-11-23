"""Base client class implementing common functionality."""

from datetime import datetime, timezone
from typing import Any, Optional, Union

from ..enums import MomentKinds
from ..models.base import Moment
from ..models.moments import CreateMoment
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
        self._user_id = None
        self._access_token = None

    async def _ensure_authenticated(self) -> None:
        """Ensure client is authenticated."""
        if self._http_client is None:
            client = await self._authenticator.authenticate(
                self._authenticator.username, self._authenticator.password
            )
            self._user_id = self._authenticator.user_id
            self._access_token = self._authenticator.access_token
            self._http_client = HttpClient(client, user_id=self._user_id)

    async def _get_cards_data(
        self, kind: str = "", page: int = 1
    ) -> list[dict[str, Any]]:
        """Get cards data from API.

        Args:
            kind: Kind of data to retrieve
            page: Page number

        Returns:
            Raw cards data (list of moments)
        """
        await self._ensure_authenticated()
        data = await self._http_client.get_cards(page=page, kind=kind)

        # Extract moments array from response structure
        if "response" not in data:
            return data

        moments_data = data.get("response", {}).get("data", {}).get("moments", [])
        return moments_data

    async def moments(self, page: int = 1) -> list[Moment]:
        """Get moments.

        Args:
            page: Page number

        Returns:
            List of dynamically created Moment objects conforming to
            MomentProtocol
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_cards(page=page, kind="")
        # Extract moments array from response structure
        moments_data = raw_data.get("moments", [])
        return self._data_processor.process_moments(moments_data)

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
        raw_data = raw_data.get("moments", [])
        return self._data_processor.process_highlights(raw_data)

    async def verse_of_the_day(self, day: Optional[int] = None) -> Any:
        """Get verse of the day.

        Args:
            day: Specific day number (optional)

        Returns:
            Votd object
        """
        raw_data = await self._http_client.get_verse_of_the_day()
        return self._data_processor.process_verse_of_the_day(raw_data, day)

    async def notes(self, page: int = 1) -> list[Any]:
        """Get notes.

        Args:
            page: Page number

        Returns:
            List of note data
        """
        raw_data = await self._get_cards_data(kind=MomentKinds.NOTE.value, page=page)
        raw_data = raw_data.get("moments", [])
        return self._data_processor.process_notes(raw_data)

    async def bookmarks(self, page: int = 1) -> list[Any]:
        """Get bookmarks.

        Args:
            page: Page number

        Returns:
            List of bookmark data
        """
        raw_data = await self._get_cards_data(
            kind=MomentKinds.BOOKMARK.value, page=page
        )
        raw_data = raw_data.get("moments", [])
        return self._data_processor.process_bookmarks(raw_data)

    async def my_images(self, page: int = 1) -> list[Any]:
        """Get images.

        Args:
            page: Page number

        Returns:
            List of image data
        """
        raw_data = await self._get_cards_data(kind=MomentKinds.IMAGE.value, page=page)
        raw_data = raw_data.get("moments", [])
        return self._data_processor.process_images(raw_data)

    async def plan_progress(self, page: int = 1) -> list[Any]:
        """Get plan progress.

        Args:
            page: Page number

        Returns:
            List of plan progress data
        """
        raw_data = await self._get_cards_data(
            kind=MomentKinds.PLAN_SEGMENT_COMPLETION.value, page=page
        )
        raw_data = raw_data.get("moments", [])
        return self._data_processor.process_plan_progress(raw_data)

    async def plan_subscriptions(self, page: int = 1) -> list[Any]:
        """Get plan subscriptions.

        Args:
            page: Page number

        Returns:
            List of plan subscription data
        """
        raw_data = await self._get_cards_data(
            kind=MomentKinds.PLAN_SUBSCRIPTION.value, page=page
        )
        raw_data = raw_data.get("moments", [])
        return self._data_processor.process_plan_subscriptions(raw_data)

    async def plan_completions(self, page: int = 1) -> list[Any]:
        """Get plan completions.

        Args:
            page: Page number

        Returns:
            List of plan completion data
        """
        raw_data = await self._get_cards_data(
            kind=MomentKinds.PLAN_COMPLETION.value, page=page
        )
        raw_data = raw_data.get("moments", [])
        return self._data_processor.process_plan_completions(raw_data)

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

    @property
    def user_id(self) -> Optional[int]:
        """Get the authenticated user ID."""
        return self._user_id

    # Bible API methods
    async def get_bible_configuration(self) -> dict[str, Any]:
        """Get Bible configuration.

        Returns:
            Bible configuration data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_bible_configuration()
        return self._data_processor.process_bible_configuration(raw_data)

    async def get_bible_versions(
        self, language_tag: str = "eng", version_type: str = "all"
    ) -> dict[str, Any]:
        """Get Bible versions for a language.

        Args:
            language_tag: Language tag (e.g., 'eng', 'spa')
            version_type: Type of versions ('all', 'text', 'audio')

        Returns:
            Bible versions data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_bible_versions(
            language_tag, version_type
        )
        return self._data_processor.process_bible_versions(raw_data)

    async def get_bible_version(self, version_id: int) -> dict[str, Any]:
        """Get specific Bible version details.

        Args:
            version_id: Version ID

        Returns:
            Bible version data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_bible_version(version_id)
        return self._data_processor.process_bible_version(raw_data)

    async def get_bible_chapter(
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
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_bible_chapter(version_id, reference)
        return self._data_processor.process_bible_chapter(raw_data)

    async def get_recommended_languages(self, country: str = "US") -> dict[str, Any]:
        """Get recommended languages for a country.

        Args:
            country: Country code (e.g., 'US', 'CA')

        Returns:
            Recommended languages data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_recommended_languages(country)
        return self._data_processor.process_recommended_languages(raw_data)

    # Audio Bible API methods
    async def get_audio_chapter(
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
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_audio_chapter(version_id, reference)
        return self._data_processor.process_audio_chapter(raw_data)

    async def get_audio_version(self, audio_id: int) -> dict[str, Any]:
        """Get audio version details.

        Args:
            audio_id: Audio version ID

        Returns:
            Audio version data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_audio_version(audio_id)
        return self._data_processor.process_audio_version(raw_data)

    # Search API methods
    async def search_bible(
        self,
        query: str,
        version_id: Optional[int] = None,
        book: Optional[str] = None,
        page: int = 1,
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
        await self._ensure_authenticated()
        raw_data = await self._http_client.search_bible(query, version_id, book, page)
        return self._data_processor.process_search_bible(raw_data)

    async def search_plans(
        self, query: str, language_tag: str = "en", page: int = 1
    ) -> dict[str, Any]:
        """Search reading plans.

        Args:
            query: Search query
            language_tag: Language tag
            page: Page number

        Returns:
            Plan search results data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.search_plans(query, language_tag, page)
        return self._data_processor.process_search_plans(raw_data)

    async def search_users(
        self, query: str, language_tag: str = "eng", page: int = 1
    ) -> dict[str, Any]:
        """Search users.

        Args:
            query: Search query
            language_tag: Language tag
            page: Page number

        Returns:
            User search results data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.search_users(query, language_tag, page)
        return self._data_processor.process_search_users(raw_data)

    # Videos API methods
    async def get_videos(self, language_tag: str = "eng") -> dict[str, Any]:
        """Get videos list.

        Args:
            language_tag: Language tag

        Returns:
            Videos data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_videos(language_tag)
        return self._data_processor.process_videos(raw_data)

    async def get_video_details(self, video_id: int) -> dict[str, Any]:
        """Get video details.

        Args:
            video_id: Video ID

        Returns:
            Video details data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_video_details(video_id)
        return self._data_processor.process_video_details(raw_data)

    # Badges API methods
    async def badges(self, page: int = 1) -> list[Any]:
        """Get badges.

        Args:
            page: Page number

        Returns:
            List of badge data
        """
        raw_data = await self._get_cards_data(kind=MomentKinds.BADGE.value, page=page)

        if raw_data.get("errors"):
            raw_data = raw_data.get("errors")

        return self._data_processor.process_badges(raw_data)

    # Images API methods
    async def get_images(
        self, reference: str, language_tag: str = "eng", page: int = 1
    ) -> dict[str, Any]:
        """Get images for a reference.

        Args:
            reference: USFM reference
            language_tag: Language tag
            page: Page number

        Returns:
            Images data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_images(reference, language_tag, page)
        raw_data = raw_data.get("images", [])
        return self._data_processor.process_images(raw_data)

    async def get_image_upload_url(self) -> dict[str, Any]:
        """Get image upload URL and parameters.

        Returns:
            Upload URL data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_image_upload_url()
        return self._data_processor.process_image_upload_url(raw_data)

    # Events API methods
    async def search_events(
        self,
        query: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        page: int = 1,
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
        await self._ensure_authenticated()
        raw_data = await self._http_client.search_events(
            query, latitude, longitude, page
        )
        return self._data_processor.process_search_events(raw_data)

    async def get_event_details(self, event_id: int) -> dict[str, Any]:
        """Get event details.

        Args:
            event_id: Event ID

        Returns:
            Event details data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_event_details(event_id)
        return self._data_processor.process_event_details(raw_data)

    async def get_saved_events(self, page: int = 1) -> dict[str, Any]:
        """Get saved events.

        Args:
            page: Page number

        Returns:
            Saved events data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_saved_events(page)
        return self._data_processor.process_saved_events(raw_data)

    async def save_event(
        self, event_id: int, comments: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Save event.

        Args:
            event_id: Event ID
            comments: Comments (optional)

        Returns:
            Save result data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.save_event(event_id, comments)
        return self._data_processor.process_save_event(raw_data)

    async def delete_saved_event(self, event_id: int) -> dict[str, Any]:
        """Delete saved event.

        Args:
            event_id: Event ID

        Returns:
            Delete result data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.delete_saved_event(event_id)
        return self._data_processor.process_delete_saved_event(raw_data)

    async def get_all_saved_event_ids(self) -> dict[str, Any]:
        """Get all saved event IDs.

        Returns:
            All saved event IDs data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_all_saved_event_ids()
        return self._data_processor.process_all_saved_event_ids(raw_data)

    async def get_event_configuration(self) -> dict[str, Any]:
        """Get event configuration.

        Returns:
            Event configuration data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_event_configuration()
        return self._data_processor.process_event_configuration(raw_data)

    # Moments API methods
    async def get_moments(
        self,
        page: int = 1,
        user_id: Optional[int] = None,
        kind: Optional[str] = None,
        version_id: Optional[int] = None,
        usfm: Optional[str] = None,
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
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_moments(
            page, user_id, kind, version_id, usfm
        )
        return self._data_processor.process_moments_list(raw_data)

    async def get_moment_details(self, moment_id: int) -> dict[str, Any]:
        """Get moment details.

        Args:
            moment_id: Moment ID

        Returns:
            Moment details data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_moment_details(moment_id)
        return self._data_processor.process_moment_details(raw_data)

    async def create_moment(
        self, data: Union[CreateMoment, dict[str, Any]]
    ) -> dict[str, Any]:
        """Create a new moment.

        Args:
            data: Moment data as CreateMoment model or dict

        Returns:
            Created moment data
        """
        await self._ensure_authenticated()
        # Convert to CreateMoment if dict is provided
        if isinstance(data, dict):
            moment_data = CreateMoment(**data)
        else:
            moment_data = data

        # Add created_dt timestamp
        moment_dict = moment_data.model_dump()
        moment_dict["created_dt"] = datetime.now(tz=timezone.utc).isoformat()

        raw_data = await self._http_client.create_moment(moment_dict)
        return self._data_processor.process_create_moment(raw_data)

    async def update_moment(self, data: dict[str, Any]) -> dict[str, Any]:
        """Update an existing moment.

        Args:
            data: Moment data

        Returns:
            Updated moment data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.update_moment(data)
        return self._data_processor.process_update_moment(raw_data)

    async def delete_moment(self, moment_id: int) -> dict[str, Any]:
        """Delete a moment.

        Args:
            moment_id: Moment ID

        Returns:
            Delete result data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.delete_moment(moment_id)
        return self._data_processor.process_delete_moment(raw_data)

    async def get_moment_colors(self) -> dict[str, Any]:
        """Get available highlight colors.

        Returns:
            Colors data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_moment_colors()
        return self._data_processor.process_moment_colors(raw_data)

    async def get_moment_labels(self) -> dict[str, Any]:
        """Get moment labels.

        Returns:
            Labels data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_moment_labels()
        return self._data_processor.process_moment_labels(raw_data)

    async def get_verse_colors(self, usfm: str, version_id: int) -> dict[str, Any]:
        """Get verse highlight colors.

        Args:
            usfm: USFM reference
            version_id: Bible version ID

        Returns:
            Verse colors data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_verse_colors(usfm, version_id)
        return self._data_processor.process_verse_colors(raw_data)

    async def hide_verse_colors(self, data: dict[str, Any]) -> dict[str, Any]:
        """Hide verse highlight colors.

        Args:
            data: Hide colors data

        Returns:
            Hide result data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.hide_verse_colors(data)
        return self._data_processor.process_hide_verse_colors(raw_data)

    async def get_moments_configuration(self) -> dict[str, Any]:
        """Get moments configuration.

        Returns:
            Moments configuration data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_moments_configuration()
        return self._data_processor.process_moments_configuration(raw_data)

    # Comments API methods
    async def create_comment(self, moment_id: int, comment: str) -> dict[str, Any]:
        """Create a comment on a moment.

        Args:
            moment_id: Moment ID
            comment: Comment text

        Returns:
            Created comment data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.create_comment(moment_id, comment)
        return self._data_processor.process_create_comment(raw_data)

    async def delete_comment(self, comment_id: int) -> dict[str, Any]:
        """Delete a comment.

        Args:
            comment_id: Comment ID

        Returns:
            Delete result data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.delete_comment(comment_id)
        return self._data_processor.process_delete_comment(raw_data)

    # Likes API methods
    async def like_moment(self, moment_id: int) -> dict[str, Any]:
        """Like a moment.

        Args:
            moment_id: Moment ID

        Returns:
            Like result data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.like_moment(moment_id)
        return self._data_processor.process_like_moment(raw_data)

    async def unlike_moment(self, moment_id: int) -> dict[str, Any]:
        """Unlike a moment.

        Args:
            moment_id: Moment ID

        Returns:
            Unlike result data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.unlike_moment(moment_id)
        return self._data_processor.process_unlike_moment(raw_data)

    # Messaging API methods
    async def register_device(
        self,
        device_id: str,
        device_type: str = "android",
        user_id: Optional[int] = None,
        old_device_id: Optional[str] = None,
        tags: Optional[str] = None,
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
        await self._ensure_authenticated()
        raw_data = await self._http_client.register_device(
            device_id, device_type, user_id, old_device_id, tags
        )
        return self._data_processor.process_register_device(raw_data)

    async def unregister_device(self, device_id: str) -> dict[str, Any]:
        """Unregister device from push notifications.

        Args:
            device_id: Device ID

        Returns:
            Unregistration result data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.unregister_device(device_id)
        return self._data_processor.process_unregister_device(raw_data)

    # Themes API methods
    async def get_themes(
        self, page: int = 1, language_tag: str = "eng"
    ) -> dict[str, Any]:
        """Get available themes.

        Args:
            page: Page number
            language_tag: Language tag

        Returns:
            Themes data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_themes(page, language_tag)
        return self._data_processor.process_themes(raw_data)

    async def add_theme(
        self,
        theme_id: int,
        available_locales: list[str],
        colors: dict[str, Any],
        cta_urls: dict[str, Any],
        msgid_suffix: str,
        version_ids: dict[str, int],
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
        await self._ensure_authenticated()
        raw_data = await self._http_client.add_theme(
            theme_id, available_locales, colors, cta_urls, msgid_suffix, version_ids
        )
        return self._data_processor.process_add_theme(raw_data)

    async def remove_theme(self, theme_id: int) -> dict[str, Any]:
        """Remove a theme from user's collection.

        Args:
            theme_id: Theme ID

        Returns:
            Remove result data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.remove_theme(theme_id)
        return self._data_processor.process_remove_theme(raw_data)

    async def set_theme(
        self, theme_id: int, previous_theme_id: Optional[int] = None
    ) -> dict[str, Any]:
        """Set active theme.

        Args:
            theme_id: Theme ID
            previous_theme_id: Previous theme ID (optional)

        Returns:
            Set result data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.set_theme(theme_id, previous_theme_id)
        return self._data_processor.process_set_theme(raw_data)

    async def get_theme_description(
        self, theme_id: int, language_tag: str = "eng"
    ) -> dict[str, Any]:
        """Get theme description.

        Args:
            theme_id: Theme ID
            language_tag: Language tag

        Returns:
            Theme description data
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.get_theme_description(theme_id, language_tag)
        return self._data_processor.process_theme_description(raw_data)

    # Friendships API methods
    async def send_friend_request(self, user_id: int) -> dict[str, Any]:
        """Send a friend request to a user.

        Args:
            user_id: User ID to send friend request to

        Returns:
            Friend request response data with incoming and outgoing lists
        """
        await self._ensure_authenticated()
        raw_data = await self._http_client.send_friend_request(user_id)
        return self._data_processor.process_send_friend_request(raw_data)

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
