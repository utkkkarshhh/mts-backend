import redis
from fastapi import FastAPI
from rq import Queue

from app.routes import urls
from settings import Settings

app = FastAPI()

redis_conn = redis.Redis()
queue = Queue(connection=redis_conn)

settings = Settings(app)
app.include_router(urls)
