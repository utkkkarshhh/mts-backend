from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.utils import logger
from settings.tortoise_config import TORTOISE_ORM


class DatabaseConfig:
    def register(self, app: FastAPI):
        register_tortoise(
            app,
            config=TORTOISE_ORM,
            generate_schemas=True,
            add_exception_handlers=True    
        )
        app.add_event_handler("startup", self._log_connection)

    async def _log_connection(self):
        try:
            logger.info("Successfully connected to the database!")
        except Exception as e:
            logger.error(f"Failed to connect to the database: {e}")
