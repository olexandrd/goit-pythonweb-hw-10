"""
This module provides /me endpoint for logged users.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

from fastapi import APIRouter, Depends, Request

from src.schemas import UserModel
from src.services.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])
limiter = Limiter(key_func=get_remote_address)


@router.get(
    "/me", response_model=UserModel, description="No more than 5 requests per minute"
)
@limiter.limit("5/minute")
async def me(request: Request, user: UserModel = Depends(get_current_user)):
    """
    Retrieve the current authenticated user.
    """
    return user
