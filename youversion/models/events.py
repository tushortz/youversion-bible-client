"""Events and church finder data models."""

from datetime import datetime
from typing import Any, Protocol

try:
    from typing import TypeAlias
except ImportError:
    # Python < 3.10 compatibility
    from typing import TypeAlias


class EventLocationProtocol(Protocol):
    """Protocol for event location information."""

    name: str
    address: str | None
    city: str | None
    state: str | None
    country: str | None
    latitude: float | None
    longitude: float | None

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
EventLocation: TypeAlias = EventLocationProtocol


class EventTimeProtocol(Protocol):
    """Protocol for event time information."""

    start_time: datetime | None
    end_time: datetime | None
    timezone: str | None
    recurring: str | None

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
EventTime: TypeAlias = EventTimeProtocol


class EventContentProtocol(Protocol):
    """Protocol for event content information."""

    title: str
    description: str | None
    image_url: str | None
    website_url: str | None

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
EventContent: TypeAlias = EventContentProtocol


class EventProtocol(Protocol):
    """Protocol for event information."""

    id: int
    content: EventContent
    location: EventLocation
    time: EventTime
    created_dt: datetime | None
    updated_dt: datetime | None

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Event: TypeAlias = EventProtocol


class SavedEventProtocol(Protocol):
    """Protocol for saved event information."""

    event: Event
    saved_dt: datetime | None
    comments: dict[str, Any] | None

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
SavedEvent: TypeAlias = SavedEventProtocol


class SavedEventsProtocol(Protocol):
    """Protocol for saved events list."""

    events: list[SavedEvent]
    total: int

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
SavedEvents: TypeAlias = SavedEventsProtocol


class SearchEventProtocol(Protocol):
    """Protocol for search event result."""

    event: Event
    distance: float | None
    relevance_score: float | None

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
SearchEvent: TypeAlias = SearchEventProtocol


class SearchEventsProtocol(Protocol):
    """Protocol for search events results."""

    events: list[SearchEvent]
    total: int
    query: str | None

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
SearchEvents: TypeAlias = SearchEventsProtocol


class EventConfigurationProtocol(Protocol):
    """Protocol for event configuration."""

    categories: list[dict[str, Any]]
    filters: list[dict[str, Any]]
    sort_options: list[dict[str, Any]]

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
EventConfiguration: TypeAlias = EventConfigurationProtocol
