"""Data processor for YouVersion API responses."""

from datetime import datetime
from typing import Any, Optional, Union

from ..models import Moment, Reference, Votd
from ..utils import create_instance_from_response
from .interfaces import IDataProcessor


class DataProcessor(IDataProcessor):
    """Processes raw API responses into structured objects."""

    def __init__(self):
        """Initialize data processor."""

    def _create_references(self, references: list[dict[str, Any]]) -> list[Reference]:
        """Create Reference objects from raw data using dynamic creation.

        Args:
            references: List of reference dictionaries

        Returns:
            List of dynamically created Reference objects
        """
        normalized: list[Reference] = []
        for ref in references:
            usfm_value = ref.get("usfm")
            # Normalize usfm to a string when a single-item list is provided
            if isinstance(usfm_value, list) and len(usfm_value) == 1:
                usfm_value = usfm_value[0]
            ref_data = {
                "version_id": ref["version_id"],
                "human": ref["human"],
                "usfm": usfm_value,
            }
            reference = create_instance_from_response("Reference", ref_data)
            normalized.append(reference)
        return normalized

    def _process_common_fields(self, obj: dict[str, Any]) -> dict[str, Any]:
        """Process common fields in moment objects using dynamic creation.

        Args:
            obj: Raw object data

        Returns:
            Processed object data
        """
        # Process comments
        comments = obj.get("comments", {})
        if comments:
            obj["comments"] = create_instance_from_response("Comment", comments)

        # Process likes
        likes = obj.get("likes", {})
        if likes:
            obj["likes"] = create_instance_from_response("Like", likes)

        # Process user
        user = obj.get("user", {})
        if user:
            obj["user"] = create_instance_from_response("User", user)

        return obj

    def process_moments(self, raw_data: list[dict[str, Any]]) -> list[Moment]:
        """Process raw moments data using dynamic Pydantic models.

        Args:
            raw_data: Raw moments data from API

        Returns:
            List of dynamically created Moment objects conforming to
            MomentProtocol
        """
        moments = []

        for item in raw_data:
            # Create a dynamic dataclass instance from the moment item
            # Use kind_id to create a unique class name
            kind_id = item.get("kind_id", "moment")
            # Sanitize kind_id for class name
            kind_base = kind_id.split(".")[0]
            class_name = f"{kind_base.replace('.', '').replace('_', '').title()}"
            moment = create_instance_from_response(class_name, item)
            moments.append(moment)

        return moments

    def process_highlights(self, raw_data: list[dict[str, Any]]) -> list[Any]:
        """Process raw highlights data using dynamic Pydantic models.

        Args:
            raw_data: Raw highlights data from API

        Returns:
            List of dynamically created Highlight objects
        """
        highlights = []

        for item in raw_data:
            # Create a dynamic dataclass instance from the highlight item
            class_name = "Highlight"
            highlight = create_instance_from_response(class_name, item)
            highlights.append(highlight)

        return highlights

    def process_verse_of_the_day(
        self, raw_data: dict[str, Any], day: Optional[int] = None
    ) -> Votd:
        """Process verse of the day data using dynamic creation.

        Args:
            raw_data: Raw verse of the day data
            day: Specific day number (optional)

        Returns:
            Dynamically created Votd object
        """
        requested_day: Optional[int] = day
        if day is None:
            day = datetime.now().day

        votd_data = raw_data.get("votd", [])
        for ref in votd_data:
            if ref["day"] == day:
                return create_instance_from_response("Votd", ref)

        # Always fallback to first when available
        if votd_data:
            return create_instance_from_response("Votd", votd_data[0])
        # No data at all
        day_value = requested_day if requested_day is not None else day
        raise ValueError(f"No verse of the day found for day {day_value}")

    def process_notes(self, raw_data: list[dict[str, Any]]) -> list[Any]:
        """Process raw notes data using dynamic Pydantic models.

        Args:
            raw_data: Raw notes data from API

        Returns:
            List of dynamically created Note objects
        """
        notes = []
        for item in raw_data:
            note = create_instance_from_response("Note", item)
            notes.append(note)
        return notes

    def process_bookmarks(self, raw_data: list[dict[str, Any]]) -> list[Any]:
        """Process raw bookmarks data using dynamic Pydantic models.

        Args:
            raw_data: Raw bookmarks data from API

        Returns:
            List of dynamically created Bookmark objects
        """
        bookmarks = []
        for item in raw_data:
            bookmark = create_instance_from_response("Bookmark", item)
            bookmarks.append(bookmark)
        return bookmarks

    def process_images(self, raw_data: list[dict[str, Any]]) -> list[Any]:
        """Process raw images data using dynamic Pydantic models.

        Args:
            raw_data: Raw images data from API

        Returns:
            List of dynamically created Image objects
        """
        images = []
        for item in raw_data:
            image = create_instance_from_response("Image", item)
            images.append(image)
        return images

    def process_plan_progress(self, raw_data: list[dict[str, Any]]) -> list[Any]:
        """Process raw plan progress data using dynamic Pydantic models.

        Args:
            raw_data: Raw plan progress data from API

        Returns:
            List of dynamically created PlanProgress objects
        """
        plan_progress = []
        for item in raw_data:
            progress = create_instance_from_response("PlanProgress", item)
            plan_progress.append(progress)
        return plan_progress

    def process_plan_subscriptions(self, raw_data: list[dict[str, Any]]) -> list[Any]:
        """Process raw plan subscriptions data using dynamic Pydantic models.

        Args:
            raw_data: Raw plan subscriptions data from API

        Returns:
            List of dynamically created PlanSubscription objects
        """
        plan_subscriptions = []
        for item in raw_data:
            subscription = create_instance_from_response("PlanSubscription", item)
            plan_subscriptions.append(subscription)
        return plan_subscriptions

    def process_badges(self, raw_data: list[dict[str, Any]]) -> list[Any]:
        """Process raw badges data using dynamic Pydantic models.

        Args:
            raw_data: Raw badges data from API

        Returns:
            List of dynamically created Badge objects
        """
        badges = []
        for item in raw_data:
            badge = create_instance_from_response("Badge", item)
            badges.append(badge)
        return badges

    def process_plan_completions(self, raw_data: list[dict[str, Any]]) -> list[Any]:
        """Process raw plan completions data using dynamic Pydantic models.

        Args:
            raw_data: Raw plan completions data from API

        Returns:
            List of dynamically created PlanCompletion objects
        """
        plan_completions = []
        for item in raw_data:
            completion = create_instance_from_response("PlanCompletion", item)
            plan_completions.append(completion)
        return plan_completions

    def process_search_bible(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw Bible search results using dynamic Pydantic models.

        Args:
            raw_data: Raw Bible search results data from API

        Returns:
            Processed search results with dynamically created objects
        """
        return create_instance_from_response("BibleSearch", raw_data)

    def process_bible_chapter(self, raw_data: dict[str, Any]) -> Any:
        """Process raw Bible chapter data using dynamic Pydantic models.

        Args:
            raw_data: Raw Bible chapter data from API

        Returns:
            Dynamically created BibleChapter object
        """
        return create_instance_from_response("BibleChapter", raw_data)

    def process_bible_version(self, raw_data: dict[str, Any]) -> Any:
        """Process raw Bible version data using dynamic Pydantic models.

        Args:
            raw_data: Raw Bible version data from API

        Returns:
            Dynamically created Version object
        """
        return create_instance_from_response("Version", raw_data)

    def process_bible_versions(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw Bible versions data using dynamic Pydantic models.

        Args:
            raw_data: Raw Bible versions data from API

        Returns:
            Processed versions data with dynamically created objects
        """
        processed_data = raw_data.copy()

        # Process versions list if it exists
        if "versions" in processed_data:
            versions = []
            for item in processed_data["versions"]:
                version = create_instance_from_response("Version", item)
                versions.append(version)
            processed_data["versions"] = versions

        # Create the main BibleVersions model
        return create_instance_from_response("BibleVersions", processed_data)

    def process_audio_chapter(
        self, raw_data: Union[dict[str, Any], list[dict[str, Any]]]
    ) -> Any:
        """Process raw audio chapter data using dynamic Pydantic models.

        Args:
            raw_data: Raw audio chapter data from API (dict or list of dicts)

        Returns:
            AudioChapter object or list of AudioChapter objects
        """
        # Handle list input
        if isinstance(raw_data, list):
            chapters = []
            for item in raw_data:
                chapter = create_instance_from_response("AudioChapter", item)
                chapters.append(chapter)
            return chapters
        # Handle dict input
        return create_instance_from_response("AudioChapter", raw_data)

    def process_audio_version(self, raw_data: dict[str, Any]) -> Any:
        """Process raw audio version data using dynamic Pydantic models.

        Args:
            raw_data: Raw audio version data from API

        Returns:
            Dynamically created AudioVersion object
        """
        return create_instance_from_response("AudioVersion", raw_data)

    def process_send_friend_request(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw friend request data using dynamic Pydantic models.

        Args:
            raw_data: Raw friend request data from API

        Returns:
            Processed friend request data with dynamically created objects
        """
        return create_instance_from_response("FriendshipRequest", raw_data)

    def process_bible_configuration(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw Bible configuration data using dynamic Pydantic models.

        Args:
            raw_data: Raw Bible configuration data from API

        Returns:
            Processed configuration data with dynamically created objects
        """
        return create_instance_from_response("BibleConfiguration", raw_data)

    def process_recommended_languages(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process recommended languages data using dynamic Pydantic models.

        Args:
            raw_data: Raw recommended languages data from API

        Returns:
            Processed languages data with dynamically created objects
        """
        return create_instance_from_response("RecommendedLanguages", raw_data)

    def process_search_plans(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw plan search results using dynamic Pydantic models.

        Args:
            raw_data: Raw plan search results data from API

        Returns:
            Processed search results with dynamically created objects
        """
        return create_instance_from_response("PlanSearch", raw_data)

    def process_search_users(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw user search results using dynamic Pydantic models.

        Args:
            raw_data: Raw user search results data from API

        Returns:
            Processed search results with dynamically created objects
        """
        return create_instance_from_response("UserSearch", raw_data)

    def process_videos(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw videos data using dynamic Pydantic models.

        Args:
            raw_data: Raw videos data from API

        Returns:
            Processed videos data with dynamically created objects
        """
        return create_instance_from_response("Videos", raw_data)

    def process_video_details(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw video details data using dynamic Pydantic models.

        Args:
            raw_data: Raw video details data from API

        Returns:
            Processed video details with dynamically created objects
        """
        return create_instance_from_response("VideoDetails", raw_data)

    def process_image_upload_url(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw image upload URL data using dynamic Pydantic models.

        Args:
            raw_data: Raw image upload URL data from API

        Returns:
            Processed upload URL data with dynamically created objects
        """
        return create_instance_from_response("ImageUploadUrl", raw_data)

    def process_search_events(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw event search results using dynamic Pydantic models.

        Args:
            raw_data: Raw event search results data from API

        Returns:
            Processed search results with dynamically created objects
        """
        return create_instance_from_response("EventSearch", raw_data)

    def process_event_details(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw event details data using dynamic Pydantic models.

        Args:
            raw_data: Raw event details data from API

        Returns:
            Processed event details with dynamically created objects
        """
        return create_instance_from_response("EventDetails", raw_data)

    def process_saved_events(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw saved events data using dynamic Pydantic models.

        Args:
            raw_data: Raw saved events data from API

        Returns:
            Processed saved events data with dynamically created objects
        """
        return create_instance_from_response("SavedEvents", raw_data)

    def process_moments_list(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw moments list data using dynamic Pydantic models.

        Args:
            raw_data: Raw moments list data from API

        Returns:
            Processed moments list with dynamically created objects
        """
        return create_instance_from_response("MomentsList", raw_data)

    def process_moment_details(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw moment details data using dynamic Pydantic models.

        Args:
            raw_data: Raw moment details data from API

        Returns:
            Processed moment details with dynamically created objects
        """
        return create_instance_from_response("MomentDetails", raw_data)

    def process_moment_colors(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw moment colors data using dynamic Pydantic models.

        Args:
            raw_data: Raw moment colors data from API

        Returns:
            Processed colors data with dynamically created objects
        """
        return create_instance_from_response("MomentColors", raw_data)

    def process_moment_labels(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw moment labels data using dynamic Pydantic models.

        Args:
            raw_data: Raw moment labels data from API

        Returns:
            Processed labels data with dynamically created objects
        """
        return create_instance_from_response("MomentLabels", raw_data)

    def process_verse_colors(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw verse colors data using dynamic Pydantic models.

        Args:
            raw_data: Raw verse colors data from API

        Returns:
            Processed verse colors data with dynamically created objects
        """
        return create_instance_from_response("VerseColors", raw_data)

    def process_moments_configuration(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process moments configuration data using dynamic Pydantic models.

        Args:
            raw_data: Raw moments configuration data from API

        Returns:
            Processed configuration data with dynamically created objects
        """
        return create_instance_from_response("MomentsConfiguration", raw_data)

    def process_themes(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw themes data using dynamic Pydantic models.

        Args:
            raw_data: Raw themes data from API

        Returns:
            Processed themes data with dynamically created objects
        """
        return create_instance_from_response("Themes", raw_data)

    def process_theme_description(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw theme description data using dynamic Pydantic models.

        Args:
            raw_data: Raw theme description data from API

        Returns:
            Processed theme description with dynamically created objects
        """
        return create_instance_from_response("ThemeDescription", raw_data)

    def process_event_configuration(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw event configuration data using dynamic Pydantic models.

        Args:
            raw_data: Raw event configuration data from API

        Returns:
            Processed configuration data with dynamically created objects
        """
        return create_instance_from_response("EventConfiguration", raw_data)

    def process_all_saved_event_ids(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw all saved event IDs data using dynamic Pydantic models.

        Args:
            raw_data: Raw all saved event IDs data from API

        Returns:
            Processed event IDs data with dynamically created objects
        """
        return create_instance_from_response("AllSavedEventIds", raw_data)

    def process_save_event(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw save event response using dynamic Pydantic models.

        Args:
            raw_data: Raw save event response data from API

        Returns:
            Processed save event response with dynamically created objects
        """
        return create_instance_from_response("SaveEvent", raw_data)

    def process_delete_saved_event(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw delete saved event response using dynamic Pydantic models.

        Args:
            raw_data: Raw delete saved event response data from API

        Returns:
            Processed delete response with dynamically created objects
        """
        return create_instance_from_response("DeleteSavedEvent", raw_data)

    def process_create_moment(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw create moment response using dynamic Pydantic models.

        Args:
            raw_data: Raw create moment response data from API

        Returns:
            Processed create moment response with dynamically created objects
        """
        return create_instance_from_response("CreateMomentResponse", raw_data)

    def process_update_moment(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw update moment response using dynamic Pydantic models.

        Args:
            raw_data: Raw update moment response data from API

        Returns:
            Processed update moment response with dynamically created objects
        """
        return create_instance_from_response("UpdateMomentResponse", raw_data)

    def process_delete_moment(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw delete moment response using dynamic Pydantic models.

        Args:
            raw_data: Raw delete moment response data from API

        Returns:
            Processed delete moment response with dynamically created objects
        """
        return create_instance_from_response("DeleteMomentResponse", raw_data)

    def process_hide_verse_colors(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw hide verse colors response using dynamic Pydantic models.

        Args:
            raw_data: Raw hide verse colors response data from API

        Returns:
            Processed hide verse colors response with dynamically created objects
        """
        return create_instance_from_response("HideVerseColors", raw_data)

    def process_create_comment(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw create comment response using dynamic Pydantic models.

        Args:
            raw_data: Raw create comment response data from API

        Returns:
            Processed create comment response with dynamically created objects
        """
        return create_instance_from_response("CreateComment", raw_data)

    def process_delete_comment(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw delete comment response using dynamic Pydantic models.

        Args:
            raw_data: Raw delete comment response data from API

        Returns:
            Processed delete comment response with dynamically created objects
        """
        return create_instance_from_response("DeleteComment", raw_data)

    def process_like_moment(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw like moment response using dynamic Pydantic models.

        Args:
            raw_data: Raw like moment response data from API

        Returns:
            Processed like moment response with dynamically created objects
        """
        return create_instance_from_response("LikeMoment", raw_data)

    def process_unlike_moment(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw unlike moment response using dynamic Pydantic models.

        Args:
            raw_data: Raw unlike moment response data from API

        Returns:
            Processed unlike moment response with dynamically created objects
        """
        return create_instance_from_response("UnlikeMoment", raw_data)

    def process_register_device(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw register device response using dynamic Pydantic models.

        Args:
            raw_data: Raw register device response data from API

        Returns:
            Processed register device response with dynamically created objects
        """
        return create_instance_from_response("RegisterDevice", raw_data)

    def process_unregister_device(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw unregister device response using dynamic Pydantic models.

        Args:
            raw_data: Raw unregister device response data from API

        Returns:
            Processed unregister device response with dynamically created objects
        """
        return create_instance_from_response("UnregisterDevice", raw_data)

    def process_add_theme(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw add theme response using dynamic Pydantic models.

        Args:
            raw_data: Raw add theme response data from API

        Returns:
            Processed add theme response with dynamically created objects
        """
        return create_instance_from_response("AddTheme", raw_data)

    def process_remove_theme(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw remove theme response using dynamic Pydantic models.

        Args:
            raw_data: Raw remove theme response data from API

        Returns:
            Processed remove theme response with dynamically created objects
        """
        return create_instance_from_response("RemoveTheme", raw_data)

    def process_set_theme(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw set theme response using dynamic Pydantic models.

        Args:
            raw_data: Raw set theme response data from API

        Returns:
            Processed set theme response with dynamically created objects
        """
        return create_instance_from_response("SetTheme", raw_data)
