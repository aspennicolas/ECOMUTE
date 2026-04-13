from typing import Any, Dict, List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.database import get_db
from src.data.models import Bike


# BikesDataSource is the data-access layer for bikes.
# It wraps all database queries so the router doesn't talk to the DB directly.
class BikesDataSource:
    def __init__(self, db: AsyncSession):
        # Store the injected DB session for use in every method below.
        self.db = db

    async def get_all_bikes(self) -> List[Bike]:
        # execute() runs the query; scalars().all() extracts the Bike objects from the result.
        result = await self.db.execute(select(Bike))
        return result.scalars().all()

    async def get_bike(self, bike_id: int) -> Optional[Bike]:
        # scalar_one_or_none() returns the single matched row, or None if not found.
        result = await self.db.execute(
            select(Bike).where(Bike.id == bike_id)
        )
        return result.scalar_one_or_none()

    async def create_bike(self, bike_data: Dict[str, Any]) -> Bike:
        new_bike = Bike(**bike_data)   # unpack the dict into keyword args for the ORM model
        self.db.add(new_bike)          # stage the new row (not written yet)
        await self.db.commit()         # flush to the database
        await self.db.refresh(new_bike)  # reload from DB so auto-generated fields (e.g. id) are populated
        return new_bike

    async def update_bike(self, bike_id: int, update_data: Dict[str, Any]) -> Optional[Bike]:
        result = await self.db.execute(
            select(Bike).where(Bike.id == bike_id)
        )
        bike = result.scalar_one_or_none()

        if not bike:
            return None  # signal to the router that the bike doesn't exist

        # Apply each field from the payload onto the ORM object.
        # SQLAlchemy tracks these changes and writes them on commit.
        for key, value in update_data.items():
            setattr(bike, key, value)

        await self.db.commit()
        await self.db.refresh(bike)
        return bike

    async def delete_bike(self, bike_id: int) -> bool:
        result = await self.db.execute(
            select(Bike).where(Bike.id == bike_id)
        )
        bike = result.scalar_one_or_none()

        if not bike:
            return False  # caller can use this to raise a 404

        await self.db.delete(bike)
        await self.db.commit()
        return True


# FastAPI dependency factory: builds a BikesDataSource with a fresh DB session
# for each incoming request, then discards it when the request is done.
def get_bike_datasource(db: AsyncSession = Depends(get_db)) -> BikesDataSource:
    return BikesDataSource(db)
