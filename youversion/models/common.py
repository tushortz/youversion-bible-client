"""Common data models used across different API endpoints."""

from typing import Any, Protocol

try:
    from typing import TypeAlias
except ImportError:
    # Python < 3.10 compatibility
    from typing import TypeAlias


class UserBaseProtocol(Protocol):
    """Protocol for base user information."""

    id: int
    name: str
    avatar: str | None
    email: str | None

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
UserBase: TypeAlias = UserBaseProtocol


class AvatarProtocol(Protocol):
    """Protocol for user avatar information."""

    url: str
    width: int | None
    height: int | None

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Avatar: TypeAlias = AvatarProtocol


class ImagesProtocol(Protocol):
    """Protocol for image information."""

    url: str
    width: int | None
    height: int | None
    alt: str | None

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Images: TypeAlias = ImagesProtocol


class LinkProtocol(Protocol):
    """Protocol for link information."""

    url: str
    text: str | None
    target: str | None

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Link: TypeAlias = LinkProtocol


class LocalizeProtocol(Protocol):
    """Protocol for localized text information."""

    text: str
    language_tag: str | None

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Localize: TypeAlias = LocalizeProtocol


class ApiErrorProtocol(Protocol):
    """Protocol for API error information."""

    code: str
    message: str
    field: str | None

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
ApiError: TypeAlias = ApiErrorProtocol


class ApiErrorsProtocol(Protocol):
    """Protocol for multiple API errors."""

    errors: list[ApiError]

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
ApiErrors: TypeAlias = ApiErrorsProtocol


class PaginationInfoProtocol(Protocol):
    """Protocol for pagination information."""

    page: int
    per_page: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
PaginationInfo: TypeAlias = PaginationInfoProtocol


class ApiResponseProtocol(Protocol):
    """Protocol for generic API response wrapper."""

    data: Any
    pagination: PaginationInfo | None
    errors: list[ApiError] | None

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
ApiResponse: TypeAlias = ApiResponseProtocol
