from fastapi import APIRouter, Depends
from src.data.datasources.users_data_source import (
    UsersDataSource,
    get_user_datasource,
)
from src.models.users import UserSignup

router = APIRouter(prefix="/users", tags=["Users"])


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
    success = await datasource.delete_user(user_id)
    return {"success": success}


@router.post("/signup-test")
def signup_test(payload: UserSignup):
    return {"ok": True, "email": str(payload.email)}