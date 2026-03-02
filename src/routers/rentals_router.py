from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.rentals import RentalOutcome, RentalProcessing
from src.data.database import get_db
from src.data.schema_models import Rental, Bike, User

router = APIRouter(prefix="/rentals", tags=["Rentals"])


@router.post("/", response_model=RentalOutcome, status_code=201)
async def create_rental(
    payload: RentalProcessing,
    db: AsyncSession = Depends(get_db),
) -> RentalOutcome:
    # 1) Check bike exists
    bike = await db.get(Bike, payload.bike_id)
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")

    # 2) Bike must be available
    if bike.status != "available":
        raise HTTPException(status_code=400, detail="Bike not available")

    # 3) Check user exists
    user = await db.get(User, payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 4) Create rental row
    rental = Rental(user_id=payload.user_id, bike_id=payload.bike_id)

    # 5) Update bike status
    bike.status = "rented"

    db.add(rental)
    await db.commit()
    await db.refresh(rental)

    # Use battery from DB (source of truth)
    return RentalOutcome(
        user_id=rental.user_id,
        bike_id=rental.bike_id,
        bike_battery=bike.battery,
    )