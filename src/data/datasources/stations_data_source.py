from typing import Any, Dict, List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.database import get_db
from src.data.models import Station


class StationsDataSource:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_stations(self) -> List[Station]:
        result = await self.db.execute(select(Station))
        return result.scalars().all()

    async def get_station(self, station_id: int) -> Optional[Station]:
        result = await self.db.execute(
            select(Station).where(Station.id == station_id)
        )
        return result.scalar_one_or_none()

    async def create_station(self, station_data: Dict[str, Any]) -> Station:
        new_station = Station(**station_data)
        self.db.add(new_station)
        await self.db.commit()
        await self.db.refresh(new_station)
        return new_station


def get_station_datasource(db: AsyncSession = Depends(get_db)) -> StationsDataSource:
    return StationsDataSource(db)
