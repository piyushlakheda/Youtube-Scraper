"""
Global exception handlers for the YouTube Video Fetcher API.

This module defines custom handlers for HTTP exceptions, validation errors,
and generic server errors, returning structured JSON responses.
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError
from app.errors import errors

def http_error_handler(request: Request, exc: HTTPException):
    """
    Handle FastAPI HTTPException and return a JSON response.

    Args:
        request (Request): The incoming request.
        exc (HTTPException): The raised HTTP exception.

    Returns:
        JSONResponse: JSON error response with status code and detail.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle FastAPI request validation errors and return a JSON response.

    Args:
        request (Request): The incoming request.
        exc (RequestValidationError): The raised validation error.

    Returns:
        JSONResponse: JSON error response with status code and validation details.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )

def generic_exception_handler(request: Request, exc: Exception):
    """
    Handle uncaught exceptions and return a generic JSON error response.

    Args:
        request (Request): The incoming request.
        exc (Exception): The raised exception.

    Returns:
        JSONResponse: JSON error response with status code 500 and generic message.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": errors.INTERNAL_SERVER_ERROR},
    )
