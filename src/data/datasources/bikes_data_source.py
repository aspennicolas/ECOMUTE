from typing import Any, Dict, List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.database import get_db
from src.data.schema_models import Bike  # change to src.data.models if you renamed the file


class BikesDataSource:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_bikes(self) -> List[Bike]:
        """Retrieve all bikes."""
        result = await self.db.execute(select(Bike))
        return result.scalars().all()

    async def get_bike(self, bike_id: int) -> Optional[Bike]:
        """Retrieve a single bike by ID."""
        result = await self.db.execute(
            select(Bike).where(Bike.id == bike_id)
        )
        return result.scalar_one_or_none()

    async def create_bike(self, bike_data: Dict[str, Any]) -> Bike:
        """Create a new bike."""
        new_bike = Bike(**bike_data)
        self.db.add(new_bike)
        await self.db.commit()
        await self.db.refresh(new_bike)
        return new_bike

    async def update_bike(self, bike_id: int, update_data: Dict[str, Any]) -> Optional[Bike]:
        """Update a bike. Returns the updated bike or None if not found."""
        result = await self.db.execute(
            select(Bike).where(Bike.id == bike_id)
        )
        bike = result.scalar_one_or_none()

        if not bike:
            return None

        for key, value in update_data.items():
            setattr(bike, key, value)

        await self.db.commit()
        await self.db.refresh(bike)
        return bike

    async def delete_bike(self, bike_id: int) -> bool:
        """Delete a bike. Returns True if deleted, False if not found."""
        result = await self.db.execute(
            select(Bike).where(Bike.id == bike_id)
        )
        bike = result.scalar_one_or_none()

        if not bike:
            return False

        await self.db.delete(bike)
        await self.db.commit()
        return True


def get_bike_datasource(db: AsyncSession = Depends(get_db)) -> BikesDataSource:
    return BikesDataSource(db)