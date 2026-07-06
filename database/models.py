from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

from database.database import Base


class QuoteModel(Base):
    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    author: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    text: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    favorite: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    likes: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    views: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    comments_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    comments: Mapped[list["CommentModel"]] = relationship(
        back_populates="quote",
        cascade="all, delete-orphan"
    )


class CommentModel(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    quote_id: Mapped[int] = mapped_column(
        ForeignKey("quotes.id")
    )

    author: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    text: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    quote: Mapped["QuoteModel"] = relationship(
        back_populates="comments"
    )

class LogModel(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    quote_id: Mapped[int | None] = mapped_column(
        ForeignKey("quotes.id"),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )