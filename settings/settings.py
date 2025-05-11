import os

from dotenv import load_dotenv
from fastapi import FastAPI

from .database_config import DatabaseConfig

load_dotenv()

class Settings:

    DATABASE_CONFIG = {
        "host": os.getenv('DB_HOST'),
        "port": int(os.getenv('DB_PORT')),
        "user": os.getenv('DB_USER'),
        "password": os.getenv('DB_PASSWORD'),
        "database": os.getenv('DB_NAME'),
    }

    def __init__(self, app: FastAPI):
        self.app = app
        self.database_config = DatabaseConfig(self.DATABASE_CONFIG)
        self.database_config.register(app)
