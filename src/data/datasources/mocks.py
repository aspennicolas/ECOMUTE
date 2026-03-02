"""
This module acts as a temporary data store (Mock Database).
In Sessions 9-10, we will replace these lists with real SQL queries.
"""
from typing import List, Dict, Any

# Mock Database Tables
BIKES: List[Dict[str, Any]] = [
    {"id": 1, "model": "EcoCruiser", "status": "available", "battery": 95, "station_id": 101},
    {"id": 2, "model": "MountainE", "status": "maintenance", "battery": 15, "station_id": 102},
    {"id": 3, "model": "CitySprint", "status": "rented", "battery": 60, "station_id": None},
]

USERS: List[Dict[str, Any]] = [
    {"id": 1, "username": "rider_one", "is_active": True},
    {"id": 2, "username": "admin_dave", "is_active": True},
]