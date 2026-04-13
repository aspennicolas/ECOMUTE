from typing import Optional
from pydantic import BaseModel


class StationBase(BaseModel):
    name: str
    location: Optional[str] = None
    capacity: int = 10


class StationCreate(StationBase):
    pass


class StationResponse(StationBase):
    id: int
