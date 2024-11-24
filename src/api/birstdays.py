from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas import ContactResponse
from src.services.birstdays import BirthdayService

router = APIRouter(prefix="/birstdays", tags=["birstdays"])


@router.get("/nearest", response_model=List[ContactResponse])
async def read_bistdays(
    skip: int = 0,
    limit: int = 100,
    daygap: int = 7,
    db: AsyncSession = Depends(get_db),
):
    contact_service = BirthdayService(db)
    contacts = await contact_service.get_contacts(skip, limit, daygap)
    return contacts
