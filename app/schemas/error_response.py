from typing import List

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    errors: List[str]
    success: bool = False