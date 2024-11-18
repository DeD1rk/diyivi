from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException
from pydantic import ValidationError

from app.config import settings
from app.models import HTTPExceptionResponse
from app.utils import create_condiscon
from app.yivi.models import (
    DisclosureRequest,
    DisclosureRequestJWT,
    DisclosureSessionResultJWT,
    ExtendedDisclosureRequest,
    ExtendedIRMASignatureRequest,
    IRMASignatureRequest,
    IRMASignatureRequestJWT,
    SignatureSessionResultJWT,
)

from .dependencies import (
    SignaturesStorage,
    get_signature_request,
    get_signatures_storage,
)
from .email import send_initiator_signature_result_email
from .models import (
    CreateSignatureRequestRequest,
    RecipientSignatureRequestResponse,
    SignatureRequest,
    SignatureRequestResponse,
)

router = APIRouter()


@router.post("/create/")
async def create(
    create_request: CreateSignatureRequestRequest,
    storage: Annotated[SignaturesStorage, Depends(get_signatures_storage)],
) -> SignatureRequestResponse:
    """Create a request for someone to sign a plain-text message."""
    request = SignatureRequest(
        message=create_request.message,
        attributes=create_request.attributes,
        expire_at=datetime.now(UTC) + timedelta(seconds=settings.exchange_ttl_before_start),
    )
    await storage.save_request(request)

    disclosure_request = DisclosureRequestJWT(
        sprequest=ExtendedDisclosureRequest(
            validity=settings.session_request_validity,
            request=DisclosureRequest(disclose=[[[settings.email_attribute]]]),
        ),
    ).signed_jwt()

    return SignatureRequestResponse(
        id=request.id,
        request_jwt=disclosure_request,
    )


@router.post(
    "/{request_id}/start/",
    responses={
        400: {"model": HTTPExceptionResponse},
        404: {"model": HTTPExceptionResponse},
    },
    status_code=204,
)
async def start(
    signature_request: Annotated[SignatureRequest, Depends(get_signature_request)],
    disclosure_result: Annotated[str, Body(title="Disclosure session result JWT", embed=True)],
    storage: Annotated[SignaturesStorage, Depends(get_signatures_storage)],
) -> None:
    """Start a signature request by submitting a disclosure of your email."""
    if signature_request.initiator_email_value:
        raise HTTPException(status_code=400, detail="Signature request already started")

    try:
        result = DisclosureSessionResultJWT.parse_jwt(disclosure_result)
    except jwt.PyJWTError:
        raise HTTPException(status_code=400, detail="Invalid JWT")
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid session result")

    if not result.satisfies_condiscon([[[settings.email_attribute]]]):
        raise HTTPException(status_code=400, detail="Invalid session result")

    disclosed_values = {
        disclosed_attribute.id: disclosed_attribute
        for con in result.disclosed
        for disclosed_attribute in con
    }

    signature_request.initiator_email_value = disclosed_values[settings.email_attribute].rawvalue
    signature_request.expire_at = datetime.now(UTC) + timedelta(
        seconds=settings.signature_request_ttl
    )

    await storage.save_request(signature_request)

    return


@router.get(
    "/{request_id}/",
    responses={
        400: {"model": HTTPExceptionResponse},
        404: {"model": HTTPExceptionResponse},
    },
)
def get_signature_request_info(
    signature_request: Annotated[SignatureRequest, Depends(get_signature_request)],
) -> RecipientSignatureRequestResponse:
    """Get information about a request to sign a message."""
    if not signature_request.initiator_email_value:
        raise HTTPException(status_code=404, detail="Signature request not found")

    signature_session_request = IRMASignatureRequestJWT(
        absrequest=ExtendedIRMASignatureRequest(
            validity=settings.session_request_validity,
            request=IRMASignatureRequest(
                message=signature_request.message,
                disclose=create_condiscon(signature_request.attributes),
            ),
        )
    ).signed_jwt()

    return RecipientSignatureRequestResponse(
        attributes=signature_request.attributes,
        message=signature_request.message,
        initiator_email_value=signature_request.initiator_email_value,
        request_jwt=signature_session_request,
    )


@router.post(
    "/{request_id}/respond/",
    responses={
        400: {"model": HTTPExceptionResponse},
        404: {"model": HTTPExceptionResponse},
    },
    status_code=204,
)
async def submit_signature(
    signature_request: Annotated[SignatureRequest, Depends(get_signature_request)],
    signature_result: Annotated[str, Body(title="Signature session result JWT", embed=True)],
    storage: Annotated[SignaturesStorage, Depends(get_signatures_storage)],
    background_tasks: BackgroundTasks,
) -> None:
    """Submit the signature that someone requested."""
    if not signature_request.initiator_email_value:
        raise HTTPException(status_code=404, detail="Signature request not found")

    try:
        result = SignatureSessionResultJWT.parse_jwt(signature_result)
    except jwt.PyJWTError:
        raise HTTPException(status_code=400, detail="Invalid JWT")
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid session result")

    if not (
        result.signature.message == signature_request.message
        and result.satisfies_condiscon(create_condiscon(signature_request.attributes))
    ):
        raise HTTPException(status_code=400, detail="Invalid session result")

    background_tasks.add_task(send_initiator_signature_result_email, signature_request, result)

    await storage.delete_request(signature_request.id)

    return
