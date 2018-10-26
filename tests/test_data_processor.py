"""Unit tests for DataProcessor class."""

from unittest.mock import patch

import pytest

from youversion.core.data_processor import DataProcessor
from youversion.enums import MomentKinds
from youversion.models import (
    Friendship,
    Highlight,
    Reference,
    Votd,
)
from youversion.models.base import (
    PlanCompletionAction,
    PlanSegmentAction,
)
from youversion.models.commons import Action, Comment, Like, User


class TestDataProcessor:
    """Test cases for DataProcessor class."""

    def test_init(self):
        """Test DataProcessor initialization."""
        processor = DataProcessor()

        # Check that moment mapper is properly initialized
        assert MomentKinds.FRIENDSHIP.value in processor._moment_mapper
        assert MomentKinds.HIGHLIGHT.value in processor._moment_mapper
        assert MomentKinds.IMAGE.value in processor._moment_mapper
        assert MomentKinds.NOTE.value in processor._moment_mapper
        assert MomentKinds.PLAN_COMPLETION.value in processor._moment_mapper
        assert MomentKinds.PLAN_SEGMENT_COMPLETION.value in processor._moment_mapper
        assert MomentKinds.PLAN_SUBSCRIPTION.value in processor._moment_mapper

    def test_create_references(self):
        """Test creating Reference objects from raw data."""
        processor = DataProcessor()

        raw_references = [
            {"version_id": "1", "human": "John 3:16", "usfm": ["JHN.3.16"]},
            {"version_id": "2", "human": "Psalm 23:1", "usfm": ["PSA.23.1"]},
        ]

        references = processor._create_references(raw_references)

        assert len(references) == 2
        assert isinstance(references[0], Reference)
        assert references[0].version_id == "1"
        assert references[0].human == "John 3:16"
        assert references[0].usfm == "JHN.3.16"

        assert isinstance(references[1], Reference)
        assert references[1].version_id == "2"
        assert references[1].human == "Psalm 23:1"
        assert references[1].usfm == "PSA.23.1"

    def test_create_references_empty(self):
        """Test creating Reference objects from empty data."""
        processor = DataProcessor()

        references = processor._create_references([])

        assert references == []

    def test_process_common_fields(self):
        """Test processing common fields in moment objects."""
        processor = DataProcessor()

        raw_obj = {
            "id": "123",
            "comments": {
                "enabled": True,
                "count": 5,
                "strings": {"en": "Comments"},
                "all": [],
                "data": [],
            },
            "likes": {
                "enabled": True,
                "count": 10,
                "strings": {"en": "Likes"},
                "all": [],
                "data": [],
                "is_liked": False,
            },
            "user": {
                "id": "user123",
                "path": "/users/testuser",
                "user_name": "testuser",
            },
        }

        processed_obj = processor._process_common_fields(raw_obj)

        assert isinstance(processed_obj["comments"], Comment)
        assert isinstance(processed_obj["likes"], Like)
        assert isinstance(processed_obj["user"], User)
        assert processed_obj["id"] == "123"

    def test_process_common_fields_no_optional_fields(self):
        """Test processing common fields when optional fields are missing."""
        processor = DataProcessor()

        raw_obj = {"id": "123"}

        processed_obj = processor._process_common_fields(raw_obj)

        assert processed_obj["id"] == "123"
        assert "comments" not in processed_obj
        assert "likes" not in processed_obj
        assert "user" not in processed_obj

    def test_process_actions_plan_segment_completion(self):
        """Test processing actions for plan segment completion."""
        processor = DataProcessor()

        raw_obj = {
            "id": "123",
            "actions": {"about_plan": True, "read_plan": True, "show": True},
        }

        processed_obj = processor._process_actions(
            raw_obj, MomentKinds.PLAN_SEGMENT_COMPLETION.value
        )

        assert isinstance(processed_obj["actions"], PlanSegmentAction)

    def test_process_actions_plan_completion(self):
        """Test processing actions for plan completion."""
        processor = DataProcessor()

        raw_obj = {
            "id": "123",
            "actions": {"about_plan": True, "show": True, "start_plan": True},
        }

        processed_obj = processor._process_actions(
            raw_obj, MomentKinds.PLAN_COMPLETION.value
        )

        assert isinstance(processed_obj["actions"], PlanCompletionAction)

    def test_process_actions_friendship(self):
        """Test processing actions for friendship (no actions)."""
        processor = DataProcessor()

        raw_obj = {
            "id": "123",
            "actions": {
                "deletable": True,
                "editable": False,
                "read": True,
                "show": False,
            },
        }

        processed_obj = processor._process_actions(
            raw_obj, MomentKinds.FRIENDSHIP.value
        )

        # Friendship should not have actions processed
        assert processed_obj["actions"] == {"can_follow": True}

    def test_process_actions_default(self):
        """Test processing actions for default case."""
        processor = DataProcessor()

        raw_obj = {
            "id": "123",
            "actions": {
                "deletable": True,
                "editable": False,
                "read": True,
                "show": False,
            },
        }

        processed_obj = processor._process_actions(raw_obj, MomentKinds.HIGHLIGHT.value)

        assert isinstance(processed_obj["actions"], Action)

    def test_process_moments_success(self):
        """Test successful moments processing."""
        processor = DataProcessor()

        raw_data = [
            {
                "kind": MomentKinds.HIGHLIGHT.value,
                "object": {
                    "id": "123",
                    "text": "Test highlight",
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
                        "data": [],
                    },
                    "likes": {
                        "enabled": True,
                        "count": 0,
                        "strings": {"en": "Likes"},
                        "all": [],
                        "data": [],
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
                    "path": "/moments/123",
                    "time_ago": "2 hours ago",
                    "created_dt": "2023-01-01T00:00:00Z",
                    "updated_dt": "2023-01-01T00:00:00Z",
                },
            }
        ]

        moments = processor.process_moments(raw_data)

        assert len(moments) == 1
        assert isinstance(moments[0], Highlight)
        assert moments[0].id == "123"
        assert moments[0].text == "Test highlight"
        assert len(moments[0].references) == 1
        assert isinstance(moments[0].references[0], Reference)

    def test_process_moments_unknown_kind(self):
        """Test processing moments with unknown kind."""
        processor = DataProcessor()

        raw_data = [{"kind": "unknown_kind", "object": {"id": "123"}}]

        moments = processor.process_moments(raw_data)

        assert len(moments) == 0

    def test_process_moments_friendship_no_references(self):
        """Test processing friendship moments (no references)."""
        processor = DataProcessor()

        raw_data = [
            {
                "kind": MomentKinds.FRIENDSHIP.value,
                "object": {
                    "id": "123",
                    "user": {
                        "id": "user123",
                        "path": "/users/testuser",
                        "user_name": "testuser",
                    },
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
                        "data": [],
                    },
                    "likes": {
                        "enabled": True,
                        "count": 0,
                        "strings": {"en": "Likes"},
                        "all": [],
                        "data": [],
                        "is_liked": False,
                    },
                    "avatar": "//example.com/avatar.jpg",
                    "moment_title": "Test Friendship",
                    "owned_by_me": True,
                    "path": "/moments/123",
                    "time_ago": "2 hours ago",
                    "created_dt": "2023-01-01T00:00:00Z",
                    "updated_dt": "2023-01-01T00:00:00Z",
                },
            }
        ]

        moments = processor.process_moments(raw_data)

        assert len(moments) == 1
        assert isinstance(moments[0], Friendship)
        assert moments[0].id == "123"
        # Friendship should not have references processed
        assert "references" not in moments[0].__dict__

    def test_process_highlights_success(self):
        """Test successful highlights processing."""
        processor = DataProcessor()

        raw_data = [
            {
                "kind": MomentKinds.HIGHLIGHT.value,
                "object": {
                    "id": "123",
                    "text": "Test highlight",
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
                        "data": [],
                    },
                    "likes": {
                        "enabled": True,
                        "count": 0,
                        "strings": {"en": "Likes"},
                        "all": [],
                        "data": [],
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
                    "path": "/moments/123",
                    "time_ago": "2 hours ago",
                    "created_dt": "2023-01-01T00:00:00Z",
                    "updated_dt": "2023-01-01T00:00:00Z",
                },
            }
        ]

        highlights = processor.process_highlights(raw_data)

        assert len(highlights) == 1
        assert isinstance(highlights[0], Highlight)
        assert highlights[0].id == "123"
        assert highlights[0].text == "Test highlight"
        assert len(highlights[0].references) == 1
        assert isinstance(highlights[0].references[0], Reference)
        assert isinstance(highlights[0].actions, Action)

    def test_process_verse_of_the_day_success(self):
        """Test successful verse of the day processing."""
        processor = DataProcessor()

        raw_data = {
            "votd": [
                {"day": 15, "usfm": ["JHN.3.16"], "image_id": "img123"},
                {"day": 16, "usfm": ["PSA.23.1"], "image_id": "img124"},
            ]
        }

        votd = processor.process_verse_of_the_day(raw_data, day=15)

        assert isinstance(votd, Votd)
        assert votd.day == 15
        assert votd.usfm == ["JHN.3.16"]
        assert votd.image_id == "img123"

    @patch("youversion.core.data_processor.datetime")
    def test_process_verse_of_the_day_default_day(self, mock_datetime):
        """Test verse of the day processing with default day."""
        processor = DataProcessor()

        # Mock datetime.now().day to return 20
        mock_datetime.now.return_value.day = 20

        raw_data = {"votd": [{"day": 20, "usfm": ["JHN.3.16"], "image_id": "img123"}]}

        votd = processor.process_verse_of_the_day(raw_data)

        assert isinstance(votd, Votd)
        assert votd.day == 20
        assert votd.usfm == ["JHN.3.16"]

    def test_process_verse_of_the_day_day_not_found(self):
        """Test verse of the day processing when specific day not found."""
        processor = DataProcessor()

        raw_data = {"votd": [{"day": 15, "usfm": ["JHN.3.16"], "image_id": "img123"}]}

        # When specific day not found, should fallback to first available
        votd = processor.process_verse_of_the_day(raw_data, day=20)

        assert isinstance(votd, Votd)
        assert votd.day == 15
        assert votd.usfm == ["JHN.3.16"]

    def test_process_verse_of_the_day_fallback_to_first(self):
        """Test verse of the day processing fallback to first available."""
        processor = DataProcessor()

        raw_data = {"votd": [{"day": 15, "usfm": ["JHN.3.16"], "image_id": "img123"}]}

        votd = processor.process_verse_of_the_day(raw_data, day=20)

        assert isinstance(votd, Votd)
        assert votd.day == 15
        assert votd.usfm == ["JHN.3.16"]

    def test_process_verse_of_the_day_empty_data(self):
        """Test verse of the day processing with empty data."""
        processor = DataProcessor()

        raw_data = {"votd": []}

        with pytest.raises(ValueError, match="No verse of the day found for day 15"):
            processor.process_verse_of_the_day(raw_data, day=15)

    def test_process_verse_of_the_day_no_votd_key(self):
        """Test verse of the day processing when votd key is missing."""
        processor = DataProcessor()

        raw_data = {}

        with pytest.raises(ValueError, match="No verse of the day found for day 15"):
            processor.process_verse_of_the_day(raw_data, day=15)
