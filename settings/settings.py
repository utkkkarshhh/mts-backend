import os
from dotenv import load_dotenv
from fastapi import FastAPI

from app.exceptions import register_exception_handlers
from .database_config import DatabaseConfig

load_dotenv()

class Settings:
    def __init__(self, app: FastAPI):
        self.app = app
        register_exception_handlers(app)
        self.database_config = DatabaseConfig()
        self.database_config.register(app)
