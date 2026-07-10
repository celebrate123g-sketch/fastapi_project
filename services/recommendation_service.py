from sqlalchemy.orm import Session
from sqlalchemy import func

from database.models import (
    QuoteModel,
    UserPreferenceModel,
    QuoteViewModel,
    UserModel
)



def add_preference_score(
        db: Session,
        user_id: int,
        category: str,
        points: int
):

    preference = (
        db.query(
            UserPreferenceModel
        )
        .filter(
            UserPreferenceModel.user_id == user_id,
            UserPreferenceModel.category == category
        )
        .first()
    )


    if preference:

        preference.score += points

    else:

        preference = UserPreferenceModel(
            user_id=user_id,
            category=category,
            score=points
        )

        db.add(preference)


    db.commit()



def register_view(
        db: Session,
        user_id: int,
        quote_id: int
):

    quote = (
        db.query(
            QuoteModel
        )
        .filter(
            QuoteModel.id == quote_id
        )
        .first()
    )


    if not quote:
        return None


    quote.views += 1


    view = QuoteViewModel(
        user_id=user_id,
        quote_id=quote_id
    )


    db.add(view)


    add_preference_score(
        db,
        user_id,
        quote.category,
        1
    )


    db.commit()


    return quote



def register_like(
        db: Session,
        user_id: int,
        quote_id: int
):

    user = (
        db.query(
            UserModel
        )
        .filter(
            UserModel.id == user_id
        )
        .first()
    )


    quote = (
        db.query(
            QuoteModel
        )
        .filter(
            QuoteModel.id == quote_id
        )
        .first()
    )


    if not user or not quote:
        return None


    if quote not in user.liked_quotes:

        user.liked_quotes.append(
            quote
        )

        quote.likes += 1


    add_preference_score(
        db,
        user_id,
        quote.category,
        5
    )


    db.commit()


    return quote



def register_favorite(
        db: Session,
        user_id: int,
        quote_id: int
):

    user = (
        db.query(
            UserModel
        )
        .filter(
            UserModel.id == user_id
        )
        .first()
    )


    quote = (
        db.query(
            QuoteModel
        )
        .filter(
            QuoteModel.id == quote_id
        )
        .first()
    )


    if not user or not quote:
        return None


    if quote not in user.favorite_quotes:

        user.favorite_quotes.append(
            quote
        )


    add_preference_score(
        db,
        user_id,
        quote.category,
        10
    )


    db.commit()


    return quote



def get_personal_recommendations(
        db: Session,
        user_id: int,
        limit: int = 10
):

    preferences = (
        db.query(
            UserPreferenceModel
        )
        .filter(
            UserPreferenceModel.user_id == user_id
        )
        .order_by(
            UserPreferenceModel.score.desc()
        )
        .all()
    )


    categories = [
        item.category
        for item in preferences
    ]


    if not categories:

        quotes = (
            db.query(
                QuoteModel
            )
            .order_by(
                QuoteModel.likes.desc()
            )
            .limit(limit)
            .all()
        )

    else:

        quotes = (
            db.query(
                QuoteModel
            )
            .filter(
                QuoteModel.category.in_(
                    categories
                )
            )
            .order_by(
                (
                    QuoteModel.likes * 5
                    +
                    QuoteModel.views
                )
                .desc()
            )
            .limit(limit)
            .all()
        )


    result = []


    for quote in quotes:

        result.append(
            {
                "id": quote.id,

                "text": quote.text,

                "author": quote.author,

                "category": quote.category,

                "score":
                    quote.likes * 5
                    +
                    quote.views,

                "reason":
                    "Подобрано на основе ваших действий"
            }
        )


    return result



def get_similar_quotes(
        db: Session,
        quote_id: int,
        limit: int = 5
):

    target = (
        db.query(
            QuoteModel
        )
        .filter(
            QuoteModel.id == quote_id
        )
        .first()
    )


    if not target:
        return []


    quotes = (
        db.query(
            QuoteModel
        )
        .filter(
            QuoteModel.id != quote_id
        )
        .all()
    )


    result = []


    target_tags = {
        tag.id
        for tag in target.tags
    }


    for quote in quotes:

        similarity = 0


        if quote.category == target.category:

            similarity += 50


        quote_tags = {
            tag.id
            for tag in quote.tags
        }


        common_tags = (
            target_tags &
            quote_tags
        )


        similarity += (
            len(common_tags)
            * 25
        )


        if similarity > 0:

            result.append(
                {
                    "id": quote.id,

                    "text": quote.text,

                    "author": quote.author,

                    "category": quote.category,

                    "similarity": similarity
                }
            )


    result.sort(
        key=lambda item:
        item["similarity"],
        reverse=True
    )


    return result[:limit]