"""Common data models used across different API endpoints."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class UserBase:
    """Base user information."""
    id: int
    name: str
    avatar: Optional[str] = None
    email: Optional[str] = None


@dataclass
class Avatar:
    """User avatar information."""
    url: str
    width: Optional[int] = None
    height: Optional[int] = None


@dataclass
class Images:
    """Image information."""
    url: str
    width: Optional[int] = None
    height: Optional[int] = None
    alt: Optional[str] = None


@dataclass
class Link:
    """Link information."""
    url: str
    text: Optional[str] = None
    target: Optional[str] = None


@dataclass
class Localize:
    """Localized text information."""
    text: str
    language_tag: Optional[str] = None


@dataclass
class ApiError:
    """API error information."""
    code: str
    message: str
    field: Optional[str] = None


@dataclass
class ApiErrors:
    """Multiple API errors."""
    errors: List[ApiError]


@dataclass
class PaginationInfo:
    """Pagination information."""
    page: int
    per_page: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool


@dataclass
class ApiResponse:
    """Generic API response wrapper."""
    data: Any
    pagination: Optional[PaginationInfo] = None
    errors: Optional[List[ApiError]] = None
