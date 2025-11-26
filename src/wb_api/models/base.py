"""Base models for Wildberries API."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class WBBaseModel(BaseModel):
    """Base model for all WB API models."""

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )


class TaskStatus(str, Enum):
    """Status of async task."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    PROCESSING = "processing"
    COMPLETED = "completed"
    DONE = "done"
    SUCCESS = "success"
    ERROR = "error"
    FAILED = "failed"
    CANCELLED = "cancelled"


class BaseTask(WBBaseModel):
    """Base model for async task."""

    task_id: str = Field(alias="taskID")
    status: TaskStatus
    created_at: datetime | None = Field(alias="createdAt", default=None)
    updated_at: datetime | None = Field(alias="updatedAt", default=None)


class BaseTaskResponse(WBBaseModel):
    """Base response when creating a task."""

    task_id: str = Field(alias="taskID")


class BaseTaskDetails(BaseTask):
    """Detailed information about task execution."""

    total_items: int = Field(alias="totalItems", default=0)
    processed_items: int = Field(alias="processedItems", default=0)
    errors_count: int = Field(alias="errorsCount", default=0)
    errors: list[dict[str, Any]] = []

    @property
    def is_completed(self) -> bool:
        """Check if task is completed (finished processing)."""
        return self.status in {
            TaskStatus.COMPLETED,
            TaskStatus.DONE,
            TaskStatus.SUCCESS,
            TaskStatus.ERROR,
            TaskStatus.FAILED,
            TaskStatus.CANCELLED,
        }

    @property
    def is_successful(self) -> bool:
        """Check if task completed successfully."""
        return self.status in {
            TaskStatus.COMPLETED,
            TaskStatus.DONE,
            TaskStatus.SUCCESS,
        }

    @property
    def has_errors(self) -> bool:
        """Check if task has errors."""
        return self.errors_count > 0 or len(self.errors) > 0

    @property
    def progress_percent(self) -> float:
        """Get completion progress in percent."""
        if self.total_items == 0:
            return 0.0
        return (self.processed_items / self.total_items) * 100
