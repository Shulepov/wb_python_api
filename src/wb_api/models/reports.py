"""Models for Reports API."""

from datetime import date, datetime
from enum import Enum
from pydantic import Field

from .base import WBBaseModel


# === Deduction Reports ===

class MeasurementTab(str, Enum):
    """Measurement tab."""

    PENALTY = "penalty"
    MEASUREMENT = "measurement"


class ParentSubject(WBBaseModel):
    """Parent subject (category) information."""

    parent_id: int = Field(alias="parentID")
    parent_name: str = Field(alias="parentName")


# === Report Tasks ===

class CreateResponseTaskData(WBBaseModel):
    task_id: str = Field(alias="taskId")

class ReportTaskResponse(WBBaseModel):
    """Response when creating a report task."""
    data: CreateResponseTaskData = Field(alias="data")


class StatusResponseTaskData(WBBaseModel):
    task_id: str = Field(alias="id")
    status: str  = Field(alias="status")

class ReportTaskStatus(WBBaseModel):
    """Report task status."""
    data: StatusResponseTaskData = Field(alias="data")

    @property
    def is_completed(self) -> bool:
        """Check if task is completed."""
        return self.data.status in ("purged", "canceled", "done")
    
    @property
    def is_successful(self) -> bool:
        return self.data.status == "done"

    @property
    def is_failed(self) -> bool:
        """Check if task failed."""
        return self.data.status in ("purged", "canceled")

    @property
    def is_processing(self) -> bool:
        """Check if task is still processing."""
        return self.data.status in ("processing", "new")
