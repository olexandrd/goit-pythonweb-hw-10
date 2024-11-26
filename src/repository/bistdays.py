"""
DB operations for bistdays
"""

import json
from datetime import timedelta, datetime
from typing import List
import redis.asyncio as redis

from sqlalchemy import select
from sqlalchemy.sql import extract
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect

from src.database.models import Contact, User
from src.conf.config import settings


class BirthdayRepository:
    """
    Birthday repository
    """

    def __init__(self, session: AsyncSession):
        self.db = session
        self._redis = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    async def serialize_contacts(self, contacts: List[Contact]) -> str:
        """
        Serialize a list of Contact objects into JSON,
        handling non-serializable fields like relationships.
        """

        def serialize(contact):
            mapper = inspect(contact)
            serialized = {}

            for column in mapper.attrs:
                value = getattr(contact, column.key)
                if isinstance(value, (int, float, str, bool, type(None))):
                    serialized[column.key] = value
                elif isinstance(value, datetime):
                    serialized[column.key] = value.isoformat()
                else:
                    serialized[column.key] = str(value)

            return serialized

        return json.dumps([serialize(contact) for contact in contacts])

    async def deserialize_contacts(self, serialized_contacts: str) -> List[dict]:
        """
        Deserialize JSON string into a list of Contact dictionaries.
        """
        return json.loads(serialized_contacts)

    async def get_contacts(
        self, skip: int, limit: int, daygap: int, user: User
    ) -> List[Contact]:
        """
        Retrieve contacts, skip and limit are used for pagination
        """

        today = datetime.now()
        start_day = today.timetuple().tm_yday
        end_day = (today + timedelta(days=daygap)).timetuple().tm_yday
        redis_key = f"{user.id}-{skip}-{limit}-{daygap}"

        cached_contacts = await self._redis.get(redis_key)
        if cached_contacts:
            # Deserialize and return cached contacts
            return await self.deserialize_contacts(cached_contacts)

        if end_day < start_day:
            stmt = (
                select(Contact)
                .filter_by(user=user)
                .filter(
                    (extract("doy", Contact.birstday) >= start_day)
                    | (extract("doy", Contact.birstday) <= end_day)
                )
                .offset(skip)
                .limit(limit)
            )
        else:
            stmt = (
                select(Contact)
                .filter_by(user=user)
                .filter(extract("doy", Contact.birstday).between(start_day, end_day))
                .offset(skip)
                .limit(limit)
            )

        contacts_result = await self.db.execute(stmt)
        contacts = contacts_result.scalars().all()

        # Serialize contacts and store them in Redis
        serialized_contacts = await self.serialize_contacts(contacts)
        await self._redis.set(redis_key, list(contacts))
        await self._redis.expire(redis_key, 3600)
        # Return serialized contacts as dictionaries
        return await self.deserialize_contacts(serialized_contacts)
