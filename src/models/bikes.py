from typing import Literal, Optional
from pydantic import BaseModel, Field

# BikeBase holds the shared fields used for both creating and reading bikes.
class BikeBase(BaseModel):
    model: str
    battery: int = Field(le=100)  # must be <= 100 (percent)
    status: Literal["available", "rented", "maintenance"]  # only these three values allowed
    station_id: Optional[int] = None  # None means the bike is not docked at any station

# BikeCreate is sent by the client when adding a new bike (no id yet).
class BikeCreate(BikeBase):
    pass

# BikeResponse is what the API sends back — includes the DB-generated id.
class BikeResponse(BikeBase):
    id: int