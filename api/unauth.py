from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.db import Users, get_db
from app.schemas import UserModel, UserAuthModel


unauth_router = APIRouter()


@unauth_router.post("/log_in", response_model=UserAuthModel)
async def log_in(user: UserModel, db: AsyncIOMotorClient = Depends(get_db)):
    return await Users.user_auth(user, db)
