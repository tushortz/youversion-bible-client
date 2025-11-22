"""Data processor for YouVersion API responses."""

from datetime import datetime
from typing import Any, Optional

from ..enums import MomentKinds
from ..models import (
    Friendship, Highlight, Image, Note, PlanCompletion, PlanSegmentCompletion,
    PlanSubscription, Reference, Votd,
)
from ..models.base import Moment, PlanCompletionAction, PlanSegmentAction
from ..models.commons import Action, Comment, Like, User
from .interfaces import IDataProcessor


class DataProcessor(IDataProcessor):
    """Processes raw API responses into structured objects."""

    def __init__(self):
        """Initialize data processor with moment type mappings."""
        self._moment_mapper = {
            MomentKinds.FRIENDSHIP.value: Friendship,
            MomentKinds.HIGHLIGHT.value: Highlight,
            MomentKinds.IMAGE.value: Image,
            MomentKinds.NOTE.value: Note,
            MomentKinds.PLAN_COMPLETION.value: PlanCompletion,
            MomentKinds.PLAN_SEGMENT_COMPLETION.value: PlanSegmentCompletion,
            MomentKinds.PLAN_SUBSCRIPTION.value: PlanSubscription,
        }

    def _create_references(self, references: list[dict[str, Any]]) -> list[Reference]:
        """Create Reference objects from raw data.

        Args:
            references: List of reference dictionaries

        Returns:
            List of Reference objects
        """
        normalized: list[Reference] = []
        for ref in references:
            usfm_value = ref.get("usfm")
            # Normalize usfm to a string when a single-item list is provided
            if isinstance(usfm_value, list) and len(usfm_value) == 1:
                usfm_value = usfm_value[0]
            normalized.append(
                Reference(
                    version_id=ref["version_id"],
                    human=ref["human"],
                    usfm=usfm_value,
                )
            )
        return normalized

    def _process_common_fields(self, obj: dict[str, Any]) -> dict[str, Any]:
        """Process common fields in moment objects.

        Args:
            obj: Raw object data

        Returns:
            Processed object data
        """
        # Process comments
        comments = obj.get("comments", {})
        if comments:
            obj["comments"] = Comment(**comments)

        # Process likes
        likes = obj.get("likes", {})
        if likes:
            obj["likes"] = Like(**likes)

        # Process user
        user = obj.get("user", {})
        if user:
            obj["user"] = User(**user)

        return obj

    def _process_actions(self, obj: dict[str, Any], kind: str) -> dict[str, Any]:
        """Process actions based on moment kind.

        Args:
            obj: Raw object data
            kind: Moment kind

        Returns:
            Processed object data
        """
        actions = obj.get("actions", {})

        if kind == MomentKinds.PLAN_SEGMENT_COMPLETION.value:
            obj["actions"] = PlanSegmentAction(**actions)
        elif kind == MomentKinds.PLAN_COMPLETION.value:
            obj["actions"] = PlanCompletionAction(**actions)
        elif kind == MomentKinds.FRIENDSHIP.value:
            # Friendship doesn't have rich actions; provide minimal marker
            obj["actions"] = {"can_follow": True}
        else:
            obj["actions"] = Action(**actions)

        return obj

    def _normalize_kind_id(self, kind_id: str) -> str:
        """Normalize kind_id (e.g., 'note.v1') to kind (e.g., 'note').

        Args:
            kind_id: Kind ID from API (e.g., 'note.v1', 'highlight.v1')

        Returns:
            Normalized kind string (e.g., 'note', 'highlight')
        """
        if not kind_id:
            return ""
        # Remove version suffix (e.g., 'note.v1' -> 'note')
        return kind_id.split(".")[0]

    def process_moments(self, raw_data: list[dict[str, Any]]) -> list[Moment]:
        """Process raw moments data.

        Args:
            raw_data: Raw moments data from API

        Returns:
            List of processed Moment objects
        """
        moments = []

        for item in raw_data:
            # Extract kind from kind_id (e.g., 'note.v1' -> 'note')
            kind_id = item.get("kind_id", "")
            kind = self._normalize_kind_id(kind_id)
            model = self._moment_mapper.get(kind)

            if not model:
                continue

            # Start with base moment data
            obj = {
                "id": item.get("id"),
                "created_dt": item.get("created_dt"),
                "updated_dt": item.get("updated_dt"),
            }

            # Merge extras data if present
            extras = item.get("extras", {})
            if extras:
                # Extract user from extras
                user = extras.get("user")
                if user:
                    obj["user"] = user
                # Copy other extras fields
                for key in ["title", "content", "color", "references"]:
                    if key in extras:
                        obj[key] = extras[key]

            # Map commenting to comments format
            commenting = item.get("commenting", {})
            if commenting:
                # Convert commenting structure to comments format
                comments_data = {
                    "enabled": commenting.get("enabled", True),
                    "count": commenting.get("total", 0),
                    "strings": {},
                    "all": commenting.get("comments") or [],
                }
                obj["comments"] = comments_data

            # Map liking to likes format
            liking = item.get("liking", {})
            if liking:
                # Convert liking structure to likes format
                likes_data = {
                    "enabled": liking.get("enabled", True),
                    "count": liking.get("total", 0),
                    "strings": {},
                    "all": liking.get("likes") or [],
                    "is_liked": False,  # Default, can be set from all_users if needed
                    "user_ids": None,
                }
                # Extract user_ids from all_users if present
                all_users = liking.get("all_users")
                if all_users:
                    user_ids = [
                        u.get("id") for u in all_users if u.get("id")
                    ]
                    likes_data["user_ids"] = user_ids
                obj["likes"] = likes_data

            # Process common fields (user, comments, likes)
            obj = self._process_common_fields(obj)

            # Process actions (if present in base or elsewhere)
            base = item.get("base", {})
            if base:
                # Extract action_url or other action-related data
                action_url = base.get("action_url")
                if action_url or "actions" in obj:
                    obj = self._process_actions(obj, kind)

            # Process references for non-friendship moments
            if kind != MomentKinds.FRIENDSHIP.value:
                references = obj.get("references", [])
                if references:
                    obj["references"] = self._create_references(references)
                else:
                    obj["references"] = []

            # Create moment object
            moment = model(kind=kind, **obj)
            moments.append(moment)

        return moments

    def process_highlights(self, raw_data: list[dict[str, Any]]) -> list[Highlight]:
        """Process raw highlights data.

        Args:
            raw_data: Raw highlights data from API

        Returns:
            List of processed Highlight objects
        """
        highlights = []

        for item in raw_data:
            kind = item["kind"]
            card = item["object"]

            # Process actions
            actions = card.get("actions", {})
            card["actions"] = Action(**actions)

            # Process references
            references = card.get("references", [])
            card["references"] = self._create_references(references)

            highlight = Highlight(kind=kind, **card)
            highlights.append(highlight)

        return highlights

    def process_verse_of_the_day(
        self, raw_data: dict[str, Any], day: Optional[int] = None
    ) -> Votd:
        """Process verse of the day data.

        Args:
            raw_data: Raw verse of the day data
            day: Specific day number (optional)

        Returns:
            Processed Votd object
        """
        requested_day: Optional[int] = day
        if day is None:
            day = datetime.now().day

        votd_data = raw_data.get("votd", [])
        for ref in votd_data:
            if ref["day"] == day:
                return Votd(**ref)

        # Always fallback to first when available
        if votd_data:
            return Votd(**votd_data[0])
        # No data at all
        day_value = requested_day if requested_day is not None else day
        raise ValueError(f"No verse of the day found for day {day_value}")
