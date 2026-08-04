from difflib import SequenceMatcher

from sqlalchemy.orm import Session

from database.models import QuoteModel


SIMILARITY_THRESHOLD = 90


def calculate_similarity(
    text1: str,
    text2: str
) -> float:

    return round(

        SequenceMatcher(

            None,

            text1.lower().strip(),

            text2.lower().strip()

        ).ratio() * 100,

        2

    )


def find_duplicate_quote(
    db: Session,
    text: str,
    exclude_id: int | None = None
):

    query = (

        db.query(
            QuoteModel
        )

        .filter(
            QuoteModel.is_deleted == False
        )

    )

    if exclude_id is not None:

        query = query.filter(
            QuoteModel.id != exclude_id
        )

    quotes = query.all()

    best_quote = None
    best_similarity = 0

    for quote in quotes:

        similarity = calculate_similarity(
            text,
            quote.text
        )

        if similarity > best_similarity:

            best_similarity = similarity
            best_quote = quote

    if (

        best_quote is None

        or

        best_similarity < SIMILARITY_THRESHOLD

    ):

        return None

    return {

        "quote": best_quote,

        "similarity": round(
            best_similarity,
            2
        )

    }