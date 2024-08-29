from typing import Annotated

import jwt
from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import ValidationError

from app.config import settings
from app.exchanges.dependencies import Storage, get_exchange, get_storage
from app.exchanges.models import (
    CreateExchangeRequest,
    Exchange,
    InitiatorExchangeResponse,
)
from app.models import HTTPExceptionResponse
from app.yivi.models import (
    DisclosureRequest,
    DisclosureRequestJWT,
    DisclosureSessionResultJWT,
    ExtendedDisclosureRequest,
)

router = APIRouter()


@router.post("/create/")
async def create(
    exchange_request: CreateExchangeRequest,
    storage: Annotated[Storage, Depends(get_storage)],
):
    """Create a new exchange.

    This endpoint allows the initiator to choose configuration options for the exchange.
    """
    # TODO: Decide on how the attributes are specified and validated. For example, there could be a
    # selection of allowed attributes defined in the settings, several predefined ConDisCons to pick
    # from, or even a system where additional attributes need to be disclosed to DIYivi, in order to
    # authorize asking for sensitive attributes.
    exchange = Exchange(
        public_initiator_attributes=exchange_request.public_initiator_attributes,
        public_initiator_attribute_values=None,
        attributes=exchange_request.attributes,
        initiator_attribute_values=None,
    )
    await storage.save_exchange(exchange)

    disclosure_request = DisclosureRequestJWT(
        sprequest=ExtendedDisclosureRequest(
            request=DisclosureRequest(
                disclose=[
                    exchange.public_initiator_attributes,
                    *exchange.attributes,
                ],
                labels={
                    "0": {
                        "en": "Known by the recipient",
                        "nl": "Bekend bij de ontvanger",
                    }
                },
                clientReturnUrl=f"{settings.base_url}exchanges/{exchange.id}/",
                augmentReturnUrl=True,
            ),
        ),
    ).signed_jwt()

    return InitiatorExchangeResponse(
        id=exchange.id,
        initiator_secret=exchange.initiator_secret,
        request_jwt=disclosure_request,
    )


@router.post(
    "/{exchange_id}/start/",
    responses={
        400: {"model": HTTPExceptionResponse},
        404: {"model": HTTPExceptionResponse},
    },
)
async def start(
    exchange: Annotated[Exchange, Depends(get_exchange)],
    initiator_secret: Annotated[str, Body(pattern="^[0-9a-f]{32}$")],
    disclosure_result: Annotated[str, Body(title="Disclosure session result JWT")],
    storage: Annotated[Storage, Depends(get_storage)],
):
    """Start an exchange by submitting the session result JWT of the initiator's disclosure."""
    if exchange.initiator_secret != initiator_secret:
        raise HTTPException(status_code=400, detail="Incorrect initiator secret")
    if exchange.public_initiator_attribute_values is not None:
        raise HTTPException(status_code=400, detail="Exchange already started")

    try:
        result = DisclosureSessionResultJWT.parse_jwt(disclosure_result)
    except jwt.PyJWTError:
        raise HTTPException(status_code=400, detail="Invalid JWT")
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid session result")

    if not result.satisfies_condiscon(
        [exchange.public_initiator_attributes] + exchange.attributes,
    ):
        raise HTTPException(status_code=400, detail="Invalid session result")

    # Extract the disclosed attributes corresponding to (a) the disjunction for the
    # public initiator attributes and (b) the disjunctions for the other attributes.
    # Since we put the public initiator attributes first, in the session request JWTs,
    # they are guaranteed to also be in the first element of the disclosed attributes.
    exchange.public_initiator_attribute_values = result.disclosed[0]
    exchange.initiator_attribute_values = result.disclosed[1:]

    await storage.save_exchange(exchange)

    return


@router.get(
    "/{exchange_id}/",
    responses={
        400: {"model": HTTPExceptionResponse},
        404: {"model": HTTPExceptionResponse},
    },
)
async def get_exchange_info(
    exchange: Annotated[Exchange, Depends(get_exchange)],
):
    """Get information about an exchange, allowing a recipient to decide to respond."""
    if (
        exchange.public_initiator_attribute_values is None
        or exchange.initiator_attribute_values is None
    ):
        raise HTTPException(status_code=404, detail="Exchange not found")

    disclosure_request = DisclosureRequestJWT(
        sprequest=ExtendedDisclosureRequest(
            request=DisclosureRequest(
                disclose=exchange.attributes,
                clientReturnUrl=f"{settings.base_url}exchanges/{exchange.id}/",
                augmentReturnUrl=True,
            ),
        ),
    ).signed_jwt()

    return RecipientExchangeResponse(
        attributes=exchange.attributes,
        public_initiator_attribute_values=exchange.public_initiator_attribute_values,
        request_jwt=disclosure_request,
    )


@router.post(
    "/{exchange_id}/respond/",
    responses={
        400: {"model": HTTPExceptionResponse},
        404: {"model": HTTPExceptionResponse},
    },
)
async def respond(
    exchange: Annotated[Exchange, Depends(get_exchange)],
    disclosure_result: Annotated[str, Body(title="Disclosure session result JWT")],
):
    """Submit the session result JWT of a recipient's disclosure."""
