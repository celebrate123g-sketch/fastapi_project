from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LogResponse(BaseModel):
    id: int
    action: str
    quote_id: int | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )