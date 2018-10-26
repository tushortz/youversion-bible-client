from enum import Enum


class StatusEnum(Enum):
    PRIVATE = "Private"
    PUBLIC = "Public"


class MomentKinds(Enum):
    """Enum for different types of moments in YouVersion API"""

    FRIENDSHIP = "friendship"
    HIGHLIGHT = "highlight"
    IMAGE = "image"
    NOTE = "note"
    PLAN_COMPLETION = "plan_completion"
    PLAN_SEGMENT_COMPLETION = "plan_segment_completion"
    PLAN_SUBSCRIPTION = "plan_subscription"
    BOOKMARK = "bookmark"
