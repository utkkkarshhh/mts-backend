from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

from app.utils import logger


def extract_cleaned_response(key: str, value: str, result: Dict[str, Any]) -> Dict[str, Any]:
    start_index = value.find("[{'detail':")
    if start_index != -1:
        cleaned_response = value[start_index:].split("}],")[0]
        result = extract_detail_value(cleaned_response, result, key, value)
    else:
        result[key] = value
    return result

def extract_detail_value(cleaned_response: str, result: Dict[str, Any], key: str, value: str) -> Dict[str, Any]:
    detail_key_index = cleaned_response.find("'detail': ")
    if detail_key_index != -1:
        detail_value = cleaned_response[detail_key_index + len("'detail': "):]
        result[key] = detail_value.strip(" '")
    else:
        result[key] = value
    return result

def reformat_error_response(input_data: Any) -> Any:
    if isinstance(input_data, dict):
        result = {}
        for key, value in input_data.items():
            if isinstance(value, str):
                result = extract_cleaned_response(key, value, result)
            else:
                result[key] = reformat_error_response(value)
        return result
    elif isinstance(input_data, list):
        return [reformat_error_response(item) for item in input_data]
    else:
        return input_data

async def custom_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    if isinstance(exc, HTTPException):
        if hasattr(exc, 'detail'):
            error_detail = exc.detail
            if isinstance(error_detail, dict):
                error_detail = reformat_error_response(error_detail)
                error_messages = [error_detail.get("detail")] if error_detail.get("detail") else [str(error_detail)]
            else:
                error_messages = [str(error_detail)]
            
            return JSONResponse(
                status_code=exc.status_code,
                content={"errors": error_messages, "success": False}
            )
    
    logger.exception("Something went wrong")
    return JSONResponse(
        status_code=500,
        content={"errors": ["Something went wrong"], "success": False}
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = []
    for error in exc.errors():
        loc = " -> ".join(str(loc_item) for loc_item in error.get("loc", []))
        message = f"{loc}: {error.get('msg', 'Validation error')}"
        errors.append(message)
    
    return JSONResponse(
        status_code=400,
        content={"errors": errors, "success": False}
    )

def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(HTTPException, custom_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, custom_exception_handler)
