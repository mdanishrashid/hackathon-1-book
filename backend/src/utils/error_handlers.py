import logging
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
import sys
from typing import Optional
import traceback
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log")
    ]
)

logger = logging.getLogger(__name__)

class ErrorCode(str, Enum):
    # Authentication errors
    AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    
    # Authorization errors
    ACCESS_DENIED = "ACCESS_DENIED"
    INSUFFICIENT_PERMISSIONS = "INSUFFICIENT_PERMISSIONS"
    
    # Resource errors
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    RESOURCE_ALREADY_EXISTS = "RESOURCE_ALREADY_EXISTS"
    
    # Validation errors
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_INPUT = "INVALID_INPUT"
    
    # Service errors
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    INTERNAL_ERROR = "INTERNAL_ERROR"

class CustomException(HTTPException):
    def __init__(self, status_code: int, detail: str, error_code: ErrorCode = ErrorCode.INTERNAL_ERROR):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        logger.error(f"CustomException: {error_code} - {detail}")

def log_error(error: Exception, context: Optional[str] = None):
    """Log an error with traceback"""
    error_msg = f"Error in {context}: {str(error)}" if context else f"Error: {str(error)}"
    logger.error(error_msg)
    logger.error(traceback.format_exc())

def log_info(message: str, context: Optional[str] = None):
    """Log an informational message"""
    log_msg = f"{context}: {message}" if context else message
    logger.info(log_msg)

def log_warning(message: str, context: Optional[str] = None):
    """Log a warning message"""
    log_msg = f"{context}: {message}" if context else message
    logger.warning(log_msg)

async def global_exception_handler(request, exc):
    """Global exception handler for the application"""
    log_error(exc, f"Unhandled exception in {request.url.path}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "type": "INTERNAL_ERROR",
                "message": "An unexpected error occurred. Please try again later."
            }
        }
    )

async def http_exception_handler(request, exc):
    """Handler for HTTP exceptions"""
    log_warning(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": exc.__class__.__name__,
                "message": exc.detail
            }
        }
    )