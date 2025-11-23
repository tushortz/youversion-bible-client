"""Common models for YouVersion API responses."""

from typing import Any, Optional, Protocol

try:
    from typing import TypeAlias
except ImportError:
    # Python < 3.10 compatibility
    from typing_extensions import TypeAlias


class ReactionModelProtocol(Protocol):
    """Protocol for reaction-based models (comments, likes)."""

    enabled: bool
    count: int
    strings: dict[str, Any]
    all: list[Any]

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
ReactionModel: TypeAlias = ReactionModelProtocol


class BodyImageProtocol(Protocol):
    """Protocol for body image objects."""

    height: int
    width: int
    url: str

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
BodyImage: TypeAlias = BodyImageProtocol


class ActionProtocol(Protocol):
    """Protocol for action objects."""

    deletable: bool
    editable: bool
    read: bool
    show: bool

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Action: TypeAlias = ActionProtocol


class UserProtocol(Protocol):
    """Protocol for user objects."""

    id: Optional[Any]  # Can be str or int
    path: str
    user_name: Optional[str]

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
User: TypeAlias = UserProtocol


class CommentProtocol(Protocol):
    """Protocol for comment objects."""

    enabled: bool
    count: int
    strings: dict[str, Any]
    all: list[Any]

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Comment: TypeAlias = CommentProtocol


class LikeProtocol(Protocol):
    """Protocol for like objects."""

    enabled: bool
    count: int
    strings: dict[str, Any]
    all: list[Any]
    is_liked: bool
    user_ids: Optional[list[int]]

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Like: TypeAlias = LikeProtocol
