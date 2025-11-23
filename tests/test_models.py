"""Unit tests for Pydantic models."""

from datetime import datetime

import pytest

from youversion.models import Reference, Votd
from youversion.models.moments import CreateMoment, ReferenceCreate
from youversion.enums import MomentKinds, StatusEnum


class TestVotd:
    """Test cases for Votd Protocol (used for type hints)."""

    def test_votd_protocol_exists(self):
        """Test that Votd Protocol exists."""
        from youversion.models import VotdProtocol
        assert VotdProtocol is not None


class TestReference:
    """Test cases for Reference Protocol (used for type hints)."""

    def test_reference_protocol_exists(self):
        """Test that Reference Protocol exists."""
        from youversion.models import ReferenceProtocol
        assert ReferenceProtocol is not None


class TestReferenceCreate:
    """Test cases for ReferenceCreate Pydantic model."""

    def test_reference_create_creation(self):
        """Test ReferenceCreate model creation."""
        reference_data = {
            "human": "John 3:16",
            "version_id": 1,
            "usfm": ["JHN.3.16"]
        }

        reference = ReferenceCreate(**reference_data)

        assert reference.human == "John 3:16"
        assert reference.version_id == 1
        assert reference.usfm == ["JHN.3.16"]

    def test_reference_create_model_dump(self):
        """Test ReferenceCreate model serialization."""
        reference_data = {
            "human": "John 3:16",
            "version_id": 1,
            "usfm": ["JHN.3.16"]
        }

        reference = ReferenceCreate(**reference_data)
        dumped = reference.model_dump()

        assert dumped["human"] == "John 3:16"
        assert dumped["version_id"] == 1
        assert dumped["usfm"] == ["JHN.3.16"]


class TestCreateMoment:
    """Test cases for CreateMoment Pydantic model."""

    def test_create_moment_creation(self):
        """Test CreateMoment model creation."""
        reference = ReferenceCreate(
            human="John 3:16",
            version_id=1,
            usfm=["JHN.3.16"]
        )
        moment_data = {
            "kind": MomentKinds.NOTE,
            "content": "Test content",
            "references": [reference],
            "title": "Test Title",
            "status": StatusEnum.PRIVATE,
            "body": "Test body",
            "color": "ff0000",
            "labels": ["test"],
            "language_tag": "en"
        }

        moment = CreateMoment(**moment_data)

        assert moment.kind == MomentKinds.NOTE
        assert moment.content == "Test content"
        assert len(moment.references) == 1
        assert moment.title == "Test Title"
        assert moment.status == StatusEnum.PRIVATE
        assert moment.body == "Test body"
        assert moment.color == "ff0000"
        assert moment.labels == ["test"]
        assert moment.language_tag == "en"

    def test_create_moment_model_dump(self):
        """Test CreateMoment model serialization."""
        reference = ReferenceCreate(
            human="John 3:16",
            version_id=1,
            usfm=["JHN.3.16"]
        )
        moment_data = {
            "kind": MomentKinds.NOTE,
            "content": "Test content",
            "references": [reference],
            "title": "Test Title",
            "status": StatusEnum.PRIVATE,
            "body": "Test body",
            "color": "ff0000",
            "labels": ["test"],
            "language_tag": "en"
        }

        moment = CreateMoment(**moment_data)
        dumped = moment.model_dump()

        assert dumped["kind"] == "note"
        assert dumped["content"] == "Test content"
        assert dumped["title"] == "Test Title"
        assert dumped["status"] == "private"
        assert len(dumped["references"]) == 1
        assert dumped["references"][0]["human"] == "John 3:16"

    def test_create_moment_validation(self):
        """Test CreateMoment model validation."""
        reference = ReferenceCreate(
            human="John 3:16",
            version_id=1,
            usfm=["JHN.3.16"]
        )

        # Test valid moment
        moment = CreateMoment(
            kind=MomentKinds.NOTE,
            content="Test",
            references=[reference],
            title="Title",
            status=StatusEnum.PRIVATE,
            body="Body",
            color="ff0000",
            labels=["test"],
            language_tag="en"
        )
        assert moment is not None

        # Test invalid color (too short)
        with pytest.raises(Exception):  # Pydantic validation error
            CreateMoment(
                kind=MomentKinds.NOTE,
                content="Test",
                references=[reference],
                title="Title",
                status=StatusEnum.PRIVATE,
                body="Body",
                color="ff00",  # Too short
                labels=["test"],
                language_tag="en"
            )

        # Test invalid language_tag (too short)
        with pytest.raises(Exception):  # Pydantic validation error
            CreateMoment(
                kind=MomentKinds.NOTE,
                content="Test",
                references=[reference],
                title="Title",
                status=StatusEnum.PRIVATE,
                body="Body",
                color="ff0000",
                labels=["test"],
                language_tag="e"  # Too short
            )

        # Test too many labels
        with pytest.raises(Exception):  # Pydantic validation error
            CreateMoment(
                kind=MomentKinds.NOTE,
                content="Test",
                references=[reference],
                title="Title",
                status=StatusEnum.PRIVATE,
                body="Body",
                color="ff0000",
                labels=["test"] * 11,  # Too many
                language_tag="en"
            )
