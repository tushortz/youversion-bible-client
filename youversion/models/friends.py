"""Friends and social features data models."""

from datetime import datetime
from typing import Any, Optional, Protocol

try:
    from typing import TypeAlias
except ImportError:
    # Python < 3.10 compatibility
    from typing_extensions import TypeAlias

from .common import UserBase


class ContactProtocol(Protocol):
    """Protocol for contact information."""

    email: str
    name: Optional[str]
    phone: Optional[str]

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Contact: TypeAlias = ContactProtocol


class ContactsProtocol(Protocol):
    """Protocol for contacts list."""

    contacts: list[Contact]

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Contacts: TypeAlias = ContactsProtocol


class FriendProtocol(Protocol):
    """Protocol for friend information."""

    user: UserBase
    friendship_id: Optional[int]
    created_dt: Optional[datetime]

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Friend: TypeAlias = FriendProtocol


class FriendsProtocol(Protocol):
    """Protocol for friends list."""

    friends: list[Friend]
    total: int

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Friends: TypeAlias = FriendsProtocol


class FriendOfferProtocol(Protocol):
    """Protocol for friend offer/request information."""

    id: int
    from_user: UserBase
    to_user: UserBase
    status: str
    created_dt: Optional[datetime]

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
FriendOffer: TypeAlias = FriendOfferProtocol


class OffersProtocol(Protocol):
    """Protocol for friend offers list."""

    offers: list[FriendOffer]
    total: int

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Offers: TypeAlias = OffersProtocol


class FriendableProtocol(Protocol):
    """Protocol for friendable user (suggestion)."""

    user: UserBase
    reason: Optional[str]
    mutual_friends: Optional[int]

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Friendable: TypeAlias = FriendableProtocol


class FriendablesProtocol(Protocol):
    """Protocol for friendable users list."""

    users: list[Friendable]
    total: int

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Friendables: TypeAlias = FriendablesProtocol
