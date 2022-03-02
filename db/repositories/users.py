import asyncio
from bson.objectid import ObjectId
from datetime import timedelta

from jose import jwt, JWTError
from fastapi import HTTPException, Header, status
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.db.connection import get_db
from app.helpers import create_access_token, get_password_hash, verify_password
from app.schemas import UserModel


class Users:
    @staticmethod
    async def create_user(user: UserModel, db: AsyncIOMotorClient):

        users = db.users

        email_quantity = await users.count_documents({"email": user.email})
        if email_quantity != 0:
            response = {"status": "Fail", "detail": "This e-mail is used"}
            return response
        if len(user.password) < 6:
            response = {"status": "Fail", "detail": "This password is too easy"}
            return response

        user.password = get_password_hash(user.password)
        result = await users.insert_one(user.dict())

        response = await users.find_one({"_id": result.inserted_id})
        response["id"] = str(response.pop("_id"))
        response.pop("password")

        return response

    @staticmethod
    async def get_current_user(token: str = Header(...)):

        db = await get_db()
        users = db.users
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user = await users.find_one({"email": email})

        if user is None:
            raise credentials_exception

        return user["_id"]

    @staticmethod
    async def user_auth(log_in_data: UserModel, db: AsyncIOMotorClient):

        users = db.users
        user = await users.find_one({"email": log_in_data.email})

        if not (user and verify_password(log_in_data.password, user["password"])):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect e-mail or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["email"]}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    async def delete_user(user_id: ObjectId, db: AsyncIOMotorClient):

        links = db.links
        users = db.users

        await users.delete_one({"_id": user_id})
        await links.delete_many({"owner": user_id})

        response = {}
        response["id"] = str(user_id)
        return response
