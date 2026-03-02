from typing import List, Dict, Any, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.database import get_db
from src.data.schema_models import User  # change to src.data.models if renamed


class UsersDataSource:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ==========================
    # USER OPERATIONS
    # ==========================

    async def get_all_users(self) -> List[User]:
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def get_user(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_user(self, user_data: Dict[str, Any]) -> User:
        new_user = User(**user_data)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def update_user(
        self, user_id: int, update_data: Dict[str, Any]
    ) -> Optional[User]:

        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            return None

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


def get_user_datasource(db: AsyncSession = Depends(get_db)) -> UsersDataSource:
    return UsersDataSource(db)