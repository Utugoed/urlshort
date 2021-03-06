import logging.config

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings


logger = logging.getLogger("events")


class Database:
    client: AsyncIOMotorClient


db = Database()


async def connect_to_mongodb():
    logger.info("Connecting to MongoDB")
    db.client = AsyncIOMotorClient(
        settings.MONGODB_CONNECTION_URL,
    )
    server_info = await db.client.server_info()


async def close_mongodb_connection():
    logger.info("Closing MongoDB connections")
    db.client.close()


async def get_db():
    return db.client[settings.MONGO_DB]


async def get_mongo_client():
    return db.client
