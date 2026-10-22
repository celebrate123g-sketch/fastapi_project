
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

import bcrypt

from config.auth import create_access_token
from database.database import get_db
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
from dependencies.auth import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

templates = Jinja2Templates(
    directory="templates"
)


@router.post("/")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(UserModel)
        .filter(UserModel.username == user.username)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists."
        )

    password_hash = bcrypt.hashpw(
        user.password.encode(),
        bcrypt.gensalt()
    ).decode()

    new_user = UserModel(
        username=user.username,
        password_hash=password_hash
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(new_user.id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": new_user
    }


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(UserModel)
        .filter(UserModel.username == user.username)
        .first()
    )

    if existing_user is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password."
        )

    if not existing_user.password_hash:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password."
        )

    password_correct = bcrypt.checkpw(
        user.password.encode(),
        existing_user.password_hash.encode()
    )

    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password."
        )

    token = create_access_token(existing_user.id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": existing_user
    }


@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request}
    )


@router.get("/profile")
def profile_page(request: Request):
    return templates.TemplateResponse(
        "profile.html",
        {"request": request}
    )


@router.get("/profile/data")
def profile_data(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    likes_count = (
        db.query(user_likes)
        .filter(user_likes.c.user_id == current_user.id)
        .count()
    )

    favorites_count = (
        db.query(user_favorites)
        .filter(user_favorites.c.user_id == current_user.id)
        .count()
    )

    ratings_count = (
        db.query(QuoteRatingModel)
        .filter(QuoteRatingModel.user_id == current_user.id)
        .count()
    )

    return {
        "id": current_user.id,
        "username": current_user.username,
        "created_at": current_user.created_at,
        "likes_count": likes_count,
        "favorites_count": favorites_count,
        "ratings_count": ratings_count
    }


@router.put("/profile")
def update_profile(
    user: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    username_exists = (
        db.query(UserModel)
        .filter(
            UserModel.username == user.username,
            UserModel.id != current_user.id
        )
        .first()
    )

    if username_exists:
        raise HTTPException(
            status_code=400,
            detail="Username already exists."
        )

    current_user.username = user.username

    db.commit()
    db.refresh(current_user)

    return current_user


@router.get("/", response_model=list[UserResponse])
def get_users(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(UserModel).all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = (
        db.query(UserModel)
        .filter(UserModel.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    return user
