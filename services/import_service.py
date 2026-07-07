import csv
import json

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from database.models import QuoteModel


def import_json(
    db: Session,
    file: UploadFile
):
    try:
        data = json.load(file.file)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON file."
        )

    imported = 0

    for item in data:
        exists = (
            db.query(QuoteModel)
            .filter(
                QuoteModel.author == item["author"],
                QuoteModel.text == item["text"]
            )
            .first()
        )

        if exists:
            continue

        quote = QuoteModel(
            author=item["author"],
            text=item["text"],
            category=item["category"],
            favorite=item.get("favorite", False),
            likes=item.get("likes", 0),
            views=item.get("views", 0),
            comments_count=item.get("comments_count", 0),
            image_url=item.get("image_url")
        )

        db.add(quote)
        imported += 1

    db.commit()

    return {
        "message": "Import completed.",
        "imported": imported
    }


def import_csv(
    db: Session,
    file: UploadFile
):
    try:
        reader = csv.DictReader(
            file.file.read().decode("utf-8").splitlines()
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid CSV file."
        )

    imported = 0

    for row in reader:
        exists = (
            db.query(QuoteModel)
            .filter(
                QuoteModel.author == row["author"],
                QuoteModel.text == row["text"]
            )
            .first()
        )

        if exists:
            continue

        quote = QuoteModel(
            author=row["author"],
            text=row["text"],
            category=row["category"],
            favorite=row["favorite"] == "True",
            likes=int(row["likes"]),
            views=int(row["views"]),
            comments_count=int(row["comments_count"]),
            image_url=row["image_url"] or None
        )

        db.add(quote)
        imported += 1

    db.commit()

    return {
        "message": "Import completed.",
        "imported": imported
    }