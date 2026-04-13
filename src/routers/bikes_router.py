from typing import Optional, Literal, List

from fastapi import APIRouter, Query, Depends, HTTPException
from src.data.datasources.bikes_data_source import BikesDataSource, get_bike_datasource
from src.models.bikes import BikeCreate, BikeResponse
from src.logger import logger

# All routes here share the /bikes prefix and appear under "Bikes" in the docs.
router = APIRouter(prefix="/bikes", tags=["Bikes"])

# Restrict the status query parameter to only these three valid strings.
Status = Literal["available", "rented", "maintenance"]


# GET /bikes  — returns all bikes, with an optional filter by status.
@router.get("/", response_model=List[BikeResponse]) # List[] indicates we return a list of bikes, even if it's empty.
async def get_bikes( 
    status: Optional[Status] = Query(default=None),  # ?status=available etc. Optional means the client can omit this parameter; if they do, it will be None. Query() allows us to add metadata and validation for query parameters.
    datasource: BikesDataSource = Depends(get_bike_datasource), # FastAPI will call get_bike_datasource() to get the datasource instance and pass it in here.
) -> List[BikeResponse]: # The return type is a list of BikeResponse models.
    logger.info("Fetching all bikes")
    bikes = await datasource.get_all_bikes() # Get all bikes from the datasource.
    if status: # If the client provided a status filter, we apply it here.
        # Filter in Python (simple; fine for small datasets).
        bikes = [b for b in bikes if b.status == status] # Keep only bikes whose status matches the requested status.
    if not bikes:
        logger.warning("No bikes found")
    return bikes


# GET /bikes/{bike_id}  — fetch a single bike by its id.
@router.get("/{bike_id}", response_model=BikeResponse | None) # The response can be a BikeResponse if found, or None if not found. FastAPI will handle converting None to a 404 response.
async def get_bike(
    bike_id: int,
    datasource: BikesDataSource = Depends(get_bike_datasource),
) -> BikeResponse | None:
    return await datasource.get_bike(bike_id) 


# POST /bikes  — create a new bike; returns 201 Created on success.
@router.post("/", response_model=BikeResponse, status_code=201)
async def create_bike( # The client will send a JSON body that matches the BikeCreate model, and FastAPI will parse it into a BikeCreate instance and pass it in here.
    bike: BikeCreate,
    datasource: BikesDataSource = Depends(get_bike_datasource),
) -> BikeResponse:
    logger.info(f"Creating new bike: {bike.model}")
    # model_dump() converts the Pydantic model to a plain dict for the datasource.
    return await datasource.create_bike(bike.model_dump())


# PUT /bikes/{bike_id}  — replace all fields of an existing bike.
@router.put("/{bike_id}", response_model=BikeResponse | None) # The response can be the updated BikeResponse if the bike was found and updated, or None if the bike_id doesn't exist.
async def update_bike(
    bike_id: int, # The bike_id comes from the URL path, e.g. /bikes/123 would set bike_id=123.
    updated_bike: BikeCreate,
    datasource: BikesDataSource = Depends(get_bike_datasource),
) -> BikeResponse | None:
    return await datasource.update_bike(bike_id, updated_bike.model_dump())


# DELETE /bikes/{bike_id}  — remove a bike; 404 if it doesn't exist.
@router.delete("/{bike_id}")
async def delete_bike(
    bike_id: int,
    datasource: BikesDataSource = Depends(get_bike_datasource),
):
    success = await datasource.delete_bike(bike_id)
    if not success:
        raise HTTPException(status_code=404, detail="Bike not found")
    return {"success": True}
