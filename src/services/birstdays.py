"""
BirthdayService class, which is responsible for handling operations related to birthdays.

Classes:
    BirthdayService: A service class for managing birthday-related operations.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.bistdays import BirthdayRepository
from src.schemas import User


class BirthdayService:
    """
    BirthdayService is a service class responsible for handling operations related to birthdays.

    Attributes:
        repository (BirthdayRepository): An instance of BirthdayRepository for database operations.

    Methods:
        __init__(db: AsyncSession):
            Initializes the BirthdayService with a database session.

        get_contacts(skip: int, limit: int, daygap: int, user: User) -> List[Contact]:


    """

    def __init__(self, db: AsyncSession):
        self.repository = BirthdayRepository(db)

    async def get_contacts(self, skip: int, limit: int, daygap: int, user: User):
        """
        Retrieve a list of contacts based on pagination and day gap criteria.

        Args:
            skip (int): The number of contacts to skip for pagination.
            limit (int): The maximum number of contacts to return.
            daygap (int): The number of days to filter contacts by.
            user (User): The user for whom the contacts are being retrieved.

        Returns:
            List[Contact]: A list of contacts that match the given criteria.
        """
        return await self.repository.get_contacts(skip, limit, daygap, user)
