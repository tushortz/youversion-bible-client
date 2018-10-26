"""Friends and social features data models."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from .common import UserBase


@dataclass
class Contact:
    """Contact information."""
    email: str
    name: Optional[str] = None
    phone: Optional[str] = None


@dataclass
class Contacts:
    """Contacts list."""
    contacts: List[Contact]


@dataclass
class Friend:
    """Friend information."""
    user: UserBase
    friendship_id: Optional[int] = None
    created_dt: Optional[datetime] = None


@dataclass
class Friends:
    """Friends list."""
    friends: List[Friend]
    total: int


@dataclass
class FriendOffer:
    """Friend offer/request information."""
    id: int
    from_user: UserBase
    to_user: UserBase
    status: str
    created_dt: Optional[datetime] = None


@dataclass
class Offers:
    """Friend offers list."""
    offers: List[FriendOffer]
    total: int


@dataclass
class Friendable:
    """Friendable user (suggestion)."""
    user: UserBase
    reason: Optional[str] = None
    mutual_friends: Optional[int] = None


@dataclass
class Friendables:
    """Friendable users list."""
    users: List[Friendable]
    total: int
