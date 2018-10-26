from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator

from youversion.config import Config
from youversion.enums import StatusEnum
from youversion.models.base import Moment, PlanModel, Reference

# Import new model classes
from .bible import (
    Book, Chapter, ChapterContent, Configuration, Language, Publisher,
    RecommendedLanguages, Version,
)
from .common import (
    ApiError, ApiErrors, ApiResponse, Avatar, Images, Link, Localize,
    PaginationInfo, UserBase,
)
from .events import (
    Event, EventConfiguration, EventContent, EventLocation, EventTime,
    SavedEvent, SavedEvents, SearchEvent, SearchEvents,
)
from .friends import (
    Contact, Contacts, Friend, Friendable, Friendables, FriendOffer, Friends,
    Offers,
)
from .moments import (
    Base, Moment as MomentModel, MomentComment, MomentCommenting,
    MomentConfiguration, MomentExtras, MomentLabel, MomentLike, MomentLiking,
    VerseOfTheDay,
)


class Votd(BaseModel):
    """Verse of the day object"""

    day: int
    image_id: Optional[str]
    usfm: list[str]


class Highlight(Moment):
    """Highlight class for the Youversion moment object"""

    references: list[Reference]
    # Allow carrying extra text field for tests
    model_config = ConfigDict(extra="allow")


class Note(Moment):
    """Note class for the Youversion moment object"""

    content: str
    references: list[Reference]
    status: StatusEnum


class PlanSegmentCompletion(PlanModel):
    """Plan segment class for the Youversion moment"""

    percent_complete: float
    segment: int
    total_segments: int


class PlanSubscription(PlanModel):
    """Plan subscription class for the Youversion moment"""

    plan_title: str


class PlanCompletion(PlanModel):
    """Plan completion class for the Youversion moment"""

    plan_title: str


class Friendship(Moment):
    """Friendship class for the Youversion moment"""

    friend_path: str
    friend_name: str
    friend_avatar: str

    @field_validator("friend_path", mode="before")
    @classmethod
    def _friend_path(cls, friend_path: str) -> str:
        """Returns the full url to the moment path"""
        if friend_path and friend_path.startswith("/"):
            return f"{Config.BASE_URL}{friend_path}"

        return friend_path

    @field_validator("friend_avatar", mode="before")
    @classmethod
    def _friend_avatar(cls, friend_avatar: str) -> str:
        """Returns the full url to the moment path"""
        if friend_avatar and friend_avatar.startswith("//"):
            return f"https:{friend_avatar}"

        return friend_avatar


class Image(Moment):
    """Image class for the Youversion moment"""

    action_url: Optional[str]
    body_image: str
    references: list[Reference]

    @field_validator("action_url", mode="before")
    @classmethod
    def _action_url(cls, action_url: str) -> str:
        """Returns the full url to the moment avatar"""
        if action_url:
            action_url = f"{Config.BASE_URL}{action_url}"

        return action_url

    @field_validator("body_image", mode="before")
    @classmethod
    def _body_image(cls, body_image: str) -> str:
        """Returns the full url to the moment avatar"""
        if body_image and body_image.startswith("//"):
            body_image = "https:" + body_image

        return body_image


# Export all models
__all__ = [
    # Existing Pydantic models
    "Votd",
    "Highlight",
    "Note",
    "PlanSegmentCompletion",
    "PlanSubscription",
    "PlanCompletion",
    "Friendship",
    "Image",
    # New dataclass models
    # Bible models
    "Book",
    "Chapter",
    "ChapterContent",
    "Configuration",
    "Language",
    "Publisher",
    "RecommendedLanguages",
    "Version",
    # Moments models
    "Base",
    "MomentModel",
    "MomentComment",
    "MomentCommenting",
    "MomentConfiguration",
    "MomentExtras",
    "MomentLabel",
    "MomentLike",
    "MomentLiking",
    "VerseOfTheDay",
    # Friends models
    "Contact",
    "Contacts",
    "Friend",
    "FriendOffer",
    "Friendable",
    "Friendables",
    "Friends",
    "Offers",
    # Events models
    "Event",
    "EventConfiguration",
    "EventContent",
    "EventLocation",
    "EventTime",
    "SavedEvent",
    "SavedEvents",
    "SearchEvent",
    "SearchEvents",
    # Common models
    "ApiError",
    "ApiErrors",
    "ApiResponse",
    "Avatar",
    "Images",
    "Link",
    "Localize",
    "PaginationInfo",
    "UserBase",
]
