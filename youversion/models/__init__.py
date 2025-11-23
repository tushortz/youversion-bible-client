from typing import Any, Optional, Protocol

try:
    from typing import TypeAlias
except ImportError:
    # Python < 3.10 compatibility
    from typing_extensions import TypeAlias

from youversion.models.base import Moment, MomentProtocol, Reference, ReferenceProtocol

# Import new model classes
from .bible import (
    Book,
    Chapter,
    ChapterContent,
    Configuration,
    Language,
    Publisher,
    RecommendedLanguages,
    Version,
)
from .common import (
    ApiError,
    ApiErrors,
    ApiResponse,
    Avatar,
    Images,
    Link,
    Localize,
    PaginationInfo,
    UserBase,
)
from .events import (
    Event,
    EventConfiguration,
    EventContent,
    EventLocation,
    EventTime,
    SavedEvent,
    SavedEvents,
    SearchEvent,
    SearchEvents,
)
from .friends import (
    Contact,
    Contacts,
    Friend,
    Friendable,
    Friendables,
    FriendOffer,
    Friends,
    Offers,
)
from .moments import CreateMoment, ReferenceCreate


class VotdProtocol(Protocol):
    """Protocol for verse of the day objects."""

    day: int
    image_id: Optional[str]
    usfm: Optional[list[str]]

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Votd: TypeAlias = VotdProtocol


# Export all models
__all__ = [
    # Verse of the day
    "Votd",
    "VotdProtocol",
    # Reference (used for Bible references)
    "Reference",
    "ReferenceProtocol",
    # Moment Protocol (for dynamically created moments)
    "Moment",
    "MomentProtocol",
    # Bible models
    "Book",
    "Chapter",
    "ChapterContent",
    "Configuration",
    "Language",
    "Publisher",
    "RecommendedLanguages",
    "Version",
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
    # Moment creation models
    "CreateMoment",
    "ReferenceCreate",
]
