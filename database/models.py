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