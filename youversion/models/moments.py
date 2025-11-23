"""Pydantic models for moment creation and updates."""

from typing import Any

from pydantic import BaseModel, Field

from ..enums import MomentKinds, StatusEnum


class ReferenceCreate(BaseModel):
    """Reference data for moment creation.

    Args:
        human: Human-readable reference (e.g., "Genesis 1:1")
        version_id: Bible version ID
        usfm: USFM reference as list of strings
    """

    human: str
    version_id: int
    usfm: list[str]


class CreateMoment(BaseModel):
    """Pydantic model for creating a moment.

    Args:
        kind: Type of moment (e.g., "note", "highlight", "bookmark")
        content: Content text (optional)
        references: List of Bible references (optional)
        title: Moment title (optional)
        status: Status (private, draft or public, optional)
        body: Body text (optional)
        color: Color hex code (optional)
        labels: List of label strings (optional)
        language_tag: Language tag (optional, e.g., "en")
    """

    kind: MomentKinds = Field(..., description="Type of moment")
    content: str = Field(..., description="Content text")
    references: list[ReferenceCreate] = Field(
        ..., description="List of Bible references"
    )
    title: str = Field(..., description="Moment title")
    status: StatusEnum = Field(
        ..., description="Status (private, draft or public)"
    )
    body: str = Field(..., description="Body text")
    color: str = Field(
        ..., description="Color hex code", min_length=6, max_length=6
    )
    labels: list[str] = Field(
        ..., description="List of labels", min_items=1, max_length=10
    )
    language_tag: str = Field(
        ...,
        description="Language tag (e.g., 'en')",
        min_length=2,
        max_length=2,
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        """Convert model to dictionary for API request.

        Args:
            **kwargs: Additional arguments for model_dump

        Returns:
            Dictionary representation of the model
        """
        # Use mode='python' to get enum values as strings
        data = super().model_dump(
            mode="python", **kwargs
        )
        # Convert enum values to their string values
        if "kind" in data and hasattr(data["kind"], "value"):
            data["kind"] = data["kind"].value
        if "status" in data and hasattr(data["status"], "value"):
            data["status"] = data["status"].value
        # Convert references to dict format if present
        if "references" in data and data["references"]:
            data["references"] = [
                ref.model_dump() if isinstance(ref, ReferenceCreate) else ref
                for ref in data["references"]
            ]
        # Remove None values to keep payload clean
        return {k: v for k, v in data.items() if v is not None}
