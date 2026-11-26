
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./quotes.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


class Base(DeclarativeBase):
    pass


def migrate_user_role():
    with engine.begin() as connection:
        result = connection.exec_driver_sql(
            "PRAGMA table_info(users)"
        )

        columns = [row[1] for row in result.fetchall()]

        if columns and "role" not in columns:
            connection.exec_driver_sql(
                "ALTER TABLE users ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'user'"
            )


def migrate_comment_user_id():
    with engine.begin() as connection:
        result = connection.exec_driver_sql(
            "PRAGMA table_info(comments)"
        )

        columns = [row[1] for row in result.fetchall()]

        if columns and "user_id" not in columns:
            connection.exec_driver_sql(
                "ALTER TABLE comments ADD COLUMN user_id INTEGER REFERENCES users(id)"
            )


def migrate_quote_language():
    with engine.begin() as connection:
        result = connection.exec_driver_sql(
            "PRAGMA table_info(quotes)"
        )

        columns = [row[1] for row in result.fetchall()]

        if columns and "language" not in columns:
            connection.exec_driver_sql(
                "ALTER TABLE quotes ADD COLUMN language VARCHAR(10) NOT NULL DEFAULT 'ru'"
            )

def migrate_quote_history_language():
    with engine.begin() as connection:
        result = connection.exec_driver_sql(
            "PRAGMA table_info(quote_history)"
        )

        columns = [row[1] for row in result.fetchall()]

        if columns and "language" not in columns:
            connection.exec_driver_sql(
                "ALTER TABLE quote_history ADD COLUMN language VARCHAR(10) NOT NULL DEFAULT 'ru'"
            )

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
