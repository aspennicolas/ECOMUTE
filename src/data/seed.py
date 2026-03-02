from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.data.schema_models import Bike
from src.data.schema_models import User 

# Define your Mock Data here as dictionaries
INITIAL_BIKES = [
    {"model": "EcoCruiser", "status": "available", "battery": 95},
    {"model": "MountainE", "status": "maintenance", "battery": 15},
    {"model": "CitySprint", "status": "rented", "battery": 60},
]

INITIAL_USERS = [
    {"username": "rider_one", "is_active": True},
    {"username": "admin_dave", "is_active": True},
]

async def seed_data(db: AsyncSession):
    """
    Checks if the DB is empty. If yes, populates it with mock data.
    """
    print("🌱 Checking if database needs seeding...")
    
    # 1. Check if bikes exist
    result = await db.execute(select(Bike).limit(1))
    first_bike = result.scalar_one_or_none()
    
    if first_bike:
        print("✅ Database already contains data. Skipping seed.")
        return

    print("🚀 Seeding database with initial mock data...")

    # 2. Add Bikes
    for bike_data in INITIAL_BIKES:
        # We unpack the dictionary into the Class Constructor
        new_bike = Bike(**bike_data)
        db.add(new_bike)

    # 3. Add Users
    for user_data in INITIAL_USERS:
        new_user = User(**user_data)
        db.add(new_user)

    # 4. Save to DB
    await db.commit()
    print("🎉 Seeding complete!")