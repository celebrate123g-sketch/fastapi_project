from database.database import Base, engine
from database.models import QuoteModel


def create_tables():
    Base.metadata.create_all(bind=engine)