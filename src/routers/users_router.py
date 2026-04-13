from fastapi import APIRouter, Depends
from src.data.datasources.users_data_source import (
    UsersDataSource,
    get_user_datasource,
)
from src.models.users import UserSignup, UserCreate, UserResponse
from src.security import get_password_hash
from src.logger import logger

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    datasource: UsersDataSource = Depends(get_user_datasource),
):
    logger.info(f"Creating user: {user.username}")
    return await datasource.create_user({
        "username": user.username,
        "hashed_password": get_password_hash(user.password),
    })


@router.get("/")
async def get_users(
    datasource: UsersDataSource = Depends(get_user_datasource),
):
    return await datasource.get_all_users()


@router.get("/{user_id}")
async def get_user(
    user_id: int,
    datasource: UsersDataSource = Depends(get_user_datasource),
):
    return await datasource.get_user(user_id)


@router.put("/{user_id}")
async def update_user(
    user_id: int,
    updated_user: dict,
    datasource: UsersDataSource = Depends(get_user_datasource),
):
    return await datasource.update_user(user_id, updated_user)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    datasource: UsersDataSource = Depends(get_user_datasource),
):
    logger.warning(f"Deleting user: {user_id}")
    success = await datasource.delete_user(user_id)
    return {"success": success}


@router.post("/signup-test", response_model=UserResponse)
async def signup_test(
    payload: UserSignup,
    datasource: UsersDataSource = Depends(get_user_datasource),
):
    return await datasource.create_user({
        "username": payload.username,
        "hashed_password": get_password_hash(payload.password),
    })