from fastapi import APIRouter

from app.views import *

routes = [
    ("/healthcheck", HealthCheck.get, ["GET"]),
    ("/create_task/batch", CreateTaskView.post, ["POST"]),
]

v1_router = APIRouter()

for path, endpoint, methods in routes:
    v1_router.add_api_route(path, endpoint, methods=methods)
