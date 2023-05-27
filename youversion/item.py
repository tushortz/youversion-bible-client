import dataclasses as dc
from typing import List, Optional

from dateutil import parser


@dc.dataclass
class Base:
    """Base class for Youversion objects
    """
    @property
    def dict(self):
        """Converts object to dictionary

        Returns:
            dict: A dictionary representation of the object
        """
        return dc.asdict(self)


@dc.dataclass
class Votd(Base):
    """Verse of the day object
    """
    day: int
    usfm: List[str]
    image_id: Optional[str]


@dc.dataclass
class Image(Base):
    """Image class for Youversion moment objects
    """
    height: int
    width: int
    url: str


@dc.dataclass
class Moment(Base):
    """Base class for Youversion moment objects
    """

    id: str
    kind: str
    moment_title: str
    body_images: Optional[List[Image]] = None
    action_url: str
    created_dt: str
    updated_dt: str
    path: str
    avatar: str
    time_ago: str
    owned_by_me: str

    @property
    def created_date(self):
        """Converts the ``created_dt`` string to a valid date time object

        Returns:
            datetime: A valid date time object
        """
        if self.created_dt:
            return parser.parse(self.created_dt)

    @property
    def updated_date(self):
        """Converts the ``updated_dt`` string to a valid date time object

        Returns:
            datetime: A valid date time object
        """
        if self.updated_dt:
            return parser.parse(self.updated_dt)
