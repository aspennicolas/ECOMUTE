from fastapi import APIRouter, Depends

from src.models.rentals import RentalOutcome, RentalProcessing
from src.data.datasources.rentals_data_source import RentalsDataSource, get_rentals_datasource

router = APIRouter(prefix="/rentals", tags=["Rentals"])


# POST /rentals  — start a new rental.
# The client sends user_id and bike_id; we return confirmation + battery level.
@router.post("/", response_model=RentalOutcome, status_code=201)
async def create_rental(
    payload: RentalProcessing,           # Pydantic validates the incoming JSON
    datasource: RentalsDataSource = Depends(get_rentals_datasource), # FastAPI injects the datasource instance
) -> RentalOutcome:
    # The datasource returns the saved Rental ORM object AND the bike's battery
    # as a tuple so we can include it in the response without an extra query.
    rental, bike_battery = await datasource.create_rental(payload.user_id, payload.bike_id)
    return RentalOutcome( # We construct the response model using the data from the created rental and the bike battery.
        user_id=rental.user_id,
        bike_id=rental.bike_id,
        bike_battery=bike_battery,
    )
