"""
This module provides authentication services including password hashing, 
    JWT token creation, and user retrieval.

Classes:
    Hash: Provides methods to hash and verify passwords using bcrypt.

Functions:
    create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:

    get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        Retrieves the current user based on the provided JWT token.

    oauth2_scheme (OAuth2PasswordBearer): OAuth2 password bearer token URL for authentication.
"""

from typing import Optional
from datetime import datetime, timedelta, UTC
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from src.database.db import get_db
from src.conf.config import config
from src.services.users import UserService


class Hash:
    """
    Hash class provides methods to hash and verify passwords using bcrypt.

    Attributes:
        pwd_context (CryptContext): The context for password hashing and verification.

    Methods:
        verify_password(plain_password, hashed_password):
            Verifies a plain password against a hashed password.

        get_password_hash(password: str):
            Hashes a plain password and returns the hashed password.
    """

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        """
        Verify if the provided plain password matches the hashed password.

        Args:
            plain_password (str): The plain text password to verify.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the plain password matches the hashed password, False otherwise.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
        Hashes the provided password using the password context.

        Args:
            password (str): The plain text password to be hashed.

        Returns:
            str: The hashed password.
        """
        return self.pwd_context.hash(password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# define a function to generate a new access token
async def create_access_token(data: dict, expires_delta: Optional[int] = None):
    """
    Creates a JSON Web Token (JWT) for the given data with an optional expiration time.

    Args:
        data (dict): The data to encode in the JWT.
        expires_delta (Optional[int], optional): The number of seconds until the token expires.
                If not provided, defaults to the configured expiration time.

    Returns:
        str: The encoded JWT.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + timedelta(seconds=expires_delta)
    else:
        expire = datetime.now(UTC) + timedelta(seconds=config.JWT_EXPIRATION_SECONDS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Retrieve the current user based on the provided JWT token.

    Args:
        token (str): The JWT token provided by the user.
        db (Session): The database session dependency.

    Returns:
        User: The user object corresponding to the username in the token.

    Raises:
        HTTPException: If the token is invalid or the user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT
        payload = jwt.decode(
            token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
        )
        username = payload["sub"]
        if username is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception from e
    user_service = UserService(db)
    user = await user_service.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user
