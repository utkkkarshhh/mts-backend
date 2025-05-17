from fastapi import status

from app.exceptions.base import BaseCustomException


class BadRequestException(BaseCustomException):
    def __init__(self, detail):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)

class NotFoundException(BaseCustomException):
    def __init__(self, detail):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)
