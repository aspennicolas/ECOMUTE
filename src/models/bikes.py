'''Exercise 1: Pydantic schemas (20 Mins) 
Task: Define the "Shape" of our data here. This ensures inputs are valid and 
outputs are filtered (security). 
    1. Define a class BikeBase. 
    2. Use Type Hinting for all fields: model (str), battery_level (float), status 
    (str - strictly 'available', 'rented', or 'maintenance') and optional 
    station_id (int) 
    3. Define also classes BikeCreate and BikeResponse (which includes id) 
    4. Define classes UserCreate (username and email, both strings) and 
    UserResponse (id - int , username - str , and is_active - bool) '''

from typing import Literal, Optional
from pydantic import BaseModel, Field

class BikeBase(BaseModel):
    model: str
    battery: int = Field(le=100)
    status: Literal["available", "rented", "maintenance"]
    station_id: Optional[int] = None

class BikeCreate(BikeBase):
    pass

class BikeResponse(BikeBase):
    id: int