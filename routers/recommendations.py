from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from database.database import get_db

from schemas.recommendation import (
    RecommendationResponse,
    SimilarQuoteResponse
)

from services.recommendation_service import (
    get_personal_recommendations,
    get_similar_quotes,
    register_view,
    register_like,
    register_favorite
)


router = APIRouter(
    prefix="/recommendations",
    tags=[
        "Recommendations"
    ]
)


@router.get(
    "/user/{user_id}",
    response_model=list[RecommendationResponse]
)
def user_recommendations(
        user_id: int,
        limit: int = 10,
        db: Session = Depends(get_db)
):

    return get_personal_recommendations(
        db,
        user_id,
        limit
    )



@router.get(
    "/similar/{quote_id}",
    response_model=list[SimilarQuoteResponse]
)
def similar_quotes(
        quote_id: int,
        limit: int = 5,
        db: Session = Depends(get_db)
):

    return get_similar_quotes(
        db,
        quote_id,
        limit
    )



@router.post(
    "/view/{user_id}/{quote_id}"
)
def view_quote(
        user_id: int,
        quote_id: int,
        db: Session = Depends(get_db)
):

    quote = register_view(
        db,
        user_id,
        quote_id
    )


    if not quote:

        return {
            "success": False
        }


    return {
        "success": True,
        "message": "Просмотр сохранён"
    }



@router.post(
    "/like/{user_id}/{quote_id}"
)
def like_quote(
        user_id: int,
        quote_id: int,
        db: Session = Depends(get_db)
):

    quote = register_like(
        db,
        user_id,
        quote_id
    )


    if not quote:

        return {
            "success": False
        }


    return {
        "success": True,
        "message": "Лайк добавлен"
    }



@router.post(
    "/favorite/{user_id}/{quote_id}"
)
def favorite_quote(
        user_id: int,
        quote_id: int,
        db: Session = Depends(get_db)
):

    quote = register_favorite(
        db,
        user_id,
        quote_id
    )


    if not quote:

        return {
            "success": False
        }


    return {
        "success": True,
        "message": "Добавлено в избранное"
    }