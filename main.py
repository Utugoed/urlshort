import logging.config

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from app.api import api_router
from app.config import settings
from app.db import connect_to_mongodb, close_mongodb_connection, Links, Redirects


log_conf = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(process)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": "DEBUG",
        }
    },
    "root": {"handlers": ["console"], "level": "DEBUG"},
    "loggers": {
        "gunicorn": {"propagate": True},
        "uvicorn": {"propagate": True},
        "uvicorn.access": {"propagate": True},
        "events": {"propagate": True},
    },
}
logging.config.dictConfig(log_conf)


app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.include_router(api_router, prefix='/api')

app.add_event_handler("startup", connect_to_mongodb)
app.add_event_handler("shutdown", close_mongodb_connection)


@app.get("/{link}")
async def redirect(link: str, request: Request):

    client_host = request.client.host
    link_data = await Links.link_redirect(link)

    await Redirects.insert_redirect(link_data["_id"], client_host)
    response = RedirectResponse(link_data["url"])

    return response


if settings.DOMAIN == "urlshort.appvelox.ru":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
