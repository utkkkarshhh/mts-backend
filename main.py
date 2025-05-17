import redis
from fastapi import FastAPI
from rq import Queue

from app.routes import urls
from settings import Settings

redis_conn = redis.Redis()
queue = Queue(connection=redis_conn)

app = FastAPI()
settings = Settings(app)
app.include_router(urls)
