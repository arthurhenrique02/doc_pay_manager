from fastapi import FastAPI

from .config import (
    configure_cors,
    configure_db,
    configure_routes,
)


def create_app() -> FastAPI:
    app = FastAPI()
    configure_cors(app)
    configure_routes(app)
    configure_db()
    return app


app = create_app()
