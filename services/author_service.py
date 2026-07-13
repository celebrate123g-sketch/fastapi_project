from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from database.models import QuoteModel


def get_all_authors(
    db: Session
):

    authors = (
        db.query(
            QuoteModel.author,
            func.count(
                QuoteModel.id
            ).label("quotes"),
            func.sum(
                QuoteModel.likes
            ).label("likes"),
            func.sum(
                QuoteModel.views
            ).label("views"),
            func.sum(
                func.cast(
                    QuoteModel.favorite,
                    db.bind.dialect.type_descriptor(
                        QuoteModel.favorite.type
                    )
                )
            ).label("favorites")
        )
        .group_by(
            QuoteModel.author
        )
        .order_by(
            QuoteModel.author
        )
        .all()
    )


    result = []


    for author in authors:

        result.append(
            {
                "author": author.author,
                "quotes": author.quotes,
                "likes": author.likes or 0,
                "views": author.views or 0,
                "favorites": author.favorites or 0
            }
        )


    return result



def get_top_authors(
    db: Session,
    sort: str = "likes"
):

    authors = get_all_authors(db)


    if sort == "likes":

        authors.sort(
            key=lambda item: item["likes"],
            reverse=True
        )

    elif sort == "views":

        authors.sort(
            key=lambda item: item["views"],
            reverse=True
        )

    elif sort == "quotes":

        authors.sort(
            key=lambda item: item["quotes"],
            reverse=True
        )


    return authors



def get_author(
    db: Session,
    author: str
):

    quotes = (
        db.query(
            QuoteModel
        )
        .filter(
            QuoteModel.author == author
        )
        .all()
    )


    if not quotes:
        return None


    likes = sum(
        quote.likes
        for quote in quotes
    )


    views = sum(
        quote.views
        for quote in quotes
    )


    favorites = sum(
        1
        for quote in quotes
        if quote.favorite
    )


    comments = sum(
        quote.comments_count
        for quote in quotes
    )


    return {

        "author": author,

        "statistics": {

            "quotes": len(quotes),

            "likes": likes,

            "views": views,

            "favorites": favorites,

            "comments": comments
        },

        "quotes": quotes
    }



def get_author_popular_quotes(
    db: Session,
    author: str
):

    return (

        db.query(
            QuoteModel
        )

        .filter(
            QuoteModel.author == author
        )

        .order_by(
            desc(
                QuoteModel.likes
            )
        )

        .all()
    )



def get_author_random_quote(
    db: Session,
    author: str
):

    return (

        db.query(
            QuoteModel
        )

        .filter(
            QuoteModel.author == author
        )

        .order_by(
            func.random()
        )

        .first()
    )



def get_author_categories(
    db: Session,
    author: str
):

    categories = (

        db.query(

            QuoteModel.category,

            func.count(
                QuoteModel.id
            )

        )

        .filter(
            QuoteModel.author == author
        )

        .group_by(
            QuoteModel.category
        )

        .all()
    )


    result = []


    for category in categories:

        result.append(

            {

                "category": category[0],

                "quotes": category[1]

            }

        )


    return result