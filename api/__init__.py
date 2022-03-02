from fastapi import APIRouter

from .links import links_router
from .users import users_router
from .unauth import unauth_router


api_router = APIRouter()

api_router.include_router(links_router, prefix="/links")
api_router.include_router(unauth_router, prefix="/auth")
api_router.include_router(users_router, prefix="/users")
