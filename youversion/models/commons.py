from dataclasses import dataclass
from typing import Any, Optional, Union

from youversion.config import Config


@dataclass
class ReactionModel:
    """Base model for several actions"""

    enabled: bool
    count: int
    strings: dict[str, Any]
    all: list[Any]


@dataclass
class BodyImage:
    """Image class for Youversion moment objects"""

    height: int
    width: int
    url: str

    def __post_init__(self) -> None:
        """Normalize URL after initialization."""
        if self.url and self.url.startswith("//"):
            self.url = "https:" + self.url


@dataclass
class Action:
    """Action class for the Youversion moment object"""

    deletable: bool = True
    editable: bool = False
    read: bool = True
    show: bool = False


@dataclass
class User:
    """User model for the YouVersion object"""

    id: Optional[Union[str, int]]
    path: str
    user_name: Optional[str] = None

    def __post_init__(self) -> None:
        """Normalize path after initialization."""
        if self.path:
            self.path = f"{Config.BASE_URL}{self.path}"


@dataclass
class Comment(ReactionModel):
    """Comment class inheriting from ReactionModel"""


@dataclass
class Like(ReactionModel):
    """Comment class inheriting fields from ReactionModel"""

    is_liked: bool
    user_ids: Optional[list[int]] = None
