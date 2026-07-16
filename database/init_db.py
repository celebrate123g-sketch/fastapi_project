from database.database import engine, Base

from database.models import (
    QuoteModel,
    TagModel,
    CommentModel,
    LogModel,
    UserModel,
    UserPreferenceModel,
    QuoteViewModel,
    QuoteHistoryModel,
    QuoteRatingModel
)


def create_tables():

    Base.metadata.create_all(
        bind=engine
    )


if __name__ == "__main__":

    create_tables()