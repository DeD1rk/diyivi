from pydantic import BaseModel


class HTTPExceptionResponse(BaseModel):
    """Response model for HTTP exceptions."""

    detail: str
