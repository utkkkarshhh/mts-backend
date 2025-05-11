from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.utils import logger


class DatabaseConfig:
    
    def __init__(self, database_config: dict):
        self.TORTOISE_ORM = {
            "connections": {
                "default": {
                    "engine": "tortoise.backends.asyncpg",
                    "credentials": database_config
                }
            },
            "apps": {
                "models": {
                    "models": [ "app.models", "aerich.models" ],
                    "default_connection": "default",
                },
            },
        }

    def register(self, app: FastAPI):
        register_tortoise(
            app,
            config=self.TORTOISE_ORM,
            generate_schemas=True,
            add_exception_handlers=True    
        )
        app.add_event_handler("startup", self._log_connection)

    async def _log_connection(self):
        try:
            logger.info("Successfully connected to the database!")
        except Exception as e:
            logger.error(f"Failed to connect to the database: {e}")
