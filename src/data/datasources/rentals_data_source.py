from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.database import get_db
from src.data.models import Rental, Bike, User
from src.logger import logger


# RentalsDataSource handles the business logic for creating a rental.
class RentalsDataSource:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_rental(self, user_id: int, bike_id: int):
        logger.info(f"Rental attempt: user_id={user_id}, bike_id={bike_id}")
        # db.get() is a shortcut for fetching a row by primary key.
        bike = await self.db.get(Bike, bike_id)
        if not bike:
            logger.warning(f"Rental failed: bike_id={bike_id} not found")
            raise HTTPException(status_code=404, detail="Bike not found")
        if bike.status != "available":
            # Prevent renting a bike that's already out or under maintenance.
            logger.warning(f"Rental failed: bike_id={bike_id} is {bike.status}")
            raise HTTPException(status_code=400, detail="Bike not available")

        user = await self.db.get(User, user_id)
        if not user:
            logger.warning(f"Rental failed: user_id={user_id} not found")
            raise HTTPException(status_code=404, detail="User not found")

        # Create the rental record and mark the bike as rented in the same transaction.
        rental = Rental(user_id=user_id, bike_id=bike_id)
        bike.status = "rented"  # SQLAlchemy detects this change and includes it in the commit

        self.db.add(rental)
        await self.db.commit()
        await self.db.refresh(rental)  # ensure rental.id is populated from the DB

        logger.info(f"Rental created: rental_id={rental.id}, user_id={user_id}, bike_id={bike_id}")
        # Return both the rental object and the bike's battery level so the
        # router can build a RentalOutcome response without a second query.
        return rental, bike.battery


# Dependency factory: wires up the datasource with a DB session for each request.
def get_rentals_datasource(db: AsyncSession = Depends(get_db)) -> RentalsDataSource:
    return RentalsDataSource(db)
