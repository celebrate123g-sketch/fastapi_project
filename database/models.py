from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Column,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from database.database import Base

quote_tags = Table(
    "quote_tags",
    Base.metadata,

    Column(
        "quote_id",
        ForeignKey("quotes.id"),
        primary_key=True
    ),

    Column(
        "tag_id",
        ForeignKey("tags.id"),
        primary_key=True
    )
)


user_likes = Table(
    "user_likes",
    Base.metadata,

    Column(
        "user_id",
        ForeignKey("users.id"),
        primary_key=True
    ),

    Column(
        "quote_id",
        ForeignKey("quotes.id"),
        primary_key=True
    )
)


user_favorites = Table(
    "user_favorites",
    Base.metadata,

    Column(
        "user_id",
        ForeignKey("users.id"),
        primary_key=True
    ),

    Column(
        "quote_id",
        ForeignKey("quotes.id"),
        primary_key=True
    )
)


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

    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False
    )

    deleted_at = Column(
        DateTime,
        nullable=True
    )


    comments_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )


    image_url: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
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


    tags: Mapped[list["TagModel"]] = relationship(
        secondary=quote_tags,
        back_populates="quotes"
    )


    views_history: Mapped[list["QuoteViewModel"]] = relationship(
        cascade="all, delete-orphan"
    )


    liked_by: Mapped[list["UserModel"]] = relationship(
        secondary=user_likes,
        back_populates="liked_quotes"
    )


    favorited_by: Mapped[list["UserModel"]] = relationship(
        secondary=user_favorites,
        back_populates="favorite_quotes"
    )

    reports = relationship(
        "ReportModel",
        back_populates="quote",
        cascade="all, delete-orphan"
    )

    ratings: Mapped[list["QuoteRatingModel"]] = relationship(
        back_populates="quote",
        cascade="all, delete-orphan"
    )

    history: Mapped[list["QuoteHistoryModel"]] = relationship(
        cascade="all, delete-orphan"
    )

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True
    )

    user: Mapped["UserModel"] = relationship(
        back_populates="quotes"
    )

class NotificationModel(Base):

    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    message: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    notification_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    user: Mapped["UserModel"] = relationship(
        back_populates="notifications"
    )


class TagModel(Base):

    __tablename__ = "tags"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )


    quotes: Mapped[list["QuoteModel"]] = relationship(
        secondary=quote_tags,
        back_populates="tags"
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



class UserModel(Base):

    __tablename__ = "users"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


    liked_quotes: Mapped[list["QuoteModel"]] = relationship(
        secondary=user_likes,
        back_populates="liked_by"
    )


    favorite_quotes: Mapped[list["QuoteModel"]] = relationship(
        secondary=user_favorites,
        back_populates="favorited_by"
    )


    preferences: Mapped[list["UserPreferenceModel"]] = relationship(
        cascade="all, delete-orphan"
    )

    notifications: Mapped[list["NotificationModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    quotes: Mapped[list["QuoteModel"]] = relationship(
        back_populates="user"
    )



class UserPreferenceModel(Base):

    __tablename__ = "user_preferences"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )


    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )


    score: Mapped[int] = mapped_column(
        Integer,
        default=0
    )


    user: Mapped["UserModel"] = relationship()



class QuoteViewModel(Base):

    __tablename__ = "quote_views"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )


    quote_id: Mapped[int] = mapped_column(
        ForeignKey("quotes.id")
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


    quote: Mapped["QuoteModel"] = relationship()

class QuoteHistoryModel(Base):

    __tablename__ = "quote_history"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


    quote_id: Mapped[int] = mapped_column(
        ForeignKey("quotes.id"),
        nullable=False
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


    image_url: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


    quote: Mapped["QuoteModel"] = relationship()

class ReportModel(Base):

    __tablename__ = "reports"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    quote_id = Column(
        Integer,
        ForeignKey("quotes.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        nullable=False
    )

    reason = Column(
        String,
        nullable=False
    )

    description = Column(
        String,
        nullable=True
    )

    status = Column(
        String,
        default="Pending",
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    quote = relationship(
        "QuoteModel",
        back_populates="reports"
    )

class QuoteRatingModel(Base):

    __tablename__ = "quote_ratings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    quote_id: Mapped[int] = mapped_column(
        ForeignKey("quotes.id"),
        nullable=False
    )

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    quote: Mapped["QuoteModel"] = relationship(
        back_populates="ratings"
    )