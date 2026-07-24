from pydantic import BaseModel


class BadgeResponse(BaseModel):

    name: str

    description: str

    icon: str

    unlocked: bool


class BadgeStatistics(BaseModel):

    total_badges: int

    unlocked_badges: int

    locked_badges: int