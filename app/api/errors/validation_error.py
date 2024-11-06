from pydantic import BaseModel
from typing import Any
from loguru import logger
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse


class ErrorResponse(BaseModel):
    """Base Model for error responses"""
    status: int
    message: Any

    model_config = {
        "arbitrary_types_allowed": True
    }


async def http422_error_handler(request: Request, exc: RequestValidationError):
    logger.error("Validation error: {}", exc.errors())
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body}  # Use 'content' instead of 'message'
    )
