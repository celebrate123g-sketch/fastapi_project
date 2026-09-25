from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import UserModel
from database.models import (
    UserModel,
    user_likes,
    user_favorites,
    QuoteRatingModel
)
from schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate
)

from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

templates = Jinja2Templates(
    directory="templates"
)


@router.get("/login")
def login_page(
    request: Request
):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request
        }
    )


@router.get("/register")
def register_page(
    request: Request
):
    return templates.TemplateResponse(
        "register.html",
        {
            "request": request
        }
    )


@router.post(
    "/",
    response_model=UserResponse
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(UserModel)
        .filter(
            UserModel.username == user.username
        )
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists."
        )

    new_user = UserModel(
        username=user.username
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post(
    "/login",
    response_model=UserResponse
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(UserModel)
        .filter(
            UserModel.username == user.username
        )
        .first()
    )

    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    return existing_user


@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db)
):
    return db.query(UserModel).all()


@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = (
        db.query(UserModel)
        .filter(
            UserModel.id == user_id
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    return user

@router.get("/profile")
def profile_page(
    request: Request
):
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request
        }
    )


@router.get("/profile/data")
def profile_data(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = (
        db.query(UserModel)
        .filter(
            UserModel.id == user_id
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    likes_count = (
        db.query(user_likes)
        .filter(
            user_likes.c.user_id == user_id
        )
        .count()
    )

    favorites_count = (
        db.query(user_favorites)
        .filter(
            user_favorites.c.user_id == user_id
        )
        .count()
    )

    ratings_count = (
        db.query(QuoteRatingModel)
        .filter(
            QuoteRatingModel.user_id == user_id
        )
        .count()
    )

    return {
        "id": user.id,
        "username": user.username,
        "created_at": user.created_at,
        "likes_count": likes_count,
        "favorites_count": favorites_count,
        "ratings_count": ratings_count
    }

@router.put("/profile")
def update_profile(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(UserModel)
        .filter(
            UserModel.id == user_id
        )
        .first()
    )

    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    username_exists = (
        db.query(UserModel)
        .filter(
            UserModel.username == user.username,
            UserModel.id != user_id
        )
        .first()
    )

    if username_exists:
        raise HTTPException(
            status_code=400,
            detail="Username already exists."
        )

    existing_user.username = user.username

    db.commit()
    db.refresh(existing_user)

    return existing_user