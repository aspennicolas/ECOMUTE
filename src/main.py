from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.data.database import engine
from src.data.schema_models import Base
from src.routers import bikes_router, users_router, rentals_router, admin_router

#bike = BikeBase("La bcidi de contador", 30, "rented", 1)
#print(bike.model)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def get_root():
    return {"Hello Class good morning!!!"}

app.include_router(bikes_router.router)
app.include_router(users_router.router)
app.include_router(rentals_router.router)
app.include_router(admin_router.router)