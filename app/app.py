from fastapi import FastAPI

from app import routes
from app.settings import Settings


def get_app(env_file: str = ".env"):
    settings = Settings(_env_file=env_file)  # type: ignore
    app = FastAPI()

    @app.get("/")
    async def root():
        return {"message": "Hi hi"}

    @app.get("/settings/")
    async def info():
        return settings

    app.include_router(routes.router)

    return app
