import uvicorn
from fastapi import FastAPI
from src.config import Config
from loguru import logger
from src.presentation.api import router


class Application:
    def __init__(self, config: Config, app: FastAPI) -> None:
        self._config = config
        self._app = app

    @classmethod
    def from_config(cls, config: Config) -> "Application":
        app = FastAPI()
        app.include_router(router)
        return Application(config=config, app=app)

    async def start(self) -> None:
        logger.info("HTTP server is starting")

        server = uvicorn.Server(
            config=uvicorn.Config(
                app=self._app,
                host=self._config.host,
                port=self._config.port,
            )
        )
        await server.serve()
