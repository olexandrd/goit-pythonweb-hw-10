"""
Service class for managing user-related operations.
Methods:
--------
__init__(db: AsyncSession):
    Initializes the UserService with a database session.
async create_user(body: UserCreate):
    Creates a new user with the provided details and generates a Gravatar avatar if possible.
async get_user_by_id(user_id: int):
    Retrieves a user by their unique ID.
async get_user_by_username(username: str):
    Retrieves a user by their username.
async get_user_by_email(email: str):
    Retrieves a user by their email address.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from libgravatar import Gravatar

from src.repository.users import UserRepository
from src.schemas import UserCreate


class UserService:
    """
    Service class for managing user-related operations.
    Methods:
    --------
    __init__(db: AsyncSession):
        Initializes the UserService with a database session.
    async create_user(body: UserCreate):
        Creates a new user with the provided details and generates a Gravatar avatar if possible.
    async get_user_by_id(user_id: int):
        Retrieves a user by their unique ID.
    async get_user_by_username(username: str):
        Retrieves a user by their username.
    async get_user_by_email(email: str):
        Retrieves a user by their email address.
    """

    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def create_user(self, body: UserCreate):
        """
        Asynchronously creates a new user with the provided information.

        This method attempts to generate a Gravatar image based on the user's email.
        If the Gravatar generation fails, it catches the exception and proceeds without an avatar.

        Args:
            body (UserCreate): The user creation data, including email and other user details.

        Returns:
            The created user object with the provided information and the generated avatar
                (if available).
        """
        avatar = None
        try:
            g = Gravatar(body.email)
            avatar = g.get_image()
        except Exception as e:  # pylint: disable=broad-except
            print(e)

        return await self.repository.create_user(body, avatar)

    async def get_user_by_id(self, user_id: int):
        """
        Retrieve a user by their unique identifier.

        Args:
            user_id (int): The unique identifier of the user.

        Returns:
            User: The user object corresponding to the given user_id, or None if no user is found.
        """
        return await self.repository.get_user_by_id(user_id)

    async def get_user_by_username(self, username: str):
        """
        Retrieve a user by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            User: The user object corresponding to the given username, or None if no user is found.
        """
        return await self.repository.get_user_by_username(username)

    async def get_user_by_email(self, email: str):
        """
        Retrieve a user by their email address.

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            User: The user object associated with the given email address,
                or None if no user is found.
        """
        return await self.repository.get_user_by_email(email)
