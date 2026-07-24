from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class ReportReason(str, Enum):
    spam = "Spam"
    offensive = "Offensive"
    incorrect = "Incorrect quote"
    duplicate = "Duplicate"
    copyright = "Copyright"
    other = "Other"


class ReportStatus(str, Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"


class ReportCreate(BaseModel):
    quote_id: int
    user_id: int
    reason: ReportReason
    description: str | None = None


class ReportResponse(BaseModel):
    id: int
    quote_id: int
    user_id: int
    reason: ReportReason
    description: str | None = None
    status: ReportStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class ReportUpdate(BaseModel):
    status: ReportStatus


class ReportStats(BaseModel):
    total_reports: int
    pending: int
    approved: int
    rejected: int