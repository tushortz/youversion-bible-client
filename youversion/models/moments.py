"""Moments-related data models."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Base:
    """Base moment information."""
    title: Optional[str] = None
    body: Optional[str] = None
    color: Optional[str] = None
    action_url: Optional[str] = None
    share_url: Optional[str] = None
    images: Optional[Dict[str, Any]] = None


@dataclass
class MomentExtras:
    """Moment extras information."""
    reference: Optional[str] = None
    version_id: Optional[int] = None
    usfm: Optional[str] = None
    verse_text: Optional[str] = None
    verse_range: Optional[str] = None


@dataclass
class MomentCommenting:
    """Moment commenting information."""
    enabled: bool = True
    count: int = 0


@dataclass
class MomentLiking:
    """Moment liking information."""
    enabled: bool = True
    count: int = 0
    user_liked: bool = False


@dataclass
class Moment:
    """Moment (note, highlight, bookmark) information."""
    id: int
    kind: str
    kind_color: Optional[str] = None
    base: Optional[Base] = None
    extras: Optional[MomentExtras] = None
    commenting: Optional[MomentCommenting] = None
    liking: Optional[MomentLiking] = None
    created_dt: Optional[datetime] = None
    updated_dt: Optional[datetime] = None


@dataclass
class MomentComment:
    """Moment comment information."""
    id: int
    moment_id: int
    comment: str
    user_id: int
    created_dt: Optional[datetime] = None


@dataclass
class MomentLike:
    """Moment like information."""
    id: int
    moment_id: int
    user_id: int
    created_dt: Optional[datetime] = None


@dataclass
class MomentLabel:
    """Moment label information."""
    id: int
    name: str
    color: Optional[str] = None


@dataclass
class VerseOfTheDay:
    """Verse of the day information."""
    id: int
    reference: str
    verse_text: str
    version_id: int
    language_tag: str
    date: Optional[datetime] = None


@dataclass
class MomentConfiguration:
    """Moment configuration information."""
    colors: List[Dict[str, Any]]
    labels: List[MomentLabel]
    kinds: List[Dict[str, Any]]
