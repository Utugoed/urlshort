from bson.objectid import ObjectId

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.db import Users, get_db
from app.schemas import UserModel, ResponseModel


users_router = APIRouter()


@users_router.post("/sign_up", response_model=ResponseModel)
async def sign_up(user: UserModel, db: AsyncIOMotorClient = Depends(get_db)):
    return await Users.create_user(user, db)

@users_router.delete("/delete", response_model=ResponseModel)
async def delete_account(
    user_id: ObjectId = Depends(Users.get_current_user),
    db: AsyncIOMotorClient = Depends(get_db)
):
    return await Users.delete_user(user_id, db)
