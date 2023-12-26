
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, field_validator

from youversion import _endpoints as _ep


class ReactionModel(BaseModel):
    """Base model for several actions"""
    enabled: bool
    count: int
    strings: Dict[str, Any]
    all: List[Any]


class BodyImage(BaseModel):
    """Image class for Youversion moment objects
    """
    height: int
    width: int
    url: str

    @field_validator("url", mode="before")
    @classmethod
    def _url(cls, url: str) -> str:
        """Returns the full url to the moment avatar
        """
        if url and url.startswith("//"):
            url = "https:" + url

        return url


class Action(BaseModel):
    """Action class for the Youversion moment object
    """
    deletable: bool = True
    editable: bool = False
    read: bool = True
    show: bool = False


class User(BaseModel):
    """User model for the YouVersion object
    """
    id: Optional[Union[str, int]]
    path: str
    user_name: Optional[str]

    @field_validator("path", mode="before")
    @classmethod
    def _path(cls, path: str) -> str:
        """Returns the full url to the moment user
        """
        if path:
            path = f"{_ep.HOME}{path}"
        return path


class Comment(ReactionModel):
    """Comment class inheriting from ReactionModel"""


class Like(ReactionModel):
    """Comment class inheriting fields from ReactionModel"""
    is_liked: bool
    user_ids: Optional[List[int]] = None
