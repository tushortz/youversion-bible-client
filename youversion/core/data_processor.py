"""Data processor for YouVersion API responses."""

from datetime import datetime
from typing import Any, Optional

from ..enums import MomentKinds
from ..models import (
    Friendship,
    Highlight,
    Image,
    Note,
    PlanCompletion,
    PlanSegmentCompletion,
    PlanSubscription,
    Reference,
    Votd,
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

    def process_moments(self, raw_data: list[dict[str, Any]]) -> list[Moment]:
        """Process raw moments data.

        Args:
            raw_data: Raw moments data from API

        Returns:
            List of processed Moment objects
        """
        moments = []

        for item in raw_data:
            obj = item["object"]
            kind = item["kind"]
            model = self._moment_mapper.get(kind)

            if not model:
                continue

            # Process common fields
            obj = self._process_common_fields(obj)

            # Process actions
            obj = self._process_actions(obj, kind)

            # Process references for non-friendship moments
            if kind != MomentKinds.FRIENDSHIP.value:
                references = obj.get("references", [])
                obj["references"] = self._create_references(references)

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
        raise ValueError(
            f"No verse of the day found for day {requested_day if requested_day is not None else day}"
        )
