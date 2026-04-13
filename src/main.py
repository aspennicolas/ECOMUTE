from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.data.database import engine, AsyncSessionLocal
from src.data.models import Base
from src.data.seed import seed_data
from src.routers import bikes_router, predictions_router, users_router, rentals_router, admin_router
from src.routers import auth, stations_router


# lifespan runs once on startup (before yield) and once on shutdown (after yield).
# Here we use it to create all DB tables automatically if they don't exist yet.
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # create_all inspects all SQLAlchemy models that inherit from Base
        # and issues CREATE TABLE statements for any that are missing.
        await conn.run_sync(Base.metadata.create_all)
    # After tables exist, seed the DB with initial data if it's empty.
    async with AsyncSessionLocal() as db:
        await seed_data(db)
    yield  # the app runs here; code after yield would be shutdown logic


# Create the FastAPI app and attach the lifespan handler defined above.
app = FastAPI(lifespan=lifespan)


# Simple health-check / root endpoint.
@app.get("/")
async def get_root():
    return {"Hello Class good morning!!!"}


# Register each feature's router under its own URL prefix (defined inside each router file).
app.include_router(bikes_router.router)
app.include_router(users_router.router)
app.include_router(rentals_router.router)
app.include_router(admin_router.router)
app.include_router(auth.router)
app.include_router(stations_router.router)
app.include_router(predictions_router.router)
