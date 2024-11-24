"""
This module defines UserRepository Class.

Classes:
    UserRepository: Class for managing User entities in the database.

"""

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.schemas import UserCreate


class UserRepository:
    """
    Repository class for managing User entities in the database.
    Methods
    -------
    __init__(self, session: AsyncSession)
        Initializes the UserRepository with a database session.
    async def get_user_by_id(self, user_id: int) -> User | None
        Retrieves a user by their ID.
    async def get_user_by_username(self, username: str) -> User | None
        Retrieves a user by their username.
    async def get_user_by_email(self, email: str) -> User | None
        Retrieves a user by their email.
    async def create_user(self, body: UserCreate, avatar: str = None) -> User
        Creates a new user with the given details and optional avatar.
    """

    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        Retrieve a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User | None: The user object if found, otherwise None.
        """
        stmt = select(User).filter_by(id=user_id)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        """
        Retrieve a user by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            User | None: The user object if found, otherwise None.
        """
        stmt = select(User).filter_by(username=username)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by their email address.

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            User | None: The user object if found, otherwise None.
        """
        stmt = select(User).filter_by(email=email)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def create_user(self, body: UserCreate, avatar: str = None) -> User:
        """
        Create a new user in the database.

        Args:
            body (UserCreate): The data required to create a new user.
            avatar (str, optional): The URL or path to the user's avatar image. Defaults to None.

        Returns:
            User: The newly created user object.
        """
        user = User(
            **body.model_dump(exclude_unset=True, exclude={"password"}),
            hashed_password=body.password,
            avatar=avatar
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
