from fastapi import status

from app.constants import ResponseMessages
from app.utils import ResponseHandler


class HealthCheck:
    def get():
        return ResponseHandler(
            message=ResponseMessages.SERVICE_IS_UP,
            success=True,
            status=status.HTTP_200_OK
        )
