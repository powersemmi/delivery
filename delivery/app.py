from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from delivery.routes import delivery, index
from delivery.settings import settings

SERVICE_NAME = "Landing Back"
API_VERSION = "0.0.1"

origins = [
    f"http://{settings.HOST}:{settings.PORT}",
    f"https://{settings.HOST}:{settings.PORT}",
]


def create_app():
    app = FastAPI(
        debug=settings.DEBUG,
        title=SERVICE_NAME,
        version=API_VERSION,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    v1 = "/api/v1"

    app.include_router(delivery.router, prefix=v1)
    app.include_router(index.router)
    return app
