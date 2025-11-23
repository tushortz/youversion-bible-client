from typing import Any, Optional, Protocol, Union

try:
    from typing import TypeAlias
except ImportError:
    # Python < 3.10 compatibility
    from typing_extensions import TypeAlias


class ReferenceProtocol(Protocol):
    """Protocol for YouVersion Bible references."""

    version_id: Union[str, int]
    human: str
    usfm: Union[str, list[str]]

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields."""
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Reference: TypeAlias = ReferenceProtocol


class MomentProtocol(Protocol):
    """Protocol for dynamically created moment objects from YouVersion API.

    This protocol describes the structure of moments returned by the API,
    allowing type checkers to understand the expected fields while
    supporting dynamically generated dataclasses.
    """

    # Core moment fields
    id: int
    kind_id: str
    kind_color: Optional[str]
    created_dt: Optional[str]  # ISO datetime string
    updated_dt: Optional[str]  # ISO datetime string

    # Base moment information
    base: Optional[dict[str, Any]]
    # base structure typically contains:
    # - title: dict with l_str and l_args
    # - body: Optional[str]
    # - images: dict with avatar, icon, body
    # - action_url: Optional[str]
    # - share_url: Optional[str]

    # Extras information (varies by moment type)
    extras: Optional[dict[str, Any]]
    # extras structure typically contains:
    # - user: dict with id, username, name, avatar
    # - title: Optional[str]
    # - content: Optional[str]
    # - color: Optional[str]
    # - references: Optional[list[dict]] with usfm, version_id, human
    # - user_status: Optional[str]
    # - system_status: Optional[str]
    # - language_tag: Optional[str]
    # - labels: Optional[list]

    # Commenting information
    commenting: Optional[dict[str, Any]]
    # commenting structure:
    # - enabled: bool
    # - total: int
    # - comments: Optional[list]

    # Liking information
    liking: Optional[dict[str, Any]]
    # liking structure:
    # - enabled: bool
    # - total: int
    # - likes: Optional[list]
    # - all_users: Optional[list]

    def __getattr__(self, name: str) -> Any:
        """Allow access to dynamically added fields.

        This enables the protocol to work with dynamically generated
        dataclasses that may have additional fields not defined here.
        """
        class_name = self.__class__.__name__
        raise AttributeError(f"'{class_name}' has no attribute '{name}'")


# Type alias for convenience
Moment: TypeAlias = MomentProtocol
