"""Unit tests for Pydantic models."""

from datetime import datetime

from youversion.models import (
    Friendship,
    Highlight,
    Image,
    Note,
    PlanCompletion,
    PlanSegmentCompletion,
    PlanSubscription,
    Reference,
    Votd,
)
from youversion.models.base import (
    Moment,
    PlanCompletionAction,
    PlanSegmentAction,
)
from youversion.models.commons import Action, Comment, Like, User


class TestVotd:
    """Test cases for Votd model."""

    def test_votd_creation(self):
        """Test Votd model creation."""
        votd_data = {"day": 15, "usfm": ["JHN.3.16"], "image_id": "img123"}

        votd = Votd(**votd_data)

        assert votd.day == 15
        assert votd.usfm == ["JHN.3.16"]
        assert votd.image_id == "img123"

    def test_votd_optional_fields(self):
        """Test Votd model with optional fields."""
        votd_data = {"day": 15, "usfm": ["JHN.3.16"], "image_id": None}

        votd = Votd(**votd_data)

        assert votd.day == 15
        assert votd.usfm == ["JHN.3.16"]
        assert votd.image_id is None

    def test_votd_model_dump(self):
        """Test Votd model serialization."""
        votd_data = {"day": 15, "usfm": ["JHN.3.16"], "image_id": "img123"}

        votd = Votd(**votd_data)
        dumped = votd.model_dump()

        assert dumped["day"] == 15
        assert dumped["usfm"] == ["JHN.3.16"]
        assert dumped["image_id"] == "img123"


class TestReference:
    """Test cases for Reference model."""

    def test_reference_creation(self):
        """Test Reference model creation."""
        reference_data = {"version_id": "1", "human": "John 3:16", "usfm": ["JHN.3.16"]}

        reference = Reference(**reference_data)

        assert reference.version_id == "1"
        assert reference.human == "John 3:16"
        assert reference.usfm == ["JHN.3.16"]

    def test_reference_model_dump(self):
        """Test Reference model serialization."""
        reference_data = {"version_id": "1", "human": "John 3:16", "usfm": ["JHN.3.16"]}

        reference = Reference(**reference_data)
        dumped = reference.model_dump()

        assert dumped["version_id"] == "1"
        assert dumped["human"] == "John 3:16"
        assert dumped["usfm"] == ["JHN.3.16"]


class TestUser:
    """Test cases for User model."""

    def test_user_creation(self):
        """Test User model creation."""
        user_data = {
            "id": "user123",
            "path": "/users/testuser",
            "user_name": "testuser",
        }

        user = User(**user_data)

        assert user.id == "user123"
        assert user.path == "https://my.bible.com/users/testuser"
        assert user.user_name == "testuser"

    def test_user_optional_fields(self):
        """Test User model with optional fields."""
        user_data = {"id": "user123", "path": "/users/testuser", "user_name": None}

        user = User(**user_data)

        assert user.id == "user123"
        assert user.path == "https://my.bible.com/users/testuser"
        assert user.user_name is None

    def test_user_path_field(self):
        """Test User model path field validation."""
        user_data = {
            "id": "user123",
            "user_name": "testuser",
            "path": "/users/testuser",
        }

        user = User(**user_data)

        assert user.path == "https://my.bible.com/users/testuser"


class TestAction:
    """Test cases for Action model."""

    def test_action_creation(self):
        """Test Action model creation."""
        action_data = {
            "deletable": True,
            "editable": False,
            "read": True,
            "show": False,
        }

        action = Action(**action_data)

        assert action.deletable is True
        assert action.editable is False
        assert action.read is True
        assert action.show is False

    def test_action_optional_fields(self):
        """Test Action model with optional fields."""
        action_data = {"deletable": True}

        action = Action(**action_data)

        assert action.deletable is True
        assert action.editable is False  # Default value
        assert action.read is True  # Default value
        assert action.show is False  # Default value


class TestComment:
    """Test cases for Comment model."""

    def test_comment_creation(self):
        """Test Comment model creation."""
        comment_data = {
            "enabled": True,
            "count": 5,
            "strings": {"en": "Comments"},
            "all": [],
        }

        comment = Comment(**comment_data)

        assert comment.enabled is True
        assert comment.count == 5
        assert comment.strings == {"en": "Comments"}
        assert comment.all == []

    def test_comment_model_dump(self):
        """Test Comment model serialization."""
        comment_data = {
            "enabled": True,
            "count": 5,
            "strings": {"en": "Comments"},
            "all": [],
        }

        comment = Comment(**comment_data)
        dumped = comment.model_dump()

        assert dumped["enabled"] is True
        assert dumped["count"] == 5
        assert dumped["strings"] == {"en": "Comments"}
        assert dumped["all"] == []


class TestLike:
    """Test cases for Like model."""

    def test_like_creation(self):
        """Test Like model creation."""
        like_data = {
            "enabled": True,
            "count": 10,
            "strings": {"en": "Likes"},
            "all": [],
            "is_liked": False,
        }

        like = Like(**like_data)

        assert like.enabled is True
        assert like.count == 10
        assert like.strings == {"en": "Likes"}
        assert like.all == []
        assert like.is_liked is False

    def test_like_model_dump(self):
        """Test Like model serialization."""
        like_data = {
            "enabled": True,
            "count": 10,
            "strings": {"en": "Likes"},
            "all": [],
            "is_liked": False,
        }

        like = Like(**like_data)
        dumped = like.model_dump()

        assert dumped["enabled"] is True
        assert dumped["count"] == 10
        assert dumped["strings"] == {"en": "Likes"}
        assert dumped["all"] == []
        assert dumped["is_liked"] is False


class TestMoment:
    """Test cases for Moment model."""

    def test_moment_creation(self):
        """Test Moment model creation."""
        moment_data = {
            "id": "moment123",
            "kind": "highlight",
            "actions": {
                "deletable": True,
                "editable": False,
                "read": True,
                "show": False,
            },
            "avatar": "//example.com/avatar.jpg",
            "comments": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Comments"},
                "all": [],
            },
            "likes": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Likes"},
                "all": [],
                "is_liked": False,
            },
            "moment_title": "Test Moment",
            "owned_by_me": True,
            "path": "/moments/moment123",
            "time_ago": "2 hours ago",
            "user": {
                "id": "user123",
                "path": "/users/testuser",
                "user_name": "testuser",
            },
            "created_dt": datetime.now(),
            "updated_dt": datetime.now(),
        }

        moment = Moment(**moment_data)

        assert moment.id == "moment123"
        assert moment.kind == "highlight"
        assert moment.moment_title == "Test Moment"
        assert moment.owned_by_me is True
        assert moment.time_ago == "2 hours ago"

    def test_moment_optional_fields(self):
        """Test Moment model with optional fields."""
        moment_data = {
            "id": "moment123",
            "kind": "highlight",
            "actions": {
                "deletable": True,
                "editable": False,
                "read": True,
                "show": False,
            },
            "avatar": "//example.com/avatar.jpg",
            "comments": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Comments"},
                "all": [],
            },
            "likes": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Likes"},
                "all": [],
                "is_liked": False,
            },
            "moment_title": "Test Moment",
            "owned_by_me": True,
            "path": "/moments/moment123",
            "time_ago": "2 hours ago",
            "user": {
                "id": "user123",
                "path": "/users/testuser",
                "user_name": "testuser",
            },
            "created_dt": datetime.now(),
            "updated_dt": datetime.now(),
        }

        moment = Moment(**moment_data)

        assert moment.id == "moment123"
        assert moment.kind == "highlight"
        assert moment.created_dt is not None
        assert moment.updated_dt is not None

    def test_moment_model_dump(self):
        """Test Moment model serialization."""
        moment_data = {
            "id": "moment123",
            "kind": "highlight",
            "actions": {
                "deletable": True,
                "editable": False,
                "read": True,
                "show": False,
            },
            "avatar": "//example.com/avatar.jpg",
            "comments": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Comments"},
                "all": [],
            },
            "likes": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Likes"},
                "all": [],
                "is_liked": False,
            },
            "moment_title": "Test Moment",
            "owned_by_me": True,
            "path": "/moments/moment123",
            "time_ago": "2 hours ago",
            "user": {
                "id": "user123",
                "path": "/users/testuser",
                "user_name": "testuser",
            },
            "created_dt": datetime.now(),
            "updated_dt": datetime.now(),
        }

        moment = Moment(**moment_data)
        dumped = moment.model_dump()

        assert dumped["id"] == "moment123"
        assert dumped["kind"] == "highlight"
        assert dumped["moment_title"] == "Test Moment"


class TestHighlight:
    """Test cases for Highlight model."""

    def test_highlight_creation(self):
        """Test Highlight model creation."""
        highlight_data = {
            "id": "highlight123",
            "kind": "highlight",
            "references": [
                {"version_id": "1", "human": "John 3:16", "usfm": ["JHN.3.16"]}
            ],
            "actions": {
                "deletable": True,
                "editable": False,
                "read": True,
                "show": False,
            },
            "comments": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Comments"},
                "all": [],
            },
            "likes": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Likes"},
                "all": [],
                "is_liked": False,
            },
            "user": {
                "id": "user123",
                "path": "/users/testuser",
                "user_name": "testuser",
            },
            "avatar": "//example.com/avatar.jpg",
            "moment_title": "Test Highlight",
            "owned_by_me": True,
            "path": "/moments/highlight123",
            "time_ago": "2 hours ago",
            "created_dt": datetime.now(),
            "updated_dt": datetime.now(),
        }

        highlight = Highlight(**highlight_data)

        assert highlight.id == "highlight123"
        assert highlight.kind == "highlight"
        assert len(highlight.references) == 1
        assert highlight.references[0].human == "John 3:16"

    def test_highlight_optional_fields(self):
        """Test Highlight model with optional fields."""
        highlight_data = {
            "id": "highlight123",
            "kind": "highlight",
            "actions": {
                "deletable": True,
                "editable": False,
                "read": True,
                "show": False,
            },
            "avatar": "//example.com/avatar.jpg",
            "comments": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Comments"},
                "all": [],
            },
            "likes": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Likes"},
                "all": [],
                "is_liked": False,
            },
            "moment_title": "Test Highlight",
            "owned_by_me": True,
            "path": "/moments/highlight123",
            "time_ago": "2 hours ago",
            "user": {
                "id": "user123",
                "path": "/users/testuser",
                "user_name": "testuser",
            },
            "references": [],
            "created_dt": datetime.now(),
            "updated_dt": datetime.now(),
        }

        highlight = Highlight(**highlight_data)

        assert highlight.id == "highlight123"
        assert highlight.kind == "highlight"
        assert highlight.references == []


class TestNote:
    """Test cases for Note model."""

    def test_note_creation(self):
        """Test Note model creation."""
        note_data = {
            "id": "note123",
            "kind": "note",
            "content": "This is a note",
            "status": "Private",
            "references": [
                {"version_id": "1", "human": "John 3:16", "usfm": ["JHN.3.16"]}
            ],
            "actions": {
                "deletable": True,
                "editable": False,
                "read": True,
                "show": False,
            },
            "comments": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Comments"},
                "all": [],
            },
            "likes": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Likes"},
                "all": [],
                "is_liked": False,
            },
            "user": {
                "id": "user123",
                "path": "/users/testuser",
                "user_name": "testuser",
            },
            "avatar": "//example.com/avatar.jpg",
            "moment_title": "Test Note",
            "owned_by_me": True,
            "path": "/moments/note123",
            "time_ago": "2 hours ago",
            "created_dt": datetime.now(),
            "updated_dt": datetime.now(),
        }

        note = Note(**note_data)

        assert note.id == "note123"
        assert note.kind == "note"
        assert note.content == "This is a note"
        assert note.status == "Private"
        assert len(note.references) == 1

    def test_note_optional_fields(self):
        """Test Note model with optional fields."""
        note_data = {
            "id": "note123",
            "kind": "note",
            "content": "This is a note",
            "status": "Private",
            "actions": {
                "deletable": True,
                "editable": False,
                "read": True,
                "show": False,
            },
            "avatar": "//example.com/avatar.jpg",
            "comments": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Comments"},
                "all": [],
            },
            "likes": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Likes"},
                "all": [],
                "is_liked": False,
            },
            "moment_title": "Test Note",
            "owned_by_me": True,
            "path": "/moments/note123",
            "time_ago": "2 hours ago",
            "user": {
                "id": "user123",
                "path": "/users/testuser",
                "user_name": "testuser",
            },
            "references": [],
            "created_dt": datetime.now(),
            "updated_dt": datetime.now(),
        }

        note = Note(**note_data)

        assert note.id == "note123"
        assert note.kind == "note"
        assert note.content == "This is a note"
        assert note.references == []


class TestImage:
    """Test cases for Image model."""

    def test_image_creation(self):
        """Test Image model creation."""
        image_data = {
            "id": "image123",
            "kind": "image",
            "action_url": "/action/url",
            "body_image": "//example.com/image.jpg",
            "references": [
                {"version_id": "1", "human": "John 3:16", "usfm": ["JHN.3.16"]}
            ],
            "actions": {
                "deletable": True,
                "editable": False,
                "read": True,
                "show": False,
            },
            "comments": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Comments"},
                "all": [],
            },
            "likes": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Likes"},
                "all": [],
                "is_liked": False,
            },
            "user": {
                "id": "user123",
                "path": "/users/testuser",
                "user_name": "testuser",
            },
            "avatar": "//example.com/avatar.jpg",
            "moment_title": "Test Image",
            "owned_by_me": True,
            "path": "/moments/image123",
            "time_ago": "2 hours ago",
            "created_dt": datetime.now(),
            "updated_dt": datetime.now(),
        }

        image = Image(**image_data)

        assert image.id == "image123"
        assert image.kind == "image"
        assert image.action_url == "https://my.bible.com/action/url"
        assert image.body_image == "https://example.com/image.jpg"
        assert len(image.references) == 1


class TestFriendship:
    """Test cases for Friendship model."""

    def test_friendship_creation(self):
        """Test Friendship model creation."""
        friendship_data = {
            "id": "friendship123",
            "kind": "friendship",
            "friend_path": "/users/friend",
            "friend_name": "Friend User",
            "friend_avatar": "//example.com/friend.jpg",
            "actions": {
                "deletable": True,
                "editable": False,
                "read": True,
                "show": False,
            },
            "comments": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Comments"},
                "all": [],
            },
            "likes": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Likes"},
                "all": [],
                "is_liked": False,
            },
            "user": {
                "id": "user123",
                "path": "/users/testuser",
                "user_name": "testuser",
            },
            "avatar": "//example.com/avatar.jpg",
            "moment_title": "Test Friendship",
            "owned_by_me": True,
            "path": "/moments/friendship123",
            "time_ago": "2 hours ago",
            "created_dt": datetime.now(),
            "updated_dt": datetime.now(),
        }

        friendship = Friendship(**friendship_data)

        assert friendship.id == "friendship123"
        assert friendship.kind == "friendship"
        assert friendship.friend_path == "https://my.bible.com/users/friend"
        assert friendship.friend_name == "Friend User"
        assert friendship.friend_avatar == "https://example.com/friend.jpg"

    def test_friendship_no_references(self):
        """Test Friendship model without references."""
        friendship_data = {
            "id": "friendship123",
            "kind": "friendship",
            "friend_path": "/users/friend",
            "friend_name": "Friend User",
            "friend_avatar": "//example.com/friend.jpg",
            "actions": {
                "deletable": True,
                "editable": False,
                "read": True,
                "show": False,
            },
            "comments": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Comments"},
                "all": [],
            },
            "likes": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Likes"},
                "all": [],
                "is_liked": False,
            },
            "user": {
                "id": "user123",
                "path": "/users/testuser",
                "user_name": "testuser",
            },
            "avatar": "//example.com/avatar.jpg",
            "moment_title": "Test Friendship",
            "owned_by_me": True,
            "path": "/moments/friendship123",
            "time_ago": "2 hours ago",
            "created_dt": datetime.now(),
            "updated_dt": datetime.now(),
        }

        friendship = Friendship(**friendship_data)

        assert friendship.id == "friendship123"
        assert friendship.kind == "friendship"


class TestPlanSegmentCompletion:
    """Test cases for PlanSegmentCompletion model."""

    def test_plan_segment_completion_creation(self):
        """Test PlanSegmentCompletion model creation."""
        plan_data = {
            "id": "plan123",
            "kind": "plan_segment_completion",
            "percent_complete": 75.5,
            "segment": 3,
            "total_segments": 4,
            "action_url": "/plan/action",
            "actions": {"about_plan": True, "read_plan": True, "show": True},
            "body_images": [],
            "body_text": "Plan segment completed",
            "plan_id": 123,
            "subscribed": True,
            "comments": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Comments"},
                "all": [],
            },
            "likes": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Likes"},
                "all": [],
                "is_liked": False,
            },
            "user": {
                "id": "user123",
                "path": "/users/testuser",
                "user_name": "testuser",
            },
            "avatar": "//example.com/avatar.jpg",
            "moment_title": "Test Plan Segment",
            "owned_by_me": True,
            "path": "/moments/plan123",
            "time_ago": "2 hours ago",
            "created_dt": datetime.now(),
            "updated_dt": datetime.now(),
        }

        plan = PlanSegmentCompletion(**plan_data)

        assert plan.id == "plan123"
        assert plan.kind == "plan_segment_completion"
        assert plan.percent_complete == 75.5
        assert plan.segment == 3
        assert plan.total_segments == 4


class TestPlanSubscription:
    """Test cases for PlanSubscription model."""

    def test_plan_subscription_creation(self):
        """Test PlanSubscription model creation."""
        plan_data = {
            "id": "plan123",
            "kind": "plan_subscription",
            "plan_title": "Daily Bible Reading",
            "action_url": "/plan/action",
            "actions": {"about_plan": True, "read_plan": True, "show": True},
            "body_images": [],
            "body_text": "Plan subscribed",
            "plan_id": 123,
            "subscribed": True,
            "comments": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Comments"},
                "all": [],
            },
            "likes": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Likes"},
                "all": [],
                "is_liked": False,
            },
            "user": {
                "id": "user123",
                "path": "/users/testuser",
                "user_name": "testuser",
            },
            "avatar": "//example.com/avatar.jpg",
            "moment_title": "Test Plan Subscription",
            "owned_by_me": True,
            "path": "/moments/plan123",
            "time_ago": "2 hours ago",
            "created_dt": datetime.now(),
            "updated_dt": datetime.now(),
        }

        plan = PlanSubscription(**plan_data)

        assert plan.id == "plan123"
        assert plan.kind == "plan_subscription"
        assert plan.plan_title == "Daily Bible Reading"


class TestPlanCompletion:
    """Test cases for PlanCompletion model."""

    def test_plan_completion_creation(self):
        """Test PlanCompletion model creation."""
        plan_data = {
            "id": "plan123",
            "kind": "plan_completion",
            "plan_title": "Daily Bible Reading",
            "action_url": "/plan/action",
            "actions": {"about_plan": True, "show": True, "start_plan": True},
            "body_images": [],
            "body_text": "Plan completed",
            "plan_id": 123,
            "subscribed": True,
            "comments": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Comments"},
                "all": [],
            },
            "likes": {
                "enabled": True,
                "count": 0,
                "strings": {"en": "Likes"},
                "all": [],
                "is_liked": False,
            },
            "user": {
                "id": "user123",
                "path": "/users/testuser",
                "user_name": "testuser",
            },
            "avatar": "//example.com/avatar.jpg",
            "moment_title": "Test Plan Completion",
            "owned_by_me": True,
            "path": "/moments/plan123",
            "time_ago": "2 hours ago",
            "created_dt": datetime.now(),
            "updated_dt": datetime.now(),
        }

        plan = PlanCompletion(**plan_data)

        assert plan.id == "plan123"
        assert plan.kind == "plan_completion"
        assert plan.plan_title == "Daily Bible Reading"


class TestPlanSegmentAction:
    """Test cases for PlanSegmentAction model."""

    def test_plan_segment_action_creation(self):
        """Test PlanSegmentAction model creation."""
        action_data = {"about_plan": True, "read_plan": True, "show": True}

        action = PlanSegmentAction(**action_data)

        assert action.about_plan is True
        assert action.read_plan is True
        assert action.show is True

    def test_plan_segment_action_optional_fields(self):
        """Test PlanSegmentAction model with optional fields."""
        action_data = {"about_plan": True, "read_plan": False, "show": False}

        action = PlanSegmentAction(**action_data)

        assert action.about_plan is True
        # These fields are required, not optional
        assert action.read_plan is False
        assert action.show is False


class TestPlanCompletionAction:
    """Test cases for PlanCompletionAction model."""

    def test_plan_completion_action_creation(self):
        """Test PlanCompletionAction model creation."""
        action_data = {"about_plan": True, "show": True, "start_plan": True}

        action = PlanCompletionAction(**action_data)

        assert action.about_plan is True
        assert action.show is True
        assert action.start_plan is True

    def test_plan_completion_action_optional_fields(self):
        """Test PlanCompletionAction model with optional fields."""
        action_data = {"about_plan": True, "show": False, "start_plan": False}

        action = PlanCompletionAction(**action_data)

        assert action.about_plan is True
        # These fields are required, not optional
        assert action.show is False
        assert action.start_plan is False
