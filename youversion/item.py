import dataclasses as dc
from typing import Dict, List, Optional

from dateutil import parser
from youversion._endpoints import HOME


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
class Reference(Base):
    """Reference class for Youversion moment objects
    """

    version_id: str
    human: str
    usfm: List[str]


@dc.dataclass
class Moment(Base):
    """Base class for Youversion moment objects
    """

    id: str
    kind: str
    moment_title: str
    created_dt: str
    updated_dt: str
    path: str
    avatar: str
    time_ago: str
    owned_by_me: bool
    actions: Optional[Dict]
    body_images: Optional[List[Image]] = None
    action_url: Optional[str] = None
    references: Optional[List[Reference]] = None

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

    @property
    def moment_url(self):
        """Generates the full url to the moment object

        Returns:
            str: the full url to the moment object
        """
        if self.path:
            return f"{HOME}{self.path}"


@dc.dataclass
class Highlight(Moment):
    """Highlight class for the Youversion moment object
    """
    pass


@dc.dataclass
class Action(Base):
    """Action class for the Youversion moment object
    """
    show: bool = False
    editable: bool = False
    deletable: bool = True
    read: bool = True
