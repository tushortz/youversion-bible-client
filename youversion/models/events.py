"""Events and church finder data models."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class EventLocation:
    """Event location information."""
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@dataclass
class EventTime:
    """Event time information."""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    timezone: Optional[str] = None
    recurring: Optional[str] = None


@dataclass
class EventContent:
    """Event content information."""
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    website_url: Optional[str] = None


@dataclass
class Event:
    """Event information."""
    id: int
    content: EventContent
    location: EventLocation
    time: EventTime
    created_dt: Optional[datetime] = None
    updated_dt: Optional[datetime] = None


@dataclass
class SavedEvent:
    """Saved event information."""
    event: Event
    saved_dt: Optional[datetime] = None
    comments: Optional[Dict[str, Any]] = None


@dataclass
class SavedEvents:
    """Saved events list."""
    events: List[SavedEvent]
    total: int


@dataclass
class SearchEvent:
    """Search event result."""
    event: Event
    distance: Optional[float] = None
    relevance_score: Optional[float] = None


@dataclass
class SearchEvents:
    """Search events results."""
    events: List[SearchEvent]
    total: int
    query: Optional[str] = None


@dataclass
class EventConfiguration:
    """Event configuration."""
    categories: List[Dict[str, Any]]
    filters: List[Dict[str, Any]]
    sort_options: List[Dict[str, Any]]
