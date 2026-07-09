from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from schemas.tag import TagCreate
from services.tag_service import (
    add_tag_to_quote,
    create_tag,
    delete_tag,
    get_all_tags,
    get_quote_tags,
    get_tag_by_id,
    remove_tag_from_quote,
)

router = APIRouter(
    tags=["Tags"]
)


@router.post("/tags")
def add_tag(
    tag: TagCreate,
    db: Session = Depends(get_db)
):
    return create_tag(
        db,
        tag.name
    )


@router.get("/tags")
def read_tags(
    db: Session = Depends(get_db)
):
    return get_all_tags(db)


@router.get("/tags/{tag_id}")
def read_tag(
    tag_id: int,
    db: Session = Depends(get_db)
):
    return get_tag_by_id(
        db,
        tag_id
    )


@router.delete("/tags/{tag_id}")
def remove_tag(
    tag_id: int,
    db: Session = Depends(get_db)
):
    return delete_tag(
        db,
        tag_id
    )


@router.post("/quotes/{quote_id}/tags/{tag_id}")
def attach_tag(
    quote_id: int,
    tag_id: int,
    db: Session = Depends(get_db)
):
    return add_tag_to_quote(
        db,
        quote_id,
        tag_id
    )


@router.delete("/quotes/{quote_id}/tags/{tag_id}")
def detach_tag(
    quote_id: int,
    tag_id: int,
    db: Session = Depends(get_db)
):
    return remove_tag_from_quote(
        db,
        quote_id,
        tag_id
    )


@router.get("/quotes/{quote_id}/tags")
def read_quote_tags(
    quote_id: int,
    db: Session = Depends(get_db)
):
    return get_quote_tags(
        db,
        quote_id
    )