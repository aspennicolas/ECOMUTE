from typing import Optional, Literal, List

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.data.database import get_db
from src.data.schema_models import Bike  # change to: from src.data.models import Bike
from src.models.bikes import BikeCreate, BikeResponse

router = APIRouter(prefix="/bikes", tags=["Bikes"])
Status = Literal["available", "rented", "maintenance"]


@router.get("/", response_model=List[BikeResponse])
async def get_bikes(
    status: Optional[Status] = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> List[BikeResponse]:
    result = await db.execute(select(Bike))
    bikes = result.scalars().all()

    if status:
        bikes = [b for b in bikes if b.status == status]

    return bikes


@router.get("/{bike_id}", response_model=BikeResponse | None)
async def get_bike(
    bike_id: int,
    db: AsyncSession = Depends(get_db),
) -> BikeResponse | None:
    result = await db.execute(select(Bike).where(Bike.id == bike_id))
    return result.scalar_one_or_none()


@router.post("/", response_model=BikeResponse, status_code=201)
async def create_bike(
    bike: BikeCreate,
    db: AsyncSession = Depends(get_db),
) -> BikeResponse:
    new_bike = Bike(
        model=bike.model,
        battery=bike.battery,
        status=bike.status,
    )
    db.add(new_bike)
    await db.commit()
    await db.refresh(new_bike)
    return new_bike


@router.put("/{bike_id}", response_model=BikeResponse | None)
async def update_bike(
    bike_id: int,
    updated_bike: BikeCreate,
    db: AsyncSession = Depends(get_db),
) -> BikeResponse | None:
    result = await db.execute(select(Bike).where(Bike.id == bike_id))
    bike = result.scalar_one_or_none()
    if not bike:
        return None

    bike.model = updated_bike.model
    bike.battery = updated_bike.battery
    bike.status = updated_bike.status

    await db.commit()
    await db.refresh(bike)
    return bike


@router.delete("/{bike_id}")
async def delete_bike(
    bike_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Bike).where(Bike.id == bike_id))
    bike = result.scalar_one_or_none()
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")

    await db.delete(bike)
    await db.commit()
    return {"success": True}