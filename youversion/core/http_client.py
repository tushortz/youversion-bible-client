"""HTTP client for YouVersion API operations."""

from typing import Any, Dict, Optional

import httpx

from ..config import Config
from .interfaces import IHttpClient


class HttpClient(IHttpClient):
    """Handles HTTP operations for YouVersion API."""

    def __init__(self, client: httpx.AsyncClient, user_id: Optional[int] = None):
        """Initialize HTTP client.

        Args:
            client: Authenticated httpx.AsyncClient
            user_id: Authenticated user ID
        """
        self._client = client
        self._user_id = user_id

    async def get(self, url: str, **kwargs) -> dict[str, Any]:
        """Perform GET request.

        Args:
            url: URL to request
            **kwargs: Additional arguments for the request

        Returns:
            JSON response as dictionary
        """
        # Merge DEFAULT_HEADERS with any headers passed in kwargs
        headers = {**Config.DEFAULT_HEADERS, **kwargs.get("headers", {})}
        kwargs["headers"] = headers
        response = await self._client.get(url, **kwargs)
        try:
            data = response.json()
            # Support mocked AsyncMock json() returning a coroutine
            if hasattr(data, "__await__"):
                data = await data
            return data
        except ValueError:
            # Re-raise to allow callers/tests to handle JSON parse errors
            raise

    async def post(self, url: str, **kwargs) -> dict[str, Any]:
        """Perform POST request.

        Args:
            url: URL to request
            **kwargs: Additional arguments for the request

        Returns:
            JSON response as dictionary
        """
        # Merge DEFAULT_HEADERS with any headers passed in kwargs
        headers = {**Config.DEFAULT_HEADERS, **kwargs.get("headers", {})}
        kwargs["headers"] = headers
        response = await self._client.post(url, **kwargs)
        try:
            data = response.json()
            if hasattr(data, "__await__"):
                data = await data
            return data
        except ValueError:
            # Re-raise to allow callers/tests to handle JSON parse errors
            raise

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()

    # Legacy methods for backward compatibility
    async def get_cards(
        self, page: int = 1, kind: str = ""
    ) -> dict[str, Any]:
        """Get cards data from moments endpoint.

        Args:
            page: Page number
            kind: Kind of data to retrieve

        Returns:
            Cards data as dictionary
        """
        url = (
            f"{Config.MOMENTS_API_BASE}"
            f"{Config.MOMENTS_ITEMS_URL}"
        )
        # Build params dict, omitting falsy values (False, None, empty strings)
        params = {}
        if page is not None and page is not False:
            params["page"] = page
        if kind:  # Excludes None, False, and empty strings
            params["kind"] = kind
        if self._user_id is not None and self._user_id is not False:
            params["user_id"] = self._user_id

        return await self.get(url, params=params)

    async def get_verse_of_the_day(self) -> dict[str, Any]:
        """Get verse of the day data.

        Returns:
            Verse of the day data as dictionary
        """
        return await self.get(Config.VOTD_URL)

    # Bible API methods
    async def get_bible_configuration(self) -> dict[str, Any]:
        """Get Bible configuration.

        Returns:
            Bible configuration data
        """
        url = f"{Config.BIBLE_API_BASE}{Config.BIBLE_CONFIGURATION_URL}"
        return await self.get(url, headers=Config.DEFAULT_HEADERS)

    async def get_bible_versions(
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
        url = f"{Config.BIBLE_API_BASE}{Config.BIBLE_VERSIONS_URL}"
        params = {"language_tag": language_tag, "type": version_type}
        return await self.get(url, headers=Config.DEFAULT_HEADERS, params=params)

    async def get_bible_version(self, version_id: int) -> dict[str, Any]:
        """Get specific Bible version details.

        Args:
            version_id: Version ID

        Returns:
            Bible version data
        """
        url = f"{Config.BIBLE_API_BASE}{Config.BIBLE_VERSION_URL}"
        params = {"id": version_id}
        return await self.get(url, headers=Config.DEFAULT_HEADERS, params=params)

    async def get_bible_chapter(
        self,
        version_id: int,
        reference: str
    ) -> dict[str, Any]:
        """Get Bible chapter content.

        Args:
            version_id: Version ID
            reference: USFM reference (e.g., 'GEN.1')

        Returns:
            Chapter content data
        """
        url = f"{Config.BIBLE_API_BASE}{Config.BIBLE_CHAPTER_URL}"
        params = {"id": version_id, "reference": reference}
        return await self.get(url, headers=Config.DEFAULT_HEADERS, params=params)

    async def get_recommended_languages(self, country: str = "US") -> dict[str, Any]:
        """Get recommended languages for a country.

        Args:
            country: Country code (e.g., 'US', 'CA')

        Returns:
            Recommended languages data
        """
        url = f"{Config.BIBLE_API_BASE}{Config.BIBLE_RECOMMENDED_LANGUAGES_URL}"
        params = {"country": country}
        return await self.get(url, headers=Config.DEFAULT_HEADERS, params=params)

    # Audio Bible API methods
    async def get_audio_chapter(
        self,
        version_id: int,
        reference: str
    ) -> dict[str, Any]:
        """Get audio chapter information.

        Args:
            version_id: Audio version ID
            reference: USFM reference (e.g., 'GEN.1')

        Returns:
            Audio chapter data
        """
        url = f"{Config.AUDIO_BIBLE_API_BASE}{Config.AUDIO_CHAPTER_URL}"
        params = {"version_id": version_id, "reference": reference}
        return await self.get(url, headers=Config.DEFAULT_HEADERS, params=params)

    async def get_audio_version(self, audio_id: int) -> dict[str, Any]:
        """Get audio version details.

        Args:
            audio_id: Audio version ID

        Returns:
            Audio version data
        """
        url = f"{Config.AUDIO_BIBLE_API_BASE}{Config.AUDIO_VIEW_URL}"
        params = {"id": audio_id}
        return await self.get(url, headers=Config.DEFAULT_HEADERS, params=params)

    # Search API methods
    async def search_bible(
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
        url = f"{Config.SEARCH_API_BASE}{Config.SEARCH_BIBLE_URL}"
        params = {"query": query, "page": page}
        if version_id:
            params["version_id"] = version_id
        if book:
            params["book"] = book
        return await self.get(url, headers=Config.DEFAULT_HEADERS, params=params)

    async def search_plans(
        self,
        query: str,
        language_tag: str = "eng",
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
        url = f"{Config.SEARCH_API_BASE}{Config.SEARCH_PLANS_URL}"
        params = {"query": query, "language_tag": language_tag, "page": page}
        return await self.get(url, headers=Config.DEFAULT_HEADERS, params=params)

    async def search_users(
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
        url = f"{Config.SEARCH_API_BASE}{Config.SEARCH_USERS_URL}"
        params = {"query": query, "language_tag": language_tag, "page": page}
        return await self.get(url, headers=Config.DEFAULT_HEADERS, params=params)

    # Videos API methods
    async def get_videos(self, language_tag: str = "eng") -> dict[str, Any]:
        """Get videos list.

        Args:
            language_tag: Language tag

        Returns:
            Videos data
        """
        url = f"{Config.SEARCH_API_BASE}{Config.SEARCH_VIDEOS_URL}"
        params = {"language_tag": language_tag}
        return await self.get(url, headers=Config.DEFAULT_HEADERS, params=params)

    async def get_video_details(self, video_id: int) -> dict[str, Any]:
        """Get video details.

        Args:
            video_id: Video ID

        Returns:
            Video details data
        """
        url = f"{Config.VIDEOS_API_BASE}{Config.VIDEOS_VIEW_URL}"
        params = {"id": video_id}
        return await self.get(url, headers=Config.DEFAULT_HEADERS, params=params)

    # Badges API methods
    async def get_badges(self, user_id: int, page: int = 1) -> dict[str, Any]:
        """Get user badges.

        Args:
            user_id: User ID
            page: Page number

        Returns:
            Badges data
        """
        url = f"{Config.BADGES_API_BASE}{Config.BADGES_ITEMS_URL}"
        params = {"user_id": user_id, "page": page}
        return await self.get(url, headers=Config.DEFAULT_HEADERS, params=params)

    # Images API methods
    async def get_images(
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
        url = f"{Config.IMAGES_API_BASE}{Config.IMAGES_ITEMS_URL}"
        params = {"reference": reference,
                  "language_tag": language_tag, "page": page}
        return await self.get(url, headers=Config.DEFAULT_HEADERS, params=params)

    async def get_image_upload_url(self) -> dict[str, Any]:
        """Get image upload URL and parameters.

        Returns:
            Upload URL data
        """
        url = f"{Config.IMAGES_API_BASE}{Config.IMAGES_UPLOAD_URL}"
        return await self.get(url, headers=Config.DEFAULT_HEADERS)

    # Events API methods
    async def search_events(
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
        url = f"{Config.EVENTS_API_BASE}{Config.EVENTS_SEARCH_URL}"
        params = {"query": query, "page": page}
        if latitude:
            params["latitude"] = latitude
        if longitude:
            params["longitude"] = longitude
        return await self.get(url, headers=Config.DEFAULT_HEADERS, params=params)

    async def get_event_details(self, event_id: int) -> dict[str, Any]:
        """Get event details.

        Args:
            event_id: Event ID

        Returns:
            Event details data
        """
        url = f"{Config.EVENTS_API_BASE}{Config.EVENTS_VIEW_URL}"
        params = {"id": event_id}
        return await self.get(url, headers=Config.DEFAULT_HEADERS, params=params)

    async def get_saved_events(self, page: int = 1) -> dict[str, Any]:
        """Get saved events.

        Args:
            page: Page number

        Returns:
            Saved events data
        """
        url = f"{Config.EVENTS_API_BASE}{Config.EVENTS_SAVED_ITEMS_URL}"
        params = {"page": page}
        return await self.get(url, headers=Config.DEFAULT_HEADERS, params=params)

    async def save_event(
        self,
        event_id: int,
        comments: Optional[Dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Save event.

        Args:
            event_id: Event ID
            comments: Comments (optional)

        Returns:
            Save result data
        """
        url = f"{Config.EVENTS_API_BASE}{Config.EVENTS_SAVE_URL}"
        data = {"id": event_id}
        if comments:
            data["comments"] = comments
        headers = {**Config.DEFAULT_HEADERS,
                   "Content-Type": "application/json"}
        return await self.post(url, headers=headers, json=data)

    async def delete_saved_event(self, event_id: int) -> dict[str, Any]:
        """Delete saved event.

        Args:
            event_id: Event ID

        Returns:
            Delete result data
        """
        url = f"{Config.EVENTS_API_BASE}{Config.EVENTS_DELETE_SAVED_URL}"
        params = {"id": event_id}
        headers = {**Config.DEFAULT_HEADERS, "Content-Type": "text/plain"}
        return await self.post(url, headers=headers, params=params)

    async def get_all_saved_event_ids(self) -> dict[str, Any]:
        """Get all saved event IDs.

        Returns:
            All saved event IDs data
        """
        url = f"{Config.EVENTS_API_BASE}{Config.EVENTS_SAVED_ALL_ITEMS_URL}"
        return await self.get(url, headers=Config.DEFAULT_HEADERS)

    async def get_event_configuration(self) -> dict[str, Any]:
        """Get event configuration.

        Returns:
            Event configuration data
        """
        url = f"{Config.EVENTS_API_BASE}{Config.EVENTS_CONFIGURATION_URL}"
        return await self.get(url, headers=Config.DEFAULT_HEADERS)

    # Moments API methods
    async def get_moments(
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
        url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_ITEMS_URL}"
        params = {"page": page}
        if user_id:
            params["user_id"] = user_id
        if kind:
            params["kind"] = kind
        if version_id:
            params["version_id"] = version_id
        if usfm:
            params["usfm"] = usfm
        return await self.get(url, headers=Config.DEFAULT_HEADERS, params=params)

    async def get_moment_details(self, moment_id: int) -> dict[str, Any]:
        """Get moment details.

        Args:
            moment_id: Moment ID

        Returns:
            Moment details data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_VIEW_URL}"
        params = {"id": moment_id}
        return await self.get(url, headers=Config.DEFAULT_HEADERS, params=params)

    async def create_moment(self, data: Dict[str, Any]) -> dict[str, Any]:
        """Create a new moment.

        Args:
            data: Moment data

        Returns:
            Created moment data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_CREATE_URL}"
        headers = {**Config.DEFAULT_HEADERS,
                   "Content-Type": "application/json"}
        return await self.post(url, headers=headers, json=data)

    async def update_moment(self, data: Dict[str, Any]) -> dict[str, Any]:
        """Update an existing moment.

        Args:
            data: Moment data

        Returns:
            Updated moment data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_UPDATE_URL}"
        headers = {**Config.DEFAULT_HEADERS,
                   "Content-Type": "application/json"}
        return await self.post(url, headers=headers, json=data)

    async def delete_moment(self, moment_id: int) -> dict[str, Any]:
        """Delete a moment.

        Args:
            moment_id: Moment ID

        Returns:
            Delete result data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_DELETE_URL}"
        data = {"id": moment_id}
        headers = {**Config.DEFAULT_HEADERS,
                   "Content-Type": "application/json"}
        return await self.post(url, headers=headers, json=data)

    async def get_moment_colors(self) -> dict[str, Any]:
        """Get available highlight colors.

        Returns:
            Colors data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_COLORS_URL}"
        return await self.get(url, headers=Config.DEFAULT_HEADERS)

    async def get_moment_labels(self) -> dict[str, Any]:
        """Get moment labels.

        Returns:
            Labels data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_LABELS_URL}"
        return await self.get(url, headers=Config.DEFAULT_HEADERS)

    async def get_verse_colors(
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
        url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_VERSE_COLORS_URL}"
        params = {"usfm": usfm, "version_id": version_id}
        return await self.get(url, headers=Config.DEFAULT_HEADERS, params=params)

    async def hide_verse_colors(self, data: Dict[str, Any]) -> dict[str, Any]:
        """Hide verse highlight colors.

        Args:
            data: Hide colors data

        Returns:
            Hide result data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_HIDE_VERSE_COLORS_URL}"
        headers = {**Config.DEFAULT_HEADERS,
                   "Content-Type": "application/json"}
        return await self.post(url, headers=headers, json=data)

    async def get_verse_of_the_day_new(
        self,
        language_tag: str = "eng"
    ) -> dict[str, Any]:
        """Get verse of the day (new API).

        Args:
            language_tag: Language tag

        Returns:
            Verse of the day data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_VOTD_URL}"
        params = {"language_tag": language_tag}
        return await self.get(url, headers=Config.DEFAULT_HEADERS, params=params)

    async def get_moments_configuration(self) -> dict[str, Any]:
        """Get moments configuration.

        Returns:
            Moments configuration data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_CONFIGURATION_URL}"
        return await self.get(url, headers=Config.DEFAULT_HEADERS)

    # Comments API methods
    async def create_comment(
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
        url = f"{Config.MOMENTS_API_BASE}{Config.COMMENTS_CREATE_URL}"
        data = {"moment_id": moment_id, "comment": comment}
        headers = {**Config.DEFAULT_HEADERS,
                   "Content-Type": "application/json"}
        return await self.post(url, headers=headers, json=data)

    async def delete_comment(self, comment_id: int) -> dict[str, Any]:
        """Delete a comment.

        Args:
            comment_id: Comment ID

        Returns:
            Delete result data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.COMMENTS_DELETE_URL}"
        data = {"id": comment_id}
        headers = {**Config.DEFAULT_HEADERS,
                   "Content-Type": "application/json"}
        return await self.post(url, headers=headers, json=data)

    # Likes API methods
    async def like_moment(self, moment_id: int) -> dict[str, Any]:
        """Like a moment.

        Args:
            moment_id: Moment ID

        Returns:
            Like result data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.LIKES_CREATE_URL}"
        data = {"moment_id": moment_id}
        headers = {**Config.DEFAULT_HEADERS,
                   "Content-Type": "application/json"}
        return await self.post(url, headers=headers, json=data)

    async def unlike_moment(self, moment_id: int) -> dict[str, Any]:
        """Unlike a moment.

        Args:
            moment_id: Moment ID

        Returns:
            Unlike result data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.LIKES_DELETE_URL}"
        data = {"moment_id": moment_id}
        headers = {**Config.DEFAULT_HEADERS,
                   "Content-Type": "application/json"}
        return await self.post(url, headers=headers, json=data)

    # Messaging API methods
    async def register_device(
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
        url = f"{Config.MOMENTS_API_BASE}{Config.MESSAGING_REGISTER_URL}"
        data = {
            "id": device_id,
            "type": device_type
        }
        if user_id:
            data["user_id"] = user_id
        if old_device_id:
            data["old_id"] = old_device_id
        if tags:
            data["tags"] = tags
        headers = {**Config.DEFAULT_HEADERS,
                   "Content-Type": "application/x-www-form-urlencoded"}
        return await self.post(url, headers=headers, data=data)

    async def unregister_device(self, device_id: str) -> dict[str, Any]:
        """Unregister device from push notifications.

        Args:
            device_id: Device ID

        Returns:
            Unregistration result data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.MESSAGING_UNREGISTER_URL}"
        data = {"id": device_id}
        headers = {**Config.DEFAULT_HEADERS,
                   "Content-Type": "application/json"}
        return await self.post(url, headers=headers, json=data)

    # Themes API methods
    async def get_themes(
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
        url = f"{Config.MOMENTS_API_BASE}{Config.THEMES_ITEMS_URL}"
        params = {"page": page, "language_tag": language_tag}
        return await self.get(url, headers=Config.DEFAULT_HEADERS, params=params)

    async def add_theme(self, theme_id: int) -> dict[str, Any]:
        """Add a theme to user's collection.

        Args:
            theme_id: Theme ID

        Returns:
            Add result data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.THEMES_ADD_URL}"
        data = {"id": theme_id}
        headers = {**Config.DEFAULT_HEADERS,
                   "Content-Type": "application/json"}
        return await self.post(url, headers=headers, json=data)

    async def remove_theme(self, theme_id: int) -> dict[str, Any]:
        """Remove a theme from user's collection.

        Args:
            theme_id: Theme ID

        Returns:
            Remove result data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.THEMES_REMOVE_URL}"
        data = {"id": theme_id}
        headers = {**Config.DEFAULT_HEADERS,
                   "Content-Type": "application/json"}
        return await self.post(url, headers=headers, json=data)

    async def set_theme(
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
        url = f"{Config.MOMENTS_API_BASE}{Config.THEMES_SET_URL}"
        data = {"id": theme_id}
        if previous_theme_id:
            data["previous_id"] = previous_theme_id
        headers = {**Config.DEFAULT_HEADERS,
                   "Content-Type": "application/json"}
        return await self.post(url, headers=headers, json=data)

    async def get_theme_description(
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
        url = f"{Config.MOMENTS_API_BASE}{Config.THEMES_DESCRIPTION_URL}"
        params = {"id": theme_id, "language_tag": language_tag}
        return await self.get(url, headers=Config.DEFAULT_HEADERS, params=params)

    # Localization API methods
    async def get_localization_items(self, language_tag: str = "eng") -> str:
        """Get localization strings for a language.

        Args:
            language_tag: Language tag

        Returns:
            Localization strings (PO file format)
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.LOCALIZATION_ITEMS_URL}"
        params = {"language_tag": language_tag}
        response = await self._client.get(url, headers=Config.DEFAULT_HEADERS, params=params)
        return response.text
