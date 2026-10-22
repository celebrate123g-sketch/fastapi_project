
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserCreate(BaseModel):
    username: str = Field(
        min_length=2,
        max_length=100
    )

    password: str = Field(
        min_length=6,
        max_length=100
    )

    @field_validator("username")
    @classmethod
    def clean_username(cls, value: str):
        value = value.strip()

        if len(value) < 2:
            raise ValueError("Username must contain at least 2 characters.")

        return value


class UserLogin(BaseModel):
    username: str = Field(
        min_length=2,
        max_length=100
    )

    password: str = Field(
        min_length=6,
        max_length=100
    )


class UserUpdate(BaseModel):
    username: str = Field(
        min_length=2,
        max_length=100
    )

    @field_validator("username")
    @classmethod
    def clean_username(cls, value: str):
        value = value.strip()

        if len(value) < 2:
            raise ValueError("Username must contain at least 2 characters.")

        return value


class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
