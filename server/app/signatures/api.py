from fastapi import APIRouter

# from app.config import settings
# from app.models import HTTPExceptionResponse

router = APIRouter()


@router.post("/request")
def create_signature_request():
    """Create a request for someone to sign a plain-text message."""
    raise NotImplementedError


@router.get("/request/{request_id}/")
def get_signature_request():
    """Get information about a request to sign a message."""
    raise NotImplementedError


@router.post("/request/{request_id}/")
def submit_signature_request():
    """Submit the signature that someone requested."""
    raise NotImplementedError
