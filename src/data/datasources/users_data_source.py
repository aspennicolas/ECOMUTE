from typing import List, Dict, Any, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.database import get_db
from src.data.models import User


# UsersDataSource is the data-access layer for users — mirrors the pattern in bikes_data_source.py.
class UsersDataSource:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_users(self) -> List[User]:
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def get_user(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()  # None if no user with that id exists

    async def create_user(self, user_data: Dict[str, Any]) -> User:
        new_user = User(**user_data)   # build ORM object from the dict
        self.db.add(new_user)          # stage for insert
        await self.db.commit()
        await self.db.refresh(new_user)  # populate auto-generated id from DB
        return new_user

    async def update_user(
        self, user_id: int, update_data: Dict[str, Any]
    ) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            return None  # router should handle this as a 404

        # Overwrite only the fields present in update_data.
        for key, value in update_data.items():
            setattr(user, key, value)

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> bool:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            return False

        await self.db.delete(user)
        await self.db.commit()
        return True


# Dependency factory used with Depends(get_user_datasource) in the router.
def get_user_datasource(db: AsyncSession = Depends(get_db)) -> UsersDataSource:
    return UsersDataSource(db)
