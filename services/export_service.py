
import csv
import json
import os

from sqlalchemy.orm import Session

from database.models import QuoteModel


EXPORT_DIR = "exports"

os.makedirs(EXPORT_DIR, exist_ok=True)


def export_json(db: Session):
    quotes = (
        db.query(QuoteModel)
        .filter(QuoteModel.is_deleted.is_(False))
        .all()
    )

    data = []

    for quote in quotes:
        data.append(
            {
                "id": quote.id,
                "author": quote.author,
                "text": quote.text,
                "category": quote.category,
                "favorite": quote.favorite,
                "likes": quote.likes,
                "views": quote.views,
                "comments_count": quote.comments_count,
                "image_url": quote.image_url,
                "created_at": quote.created_at.isoformat() if quote.created_at else None,
                "updated_at": quote.updated_at.isoformat() if quote.updated_at else None
            }
        )

    file_path = os.path.join(
        EXPORT_DIR,
        "quotes.json"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )

    return file_path


def export_csv(db: Session):
    quotes = (
        db.query(QuoteModel)
        .filter(QuoteModel.is_deleted.is_(False))
        .all()
    )

    file_path = os.path.join(
        EXPORT_DIR,
        "quotes.csv"
    )

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "id",
                "author",
                "text",
                "category",
                "favorite",
                "likes",
                "views",
                "comments_count",
                "image_url",
                "created_at",
                "updated_at"
            ]
        )

        for quote in quotes:
            writer.writerow(
                [
                    quote.id,
                    quote.author,
                    quote.text,
                    quote.category,
                    quote.favorite,
                    quote.likes,
                    quote.views,
                    quote.comments_count,
                    quote.image_url,
                    quote.created_at.isoformat() if quote.created_at else None,
                    quote.updated_at.isoformat() if quote.updated_at else None
                ]
            )

    return file_path
