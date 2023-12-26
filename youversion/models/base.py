from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, field_validator

from youversion import _endpoints as _ep
from youversion.models.commons import Action, BodyImage, Comment, Like, User


class PlanSegmentAction(BaseModel):
    """Actions for the Plan segment model"""
    about_plan: bool
    read_plan: bool
    show: bool


class PlanCompletionAction(BaseModel):
    """Actions for the Plan completion model"""
    about_plan: bool
    show: bool
    start_plan: bool


class Moment(BaseModel):
    """Base model for all Youversion objects"""
    id: str
    actions: Action
    avatar: str
    comments: Comment
    created_dt: Optional[datetime]
    kind: str
    likes: Like
    moment_title: str
    owned_by_me: bool
    path: str
    time_ago: str
    updated_dt: Optional[datetime]
    user: User

    model_config = ConfigDict(
        extra='ignore',
        use_enum_values=True
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.moment_title[:40]}>"

    @field_validator("avatar", mode="before")
    @classmethod
    def _avatar(cls, avatar: str) -> str:
        """Returns the full url to the moment avatar
        """
        if avatar and avatar.startswith("//"):
            avatar = "https:" + avatar

        return avatar

    @field_validator("path", mode="before")
    @classmethod
    def _path(cls, path: str) -> str:
        """Returns the full url to the moment path
        """
        if path and path.startswith("/"):
            path = f"{_ep.HOME}{path}"

        return path


class Reference(BaseModel):
    """Reference class for Youversion moment objects
    """

    version_id: Union[str, int]
    human: str
    usfm: List[str]


class PlanModel(Moment):
    """Generic moment class for Youversion plans"""
    action_url: str
    actions: Union[PlanCompletionAction, PlanSegmentAction]
    body_images: Optional[List[BodyImage]] = []
    body_text: Optional[str]
    plan_id: int
    subscribed: bool

    @field_validator("action_url", mode="before")
    @classmethod
    def _action_url(cls, action_url: str) -> str:
        """Returns the full url to the moment avatar
        """
        if action_url:
            action_url = f"{_ep.HOME}{action_url}"

        return action_url
