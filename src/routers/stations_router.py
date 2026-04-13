from fastapi import APIRouter, Depends, HTTPException, status

from src.data.datasources.stations_data_source import StationsDataSource, get_station_datasource
from src.data.models import User
from src.models.stations import StationCreate, StationResponse
from src.security import get_current_user

router = APIRouter(prefix="/stations", tags=["Stations"])


@router.get("/", response_model=list[StationResponse])
async def get_stations(
    datasource: StationsDataSource = Depends(get_station_datasource),
) -> list[StationResponse]:
    return await datasource.get_all_stations()


@router.post("/", response_model=StationResponse, status_code=201)
async def create_station(
    station: StationCreate,
    current_user: User = Depends(get_current_user),
    datasource: StationsDataSource = Depends(get_station_datasource),
) -> StationResponse:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return await datasource.create_station(station.model_dump())
