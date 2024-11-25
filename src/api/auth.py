"""
This module provides authentication-related endpoints for user registration and login.

Endpoints:
- POST /auth/register: Registers a new user in the system.
- POST /auth/login: Authenticates a user and returns an access token.

Functions:
- register_user(user_data: UserCreate, db: Session = Depends(get_db)) -> User:
    Registers a new user by checking if the email or username already exists.
    If either exists, raises an HTTP 409 Conflict exception.
    If both are unique, hashes the user's password and creates a new user record in the database.
        user_data (UserCreate): The data required to create a new user, 
            including email, username, and password.
        db (Session, optional): The database session dependency. Defaults to Depends(get_db).
        HTTPException: If a user with the given email or username already exists, 
            raises an HTTP 409 Conflict exception.

- login_user(form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)) -> Token:
    Authenticates a user by verifying the username and password.
    If authentication is successful, returns an access token.
        form_data (OAuth2PasswordRequestForm): The form data containing the username and password.
        db (Session, optional): The database session dependency. Defaults to Depends(get_db).
        Token: The access token and token type.
        HTTPException: If authentication fails, raises an HTTP 401 Unauthorized exception.
"""

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas import UserCreate, Token, UserModel
from src.services.auth import create_access_token, Hash
from src.services.users import UserService
from src.database.db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user in the system.
    """

    user_service = UserService(db)

    email_user = await user_service.get_user_by_email(user_data.email)
    if email_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    username_user = await user_service.get_user_by_username(user_data.username)
    if username_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username already exists",
        )
    user_data.password = Hash().get_password_hash(user_data.password)
    new_user = await user_service.create_user(user_data)

    return new_user


@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Logs in a user by verifying their credentials and generating an access token.
    """
    user_service = UserService(db)
    user = await user_service.get_user_by_username(form_data.username)
    if not user or not Hash().verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = await create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
