
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NotificationBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    message: str = Field(min_length=1, max_length=2000)
    notification_type: str = Field(min_length=1, max_length=50)


class NotificationCreate(NotificationBase):
    user_id: int = Field(gt=0)


class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
