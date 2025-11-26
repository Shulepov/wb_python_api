"""Base models for Wildberries API."""

from pydantic import BaseModel, ConfigDict


class WBBaseModel(BaseModel):
    """Base model for all WB API models."""

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )
