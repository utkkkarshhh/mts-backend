from enum import Enum
from typing import List


class HTTPStatusCodes(Enum):
    SUCCESS = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_ERROR = 500
    TIMEOUT_ERROR = 408

    @classmethod
    def get_success_response_code(cls) -> List:
        return [
            cls.SUCCESS.value,
            cls.CREATED.value,
            cls.NO_CONTENT.value
        ]
