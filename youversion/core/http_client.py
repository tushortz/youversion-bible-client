"""HTTP client for YouVersion API operations."""

from typing import Any, Optional

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
        self._public_client: Optional[httpx.AsyncClient] = None

    def _ensure_public_client(self) -> httpx.AsyncClient:
        """Return an httpx client without Authorization (public endpoints)."""
        if self._public_client is None:
            self._public_client = httpx.AsyncClient(
                headers=dict(Config.DEFAULT_HEADERS),
                timeout=Config.HTTP_TIMEOUT,
            )
        return self._public_client

    @staticmethod
    def _unwrap_envelope(data: dict[str, Any]) -> dict[str, Any]:
        if "response" in data:
            return data.get("response", {}).get("data", {})
        return data

    async def get(self, url: str, **kwargs) -> dict[str, Any]:
        """Perform GET request.

        Args:
            url: URL to request
            **kwargs: Additional arguments for the request

        Returns:
            JSON response as dictionary
        """
        # Always merge DEFAULT_HEADERS with any headers passed in kwargs
        headers = {**Config.DEFAULT_HEADERS, **kwargs.get("headers", {})}
        kwargs["headers"] = headers
        response = await self._client.get(url, **kwargs)
        try:
            data = response.json()
            # Support mocked AsyncMock json() returning a coroutine
            if hasattr(data, "__await__"):
                data = await data
            return self._unwrap_envelope(data)
        except ValueError:
            # Re-raise to allow callers/tests to handle JSON parse errors
            raise

    async def get_public(self, url: str, **kwargs) -> dict[str, Any]:
        """Perform GET without Authorization (endpoints that reject Bearer tokens).

        Args:
            url: URL to request
            **kwargs: Additional arguments for the request

        Returns:
            JSON response data from the API envelope
        """
        headers = {**Config.DEFAULT_HEADERS, **kwargs.get("headers", {})}
        kwargs["headers"] = headers
        response = await self._ensure_public_client().get(url, **kwargs)
        try:
            data = response.json()
            if hasattr(data, "__await__"):
                data = await data
            return self._unwrap_envelope(data)
        except ValueError:
            raise

    async def post(self, url: str, **kwargs) -> dict[str, Any]:
        """Perform POST request.

        Args:
            url: URL to request
            **kwargs: Additional arguments for the request

        Returns:
            JSON response as dictionary
        """
        # Always merge DEFAULT_HEADERS with any headers passed in kwargs
        headers = {**Config.DEFAULT_HEADERS, **kwargs.get("headers", {})}
        kwargs["headers"] = headers
        response = await self._client.post(url, **kwargs)
        try:
            data = response.json()
            if hasattr(data, "__await__"):
                data = await data
            if hasattr(data, "__await__"):
                data = await data
            return self._unwrap_envelope(data)
        except ValueError:
            # Re-raise to allow callers/tests to handle JSON parse errors
            raise

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._public_client:
            await self._public_client.aclose()
        if self._client:
            await self._client.aclose()

    # Legacy methods for backward compatibility
    async def get_cards(self, page: int = 1, kind: str = "") -> dict[str, Any]:
        """Get cards data from moments endpoint.

        Args:
            page: Page number
            kind: Kind of data to retrieve

        Returns:
            Cards data as dictionary
        """
        url = f"{Config.MOMENTS_API_BASE}" f"{Config.MOMENTS_ITEMS_URL}"
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
        return await self.get(url)

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
        url = f"{Config.BIBLE_API_BASE}{Config.BIBLE_VERSIONS_URL}"
        params = {"language_tag": language_tag, "type": version_type}
        return await self.get(url, params=params)

    async def get_bible_version(self, version_id: int) -> dict[str, Any]:
        """Get specific Bible version details.

        Args:
            version_id: Version ID

        Returns:
            Bible version data
        """
        url = f"{Config.BIBLE_API_BASE}{Config.BIBLE_VERSION_URL}"
        params = {"id": version_id}
        return await self.get(url, params=params)

    async def get_bible_chapter(
        self, version_id: int, reference: str
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
        return await self.get_public(url, params=params)

    async def get_recommended_languages(self, country: str = "US") -> dict[str, Any]:
        """Get recommended languages for a country.

        Args:
            country: Country code (e.g., 'US', 'CA')

        Returns:
            Recommended languages data
        """
        url = f"{Config.BIBLE_API_BASE}{Config.BIBLE_RECOMMENDED_LANGUAGES_URL}"
        params = {"country": country}
        return await self.get(url, params=params)

    # Audio Bible API methods
    async def get_audio_chapter(
        self, version_id: int, reference: str
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
        return await self.get_public(url, params=params)

    async def get_audio_version(self, audio_id: int) -> dict[str, Any]:
        """Get audio version details.

        Args:
            audio_id: Audio version ID

        Returns:
            Audio version data
        """
        url = f"{Config.AUDIO_BIBLE_API_BASE}{Config.AUDIO_VIEW_URL}"
        params = {"id": audio_id}
        return await self.get(url, params=params)

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
        url = f"{Config.SEARCH_API_BASE}{Config.SEARCH_BIBLE_URL}"
        params = {"query": query, "page": page}
        if version_id:
            params["version_id"] = version_id
        if book:
            params["book"] = book
        return await self.get(url, params=params)

    async def search_plans(
        self, query: str, language_tag: str = "eng", page: int = 1
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
        return await self.get(url, params=params)

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
        url = f"{Config.SEARCH_API_BASE}{Config.SEARCH_USERS_URL}"
        params = {"query": query, "language_tag": language_tag, "page": page}
        return await self.get(url, params=params)

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
        return await self.get(url, params=params)

    async def get_video_details(self, video_id: int) -> dict[str, Any]:
        """Get video details.

        Args:
            video_id: Video ID

        Returns:
            Video details data
        """
        url = f"{Config.VIDEOS_API_BASE}{Config.VIDEOS_VIEW_URL}"
        params = {"id": video_id}
        return await self.get(url, params=params)

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
        url = f"{Config.IMAGES_API_BASE}{Config.IMAGES_ITEMS_URL}"
        params = {"reference": reference, "language_tag": language_tag, "page": page}
        return await self.get(url, params=params)

    async def get_image_upload_url(self) -> dict[str, Any]:
        """Get image upload URL and parameters.

        Returns:
            Upload URL data
        """
        url = f"{Config.IMAGES_API_BASE}{Config.IMAGES_UPLOAD_URL}"
        return await self.get(url)

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
        url = f"{Config.EVENTS_API_BASE}{Config.EVENTS_SEARCH_URL}"
        params = {"query": query, "page": page}
        if latitude:
            params["latitude"] = latitude
        if longitude:
            params["longitude"] = longitude
        return await self.get(url, params=params)

    async def get_event_details(self, event_id: int) -> dict[str, Any]:
        """Get event details.

        Args:
            event_id: Event ID

        Returns:
            Event details data
        """
        url = f"{Config.EVENTS_API_BASE}{Config.EVENTS_VIEW_URL}"
        params = {"id": event_id}
        return await self.get(url, params=params)

    async def get_saved_events(self, page: int = 1) -> dict[str, Any]:
        """Get saved events.

        Args:
            page: Page number

        Returns:
            Saved events data
        """
        url = f"{Config.EVENTS_API_BASE}{Config.EVENTS_SAVED_ITEMS_URL}"
        params = {"page": page}
        return await self.get(url, params=params)

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
        url = f"{Config.EVENTS_API_BASE}{Config.EVENTS_SAVE_URL}"
        data = {"id": event_id}
        if comments:
            data["comments"] = comments
        return await self.post(url, json=data)

    async def delete_saved_event(self, event_id: int) -> dict[str, Any]:
        """Delete saved event.

        Args:
            event_id: Event ID

        Returns:
            Delete result data
        """
        url = f"{Config.EVENTS_API_BASE}{Config.EVENTS_DELETE_SAVED_URL}"
        return await self.post(url, json={"id": event_id})

    async def get_all_saved_event_ids(self) -> dict[str, Any]:
        """Get all saved event IDs.

        Returns:
            All saved event IDs data
        """
        url = f"{Config.EVENTS_API_BASE}{Config.EVENTS_SAVED_ALL_ITEMS_URL}"
        return await self.get(url)

    async def get_event_configuration(self) -> dict[str, Any]:
        """Get event configuration.

        Returns:
            Event configuration data
        """
        url = f"{Config.EVENTS_API_BASE}{Config.EVENTS_CONFIGURATION_URL}"
        return await self.get(url)

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
        return await self.get(url, params=params)

    async def get_moment_details(self, moment_id: int) -> dict[str, Any]:
        """Get moment details.

        Args:
            moment_id: Moment ID

        Returns:
            Moment details data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_VIEW_URL}"
        params = {"id": moment_id}
        return await self.get(url, params=params)

    async def create_moment(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a new moment.

        Args:
            data: Moment data

        Returns:
            Created moment data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_CREATE_URL}"
        return await self.post(url, json=data)

    async def update_moment(self, data: dict[str, Any]) -> dict[str, Any]:
        """Update an existing moment.

        Args:
            data: Moment data

        Returns:
            Updated moment data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_UPDATE_URL}"
        return await self.post(url, json=data)

    async def delete_moment(self, moment_id: int) -> dict[str, Any]:
        """Delete a moment.

        Args:
            moment_id: Moment ID

        Returns:
            Delete result data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_DELETE_URL}"
        data = {"id": moment_id}
        return await self.post(url, json=data)

    async def get_moment_colors(self) -> dict[str, Any]:
        """Get available highlight colors.

        Returns:
            Colors data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_COLORS_URL}"
        return await self.get(url)

    async def get_moment_labels(self) -> dict[str, Any]:
        """Get moment labels.

        Returns:
            Labels data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_LABELS_URL}"
        return await self.get(url)

    async def get_verse_colors(self, usfm: str, version_id: int) -> dict[str, Any]:
        """Get verse highlight colors.

        Args:
            usfm: USFM reference
            version_id: Bible version ID

        Returns:
            Verse colors data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_VERSE_COLORS_URL}"
        params = {"usfm": usfm, "version_id": version_id}
        return await self.get(url, params=params)

    async def hide_verse_colors(self, data: dict[str, Any]) -> dict[str, Any]:
        """Hide verse highlight colors.

        Args:
            data: Hide colors data

        Returns:
            Hide result data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_HIDE_VERSE_COLORS_URL}"
        return await self.post(url, json=data)

    async def get_moments_configuration(self) -> dict[str, Any]:
        """Get moments configuration.

        Returns:
            Moments configuration data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_CONFIGURATION_URL}"
        return await self.get_public(url)

    # Comments API methods
    async def create_comment(self, moment_id: int, comment: str) -> dict[str, Any]:
        """Create a comment on a moment.

        Args:
            moment_id: Moment ID
            comment: Comment text

        Returns:
            Created comment data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.COMMENTS_CREATE_URL}"
        data = {"moment_id": moment_id, "comment": comment}
        return await self.post(url, json=data)

    async def delete_comment(self, comment_id: int) -> dict[str, Any]:
        """Delete a comment.

        Args:
            comment_id: Comment ID

        Returns:
            Delete result data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.COMMENTS_DELETE_URL}"
        data = {"id": comment_id}
        return await self.post(url, json=data)

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
        return await self.post(url, json=data)

    async def unlike_moment(self, moment_id: int) -> dict[str, Any]:
        """Unlike a moment.

        Args:
            moment_id: Moment ID

        Returns:
            Unlike result data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.LIKES_DELETE_URL}"
        data = {"moment_id": moment_id}
        return await self.post(url, json=data)

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
        url = f"{Config.MOMENTS_API_BASE}{Config.MESSAGING_REGISTER_URL}"
        data = {"id": device_id, "type": device_type}
        if user_id:
            data["user_id"] = user_id
        if old_device_id:
            data["old_id"] = old_device_id
        if tags:
            data["tags"] = tags
        return await self.post(url, json=data)

    async def unregister_device(self, device_id: str) -> dict[str, Any]:
        """Unregister device from push notifications.

        Args:
            device_id: Device ID

        Returns:
            Unregistration result data
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.MESSAGING_UNREGISTER_URL}"
        data = {"id": device_id}
        return await self.post(url, json=data)

    # Themes API methods
    async def get_themes(
        self, page: int = 1, language_tag: str = "en"
    ) -> dict[str, Any]:
        """Get available themes.

        Args:
            page: Page number
            language_tag: Language tag

        Returns:
            Themes data
        """
        url = f"{Config.THEMES_API_BASE}{Config.THEMES_ITEMS_URL}"
        params = {"page": page, "language_tag": language_tag}
        return await self.get(url, params=params)

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
            version_ids: List of version IDs

        Returns:
            Add result data
        """
        url = f"{Config.THEMES_API_BASE}{Config.THEMES_ADD_URL}"
        data = {
            "id": theme_id,
            "available_locales": available_locales,
            "colors": colors,
            "cta_urls": cta_urls,
            "msgid_suffix": msgid_suffix,
            "version_ids": version_ids,
        }

        return await self.post(url, json=data)

    async def remove_theme(self, theme_id: int) -> dict[str, Any]:
        """Remove a theme from user's collection.

        Args:
            theme_id: Theme ID

        Returns:
            Remove result data
        """
        url = f"{Config.THEMES_API_BASE}{Config.THEMES_REMOVE_URL}"
        data = {"id": theme_id}
        return await self.post(url, json=data)

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
        url = f"{Config.THEMES_API_BASE}{Config.THEMES_SET_URL}"
        data = {"id": theme_id}
        if previous_theme_id:
            data["previous_id"] = previous_theme_id
        return await self.post(url, json=data)

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
        url = f"{Config.THEMES_API_BASE}{Config.THEMES_DESCRIPTION_URL}"
        params = {"id": theme_id, "language_tag": language_tag}
        return await self.get(url, params=params)

    # Friendships API methods
    async def send_friend_request(self, user_id: int) -> dict[str, Any]:
        """Send a friend request to a user.

        Args:
            user_id: User ID to send friend request to

        Returns:
            Friend request response data
        """
        url = f"{Config.FRIENDSHIPS_API_BASE}{Config.FRIENDSHIPS_OFFER_URL}"
        data = {"user_id": user_id}
        return await self.post(url, json=data)

    # Friends API methods
    async def get_friends(self, page: int = 1) -> dict[str, Any]:
        """Get the authenticated user's friends list.

        Args:
            page: Page number for pagination.

        Returns:
            Friends list data including ``users`` and ``next_page``.
        """
        url = f"{Config.FRIENDS_API_BASE}{Config.FRIENDS_ITEMS_URL}"
        return await self.get(url, params={"page": page})

    async def get_all_friends(self, page: int = 1) -> dict[str, Any]:
        """Get all friends including extended friend metadata.

        Args:
            page: Page number for pagination.

        Returns:
            All friends data including a ``friends`` collection.
        """
        url = f"{Config.FRIENDS_API_BASE}{Config.FRIENDS_ALL_ITEMS_URL}"
        return await self.get(url, params={"page": page})

    async def delete_friend(self, user_id: int) -> dict[str, Any]:
        """Remove a friend.

        Args:
            user_id: YouVersion user ID of the friend to remove.

        Returns:
            Delete operation result data.
        """
        url = f"{Config.FRIENDS_API_BASE}{Config.FRIENDS_DELETE_URL}"
        return await self.post(url, json={"user_id": user_id})

    # Friendships API methods
    async def get_incoming_friend_requests(self, page: int = 1) -> dict[str, Any]:
        """Get incoming friend requests.

        Args:
            page: Page number for pagination.

        Returns:
            Incoming friend request data.
        """
        url = f"{Config.FRIENDSHIPS_API_BASE}{Config.FRIENDSHIPS_INCOMING_URL}"
        return await self.get(url, params={"page": page})

    async def get_friend_suggestions(
        self, page: int = 1, language_tag: str = "en"
    ) -> dict[str, Any]:
        """Get friend suggestions.

        Args:
            page: Page number for pagination.
            language_tag: ISO 639-1 locale (e.g. ``en``, not ``eng``).

        Returns:
            Friend suggestion data.
        """
        url = f"{Config.FRIENDSHIPS_API_BASE}{Config.FRIENDSHIPS_SUGGESTIONS_URL}"
        return await self.get(url, params={"page": page, "language_tag": language_tag})

    async def accept_friend_request(self, user_id: int) -> dict[str, Any]:
        """Accept an incoming friend request.

        Args:
            user_id: User ID of the requester to accept.

        Returns:
            Accept operation result data.
        """
        url = f"{Config.FRIENDSHIPS_API_BASE}{Config.FRIENDSHIPS_ACCEPT_URL}"
        return await self.post(url, json={"user_id": user_id})

    async def decline_friend_request(self, user_id: int) -> dict[str, Any]:
        """Decline an incoming friend request.

        Args:
            user_id: User ID of the requester to decline.

        Returns:
            Decline operation result data.
        """
        url = f"{Config.FRIENDSHIPS_API_BASE}{Config.FRIENDSHIPS_DECLINE_URL}"
        return await self.post(url, json={"user_id": user_id})

    async def dismiss_friend_suggestion(self, user_id: int) -> dict[str, Any]:
        """Dismiss a friend suggestion.

        Args:
            user_id: Suggested user ID to dismiss.

        Returns:
            Dismiss operation result data.
        """
        url = (
            f"{Config.FRIENDSHIPS_API_BASE}{Config.FRIENDSHIPS_DISMISS_SUGGESTION_URL}"
        )
        return await self.post(url, json={"user_id": user_id})

    async def get_facebook_friends(self, page: int = 1) -> dict[str, Any]:
        """Get Facebook-linked friend suggestions.

        Args:
            page: Page number for pagination.

        Returns:
            Facebook friends data.
        """
        url = f"{Config.FRIENDSHIPS_API_BASE}{Config.FRIENDSHIPS_FACEBOOK_FRIENDS_URL}"
        return await self.get(url, params={"page": page})

    async def sync_friendship_contacts(
        self, contacts: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Upload device contacts for friend matching.

        Args:
            contacts: Contact records to sync with YouVersion.

        Returns:
            Contact sync result data.
        """
        url = f"{Config.FRIENDSHIPS_API_BASE}{Config.FRIENDSHIPS_CONTACTS_URL}"
        return await self.post(url, json={"contacts": contacts})

    # Notifications API methods
    async def get_notifications(self, page: int = 1) -> dict[str, Any]:
        """Get notification feed items.

        Args:
            page: Page number for pagination.

        Returns:
            Notification items and unread counts.
        """
        url = f"{Config.NOTIFICATIONS_API_BASE}{Config.NOTIFICATIONS_ITEMS_URL}"
        return await self.get(url, params={"page": page})

    async def get_notification_settings(self) -> dict[str, Any]:
        """Get notification settings for the authenticated user.

        Returns:
            Notification settings payload.
        """
        url = f"{Config.NOTIFICATIONS_API_BASE}{Config.NOTIFICATIONS_SETTINGS_URL}"
        return await self.get(url)

    async def update_notification_settings(
        self, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update notification settings.

        Args:
            data: Settings fields to update.

        Returns:
            Updated settings data.
        """
        url = (
            f"{Config.NOTIFICATIONS_API_BASE}{Config.NOTIFICATIONS_UPDATE_SETTINGS_URL}"
        )
        return await self.post(url, json=data)

    async def update_notifications(self, data: dict[str, Any]) -> dict[str, Any]:
        """Mark notifications read or update notification state.

        Args:
            data: Notification update payload.

        Returns:
            Update result data.
        """
        url = f"{Config.NOTIFICATIONS_API_BASE}{Config.NOTIFICATIONS_UPDATE_URL}"
        return await self.post(url, json=data)

    async def get_votd_notification_settings(self) -> dict[str, Any]:
        """Get verse-of-the-day notification settings.

        Returns:
            VOTD notification settings data.
        """
        url = f"{Config.NOTIFICATIONS_API_BASE}{Config.NOTIFICATIONS_VOTD_SETTINGS_URL}"
        return await self.get(url)

    async def update_votd_notification_settings(
        self, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update verse-of-the-day notification settings.

        Args:
            data: VOTD settings fields to update.

        Returns:
            Updated VOTD settings data.
        """
        url = (
            f"{Config.NOTIFICATIONS_API_BASE}"
            f"{Config.NOTIFICATIONS_UPDATE_VOTD_SETTINGS_URL}"
        )
        return await self.post(url, json=data)

    # Share API methods
    async def invite_by_email(self, data: dict[str, Any]) -> dict[str, Any]:
        """Send a YouVersion invite email.

        Args:
            data: Invite payload (e.g. email address and message fields).

        Returns:
            Invite operation result data.
        """
        url = f"{Config.SHARE_API_BASE}{Config.SHARE_INVITE_EMAIL_URL}"
        return await self.post(url, json=data)

    async def invite_by_sms(self, data: dict[str, Any]) -> dict[str, Any]:
        """Send a YouVersion invite SMS.

        Args:
            data: Invite payload (e.g. phone number and message fields).

        Returns:
            Invite operation result data.
        """
        url = f"{Config.SHARE_API_BASE}{Config.SHARE_INVITE_SMS_URL}"
        return await self.post(url, json=data)

    # Additional moments API methods
    async def get_client_side_moments(self, page: int = 1) -> dict[str, Any]:
        """Get client-side moment items.

        Args:
            page: Page number for pagination.

        Returns:
            Client-side moments data.
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_CLIENT_SIDE_ITEMS_URL}"
        return await self.get(url, params={"page": page})

    async def get_moments_votd(
        self, language_tag: Optional[str] = None
    ) -> dict[str, Any]:
        """Get verse of the day from the moments API.

        Args:
            language_tag: Optional language tag; omit for default VOTD payload.

        Returns:
            Verse of the day data from moments service.
        """
        url = f"{Config.MOMENTS_API_BASE}{Config.MOMENTS_VOTD_URL}"
        params: dict[str, Any] = {}
        if language_tag:
            params["language_tag"] = language_tag
        return await self.get_public(url, params=params or None)
