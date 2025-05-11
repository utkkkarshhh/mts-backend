from fastapi import FastAPI

from app.routes import urls
from settings import Settings

app = FastAPI()
settings = Settings(app)
app.include_router(urls)
