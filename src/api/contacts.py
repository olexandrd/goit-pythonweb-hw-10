"""
This module defines the API routes for managing contacts using FastAPI.

Routes:
    - GET /contacts: Fetch a list of contacts from the database.
    - GET /contacts/{contact_id}: Retrieve a contact by its ID.
    - POST /contacts: Create a new contact.
    - PUT /contacts/{contact_id}: Update an existing contact.
    - DELETE /contacts/{contact_id}: Remove a contact by its ID.

Dependencies:
    - db: The database session dependency, provided by `get_db`.

Schemas:
    - ContactModel: The schema for contact data input.
    - ContactResponse: The schema for contact data output.

Services:
    - ContactService: The service class for handling contact-related operations.
"""

from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse
from src.services.contacts import ContactService

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    skip: int = 0,
    limit: int = 100,
    queue: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Fetch a list of contacts from the database.
    Args:
        skip (int, optional): The number of records to skip. Defaults to 0.
        limit (int, optional): The maximum number of records to return. Defaults to 100.
        queue (str | None, optional): An optional filter parameter. Defaults to None.
        db (AsyncSession, optional): The database session dependency.
    Returns:
        List[Contact]: A list of contact records.
    """
    contact_service = ContactService(db)
    contacts = await contact_service.get_contacts(skip, limit, queue)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a contact by its ID.
    Args:
        contact_id (int): The ID of the contact to retrieve.
        db (AsyncSession, optional): The database session dependency.
    Returns:
        Contact: The contact object if found.
    Raises:
        HTTPException: If the contact is not found, raises a 404 HTTP exception.
    """

    contact_service = ContactService(db)
    contact = await contact_service.get_contact(contact_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: AsyncSession = Depends(get_db)):
    """
    Create a new contact.
    Args:
        body (ContactModel): The contact data to be created.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).
    Returns:
        dict: The created contact data.
    """

    contact_service = ContactService(db)
    return await contact_service.create_contact(body)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    body: ContactModel, contact_id: int, db: AsyncSession = Depends(get_db)
):
    """
    Update an existing contact.

    Args:
        body (ContactModel): The contact data to update.
        contact_id (int): The ID of the contact to update.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the contact is not found, raises a 404 HTTP exception.

    Returns:
        ContactModel: The updated contact data.
    """
    contact_service = ContactService(db)
    contact = await contact_service.update_contact(contact_id, body)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    """
    Remove a contact by its ID.

    Args:
        contact_id (int): The ID of the contact to be removed.
        db (AsyncSession, optional): The database session dependency.

    Returns:
        Contact: The removed contact object.

    Raises:
        HTTPException: If the contact with the given ID is not found.
    """
    contact_service = ContactService(db)
    contact = await contact_service.remove_contact(contact_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact
