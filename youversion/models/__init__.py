from typing import List, Optional

from pydantic import BaseModel, field_validator

from youversion import _endpoints as _ep
from youversion.enums import StatusEnum
from youversion.models.base import Moment, PlanModel, Reference


class Votd(BaseModel):
    """Verse of the day object
    """
    day: int
    image_id: Optional[str]
    usfm: List[str]


class Highlight(Moment):
    """Highlight class for the Youversion moment object
    """
    references: List[Reference]


class Note(Moment):
    """Note class for the Youversion moment object"""
    content: str
    references: List[Reference]
    status: StatusEnum


class PlanSegmentCompletion(PlanModel):
    """Plan segment class for the Youversion moment"""
    percent_complete: float
    segment: int
    total_segments: int


class PlanSubscription(PlanModel):
    """Plan subscription class for the Youversion moment"""
    plan_title: str


class PlanCompletion(PlanModel):
    """Plan completion class for the Youversion moment"""
    plan_title: str


class Friendship(Moment):
    """Friendship class for the Youversion moment"""
    friend_path: str
    friend_name: str
    friend_avatar: str

    @field_validator("friend_path", mode="before")
    @classmethod
    def _friend_path(cls, friend_path: str) -> str:
        """Returns the full url to the moment path
        """
        if friend_path and friend_path.startswith("/"):
            return f"{_ep.HOME}{friend_path}"

        return friend_path

    @field_validator("friend_avatar", mode="before")
    @classmethod
    def _friend_avatar(cls, friend_avatar: str) -> str:
        """Returns the full url to the moment path
        """
        if friend_avatar and friend_avatar.startswith("//"):
            return f"https:{friend_avatar}"

        return friend_avatar


class Image(Moment):
    """Image class for the Youversion moment"""
    action_url: Optional[str]
    body_image: str
    references: List[Reference]

    @field_validator("action_url", mode="before")
    @classmethod
    def _action_url(cls, action_url: str) -> str:
        """Returns the full url to the moment avatar
        """
        if action_url:
            action_url = f"{_ep.HOME}{action_url}"

        return action_url

    @field_validator("body_image", mode="before")
    @classmethod
    def _body_image(cls, body_image: str) -> str:
        """Returns the full url to the moment avatar
        """
        if body_image and body_image.startswith("//"):
            body_image = "https:" + body_image

        return body_image
