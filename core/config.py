from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.base import Base
from models.engine import ENGINE, get_db
from routers.procedure import router as procedure_router


def configure_cors(application: FastAPI) -> None:
    origins = ["http://localhost:8000"]
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def configure_routes(application: FastAPI) -> None:
    application.include_router(procedure_router)


def configure_db() -> None:
    Base.metadata.bind = get_db()
    Base.metadata.create_all(bind=ENGINE)
