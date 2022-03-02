from bson.objectid import ObjectId

from fastapi import APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List

from app.db import Links, Users, get_db
from app.schemas import LinkModel, LinkCreateModel, ResponseModel, UserModel


links_router = APIRouter()


async def url_is_exist(input_data: dict, db: AsyncIOMotorClient, user_id: ObjectId):

    existing_url = await db.links.find_one({"url": input_data["url"], "owner": user_id})

    if existing_url is not None:
        response = {
            "status": "Fail",
            "id": str(existing_url["_id"]),
            "detail": "This URL is registered",
        }
        return response


@links_router.post("/", response_model=ResponseModel)
async def new_link(
    input_data: LinkCreateModel,
    db: AsyncIOMotorClient = Depends(get_db),
    user_id: ObjectId = Depends(Users.get_current_user),
):

    input_data = input_data.dict()
    return await url_is_exist(input_data, db, user_id) or await Links.create_link(
        input_data, db, user_id
    )


@links_router.get("/", response_model=List[LinkModel])
async def links_list(
    db: AsyncIOMotorClient = Depends(get_db),
    user_id: ObjectId = Depends(Users.get_current_user),
):
    return await Links.get_links(db, user_id)


@links_router.get("/{link_id}", response_model=LinkModel)
async def link_detail(
    link_id: str,
    db: AsyncIOMotorClient = Depends(get_db),
    user_id: ObjectId = Depends(Users.get_current_user),
):
    return await Links.get_link(link_id, db, user_id)


@links_router.patch("/{link_id}", response_model=ResponseModel)
async def link_update(
    link_id: str,
    input_data: LinkCreateModel,
    db: AsyncIOMotorClient = Depends(get_db),
    user_id: ObjectId = Depends(Users.get_current_user),
):

    input_data = input_data.dict()
    return await url_is_exist(input_data, db, user_id) or await Links.update_link(
        link_id, input_data, db, user_id
    )


@links_router.delete("/{link_id}", response_model=ResponseModel)
async def link_delete(
    link_id: str,
    db: AsyncIOMotorClient = Depends(get_db),
    user_id: ObjectId = Depends(Users.get_current_user),
):
    return await Links.delete_link(link_id, db, user_id)
