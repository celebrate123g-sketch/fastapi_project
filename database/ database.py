
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


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
