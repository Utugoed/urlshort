from bson import ObjectId
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.db.connection import get_db
from app.helpers import generate_link
from app.schemas import LinkModel, LinkCreateModel, UserModel


link_not_found = HTTPException(status_code=404, detail="Link not found")
different_link = HTTPException(status_code=418, detail="This is a different link")


class Links:
    @staticmethod
    async def create_link(input_data: dict, db: AsyncIOMotorClient, user_id: ObjectId):

        links = db.links

        link_is_exist = True
        while link_is_exist:
            link = generate_link(settings.LINK_LENGTH)
            link_is_exist = await links.count_documents({"link": link}) != 0

        result = await links.insert_one(
            {"link": link, "url": input_data["url"], "owner": user_id}
        )

        inserted_link = await links.find_one({"_id": result.inserted_id})
        response = {"id": str(inserted_link["_id"])}
        return response

    @staticmethod
    async def get_links(db: AsyncIOMotorClient, user_id: ObjectId):

        links = db.links

        response = []
        async for doc in links.find({"owner": user_id}):
            doc["id"] = str(doc.pop("_id"))
            doc["owner"] = str(doc["owner"])
            response.append(doc)

        return response

    @staticmethod
    async def get_link(link_id: str, db: AsyncIOMotorClient, user_id: ObjectId):

        links = db.links

        try:
            response = await links.find_one({"_id": ObjectId(link_id)})
            if response["owner"] != user_id:
                raise different_link
            response["id"] = str(response.pop("_id"))
            response["owner"] = str(response["owner"])
            return response

        except:
            raise link_not_found

    @staticmethod
    async def update_link(
        link_id: str, input_data: dict, db: AsyncIOMotorClient, user_id: ObjectId
    ):

        links = db.links

        try:
            link = await links.find_one({"_id": ObjectId(link_id)})
            if link["owner"] != user_id:
                raise different_link

            result = await links.update_one(
                {"_id": ObjectId(link_id)}, {"$set": {"url": input_data["url"]}}
            )

            response = {}
            response["id"] = link_id
            return response

        except:
            raise link_not_found

    @staticmethod
    async def delete_link(link_id: str, db: AsyncIOMotorClient, user_id: ObjectId):

        links = db.links

        try:
            link = await links.find_one({"_id": ObjectId(link_id)})
            if link["owner"] != user_id:
                raise different_link

            await links.delete_one({"_id": ObjectId(link_id)})

            response = {}
            response["id"] = link_id
            return response

        except:
            raise link_not_found

    @staticmethod
    async def link_redirect(link: str):

        db = await get_db()
        links = db.links

        doc = await links.find_one({"link": link})
        return doc
