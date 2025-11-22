from dataclasses import dataclass
from typing import List, Optional

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


@dataclass
class Votd:
    """Verse of the day object"""

    day: int
    image_id: Optional[str] = None
    usfm: Optional[list[str]] = None

    def __post_init__(self) -> None:
        """Initialize usfm if not provided."""
        if self.usfm is None:
            self.usfm = []


@dataclass
class Highlight(Moment):
    """Highlight class for the Youversion moment object"""

    references: list[Reference]


@dataclass
class Note(Moment):
    """Note class for the Youversion moment object"""

    content: str
    references: list[Reference]
    status: StatusEnum


@dataclass
class PlanSegmentCompletion(PlanModel):
    """Plan segment class for the Youversion moment"""

    percent_complete: float
    segment: int
    total_segments: int


@dataclass
class PlanSubscription(PlanModel):
    """Plan subscription class for the Youversion moment"""

    plan_title: str


@dataclass
class PlanCompletion(PlanModel):
    """Plan completion class for the Youversion moment"""

    plan_title: str


@dataclass
class Friendship(Moment):
    """Friendship class for the Youversion moment"""

    friend_path: str
    friend_name: str
    friend_avatar: str

    def __post_init__(self) -> None:
        """Normalize friend_path and friend_avatar after initialization."""
        super().__post_init__()
        if self.friend_path and self.friend_path.startswith("/"):
            self.friend_path = f"{Config.BASE_URL}{self.friend_path}"
        if self.friend_avatar and self.friend_avatar.startswith("//"):
            self.friend_avatar = "https:" + self.friend_avatar


@dataclass
class Image(Moment):
    """Image class for the Youversion moment"""

    action_url: Optional[str] = None
    body_image: str = ""
    references: list[Reference] = None

    def __post_init__(self) -> None:
        """Normalize action_url and body_image after initialization."""
        super().__post_init__()
        if self.action_url:
            self.action_url = f"{Config.BASE_URL}{self.action_url}"
        if self.body_image and self.body_image.startswith("//"):
            self.body_image = "https:" + self.body_image
        if self.references is None:
            self.references = []


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
