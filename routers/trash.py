from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session

from database.database import get_db

from schemas.trash import (
    TrashQuoteResponse,
    TrashResponse
)

from services.trash_service import (
    get_trash,
    get_deleted_quote,
    restore_quote,
    delete_forever,
    empty_trash
)

router = APIRouter(
    prefix="/trash",
    tags=["Trash"]
)


@router.get(
    "",
    response_model=list[TrashQuoteResponse]
)
def trash(
    db: Session = Depends(get_db)
):

    return get_trash(db)


@router.get(
    "/{quote_id}",
    response_model=TrashQuoteResponse
)
def deleted_quote(
    quote_id: int,
    db: Session = Depends(get_db)
):

    quote = get_deleted_quote(
        db,
        quote_id
    )

    if quote is None:

        raise HTTPException(
            status_code=404,
            detail="Quote not found in trash."
        )

    return quote


@router.post(
    "/restore/{quote_id}",
    response_model=TrashQuoteResponse
)
def restore(
    quote_id: int,
    db: Session = Depends(get_db)
):

    quote = restore_quote(
        db,
        quote_id
    )

    if quote is None:

        raise HTTPException(
            status_code=404,
            detail="Quote not found in trash."
        )

    return quote


@router.delete(
    "/delete/{quote_id}",
    response_model=TrashResponse
)
def delete(
    quote_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_forever(
        db,
        quote_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Quote not found in trash."
        )

    return {
        "message": "Quote permanently deleted."
    }


@router.delete(
    "/empty",
    response_model=TrashResponse
)
def clear(
    db: Session = Depends(get_db)
):

    return empty_trash(db)