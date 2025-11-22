from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Union

from youversion.config import Config
from youversion.models.commons import Action, BodyImage, Comment, Like, User


@dataclass
class PlanSegmentAction:
    """Actions for the Plan segment model"""

    about_plan: bool
    read_plan: bool
    show: bool


@dataclass
class PlanCompletionAction:
    """Actions for the Plan completion model"""

    about_plan: bool
    show: bool
    start_plan: bool


@dataclass
class Moment:
    """Base model for all Youversion objects"""

    id: str
    kind: str
    actions: Action
    avatar: str
    comments: Comment
    likes: Like
    moment_title: str
    owned_by_me: bool
    path: str
    time_ago: str
    user: User
    created_dt: Optional[datetime] = None
    updated_dt: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Normalize fields after initialization."""
        if self.avatar and self.avatar.startswith("//"):
            self.avatar = "https:" + self.avatar
        if self.path and self.path.startswith("/"):
            self.path = f"{Config.BASE_URL}{self.path}"

    def __repr__(self) -> str:
        """String representation of the moment."""
        title = self.moment_title[:40] if self.moment_title else ""
        return f"<{self.__class__.__name__}: {title}>"


@dataclass
class Reference:
    """Reference class for Youversion moment objects"""

    version_id: Union[str, int]
    human: str
    usfm: Union[str, list[str]]


@dataclass
class PlanModel(Moment):
    """Generic moment class for Youversion plans"""

    action_url: str
    actions: Union[PlanCompletionAction, PlanSegmentAction]
    body_images: Optional[list[BodyImage]] = field(default_factory=list)
    body_text: Optional[str] = None
    plan_id: int = 0
    subscribed: bool = False

    def __post_init__(self) -> None:
        """Normalize action_url after initialization."""
        super().__post_init__()
        if self.action_url:
            self.action_url = f"{Config.BASE_URL}{self.action_url}"
