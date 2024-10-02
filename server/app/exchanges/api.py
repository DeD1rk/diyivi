from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from pydantic import ValidationError

from app.config import settings
from app.exchanges.dependencies import Storage, get_exchange, get_storage
from app.exchanges.models import (
    CreateExchangeRequest,
    DisclosedValue,
    Exchange,
    ExchangeReply,
    ExchangeResultResponse,
    ExchangeType,
    InitiatorExchangeResponse,
    RecipientExchangeResponse,
    RecipientResponseResponse,
)
from app.exchanges.utils import create_condiscon
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
) -> InitiatorExchangeResponse:
    """Create a new exchange.

    This endpoint allows the initiator to choose configuration options for the exchange.
    """
    # TODO: Decide on how the attributes are specified and validated. For example, there could be a
    # selection of allowed attributes defined in the settings, several predefined ConDisCons to pick
    # from, or even a system where additional attributes need to be disclosed to DIYivi, in order to
    # authorize asking for sensitive attributes.
    exchange = Exchange(
        type=exchange_request.type,
        send_email=exchange_request.send_email,
        public_initiator_attributes=exchange_request.public_initiator_attributes,
        public_initiator_attribute_values=None,
        attributes=exchange_request.attributes,
        initiator_attribute_values=None,
        expire_at=datetime.now(UTC) + timedelta(seconds=settings.exchange_ttl_before_start),
    )
    await storage.save_exchange(exchange)

    condiscon = create_condiscon(
        ([settings.email_attribute] if exchange.send_email else [])
        + [*exchange.public_initiator_attributes, *exchange.attributes]
    )

    disclosure_request = DisclosureRequestJWT(
        sprequest=ExtendedDisclosureRequest(
            request=DisclosureRequest(disclose=condiscon),
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
    status_code=204,
)
async def start(
    exchange: Annotated[Exchange, Depends(get_exchange)],
    initiator_secret: Annotated[str, Body(pattern="^[0-9a-f]{32}$", embed=True)],
    disclosure_result: Annotated[str, Body(title="Disclosure session result JWT", embed=True)],
    storage: Annotated[Storage, Depends(get_storage)],
) -> None:
    """Start an exchange by submitting the session result JWT of the initiator's disclosure."""
    if exchange.initiator_secret != initiator_secret:
        raise HTTPException(status_code=400, detail="Incorrect initiator secret")
    if exchange.started:
        raise HTTPException(status_code=400, detail="Exchange already started")

    try:
        result = DisclosureSessionResultJWT.parse_jwt(disclosure_result)
    except jwt.PyJWTError:
        raise HTTPException(status_code=400, detail="Invalid JWT")
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid session result")

    if not result.satisfies_condiscon(
        create_condiscon(
            [settings.email_attribute, *exchange.public_initiator_attributes, *exchange.attributes]
            if exchange.send_email
            else [*exchange.public_initiator_attributes, *exchange.attributes]
        )
    ):
        raise HTTPException(status_code=400, detail="Invalid session result")

    disclosed_values = {
        disclosed_attribute.id: disclosed_attribute
        for con in result.disclosed
        for disclosed_attribute in con
    }

    exchange.public_initiator_attribute_values = [
        DisclosedValue(id=id, value=disclosed_values[id].value)
        for id in exchange.public_initiator_attributes
    ]
    exchange.initiator_attribute_values = [
        DisclosedValue(id=id, value=disclosed_values[id].value) for id in exchange.attributes
    ]

    if exchange.send_email:
        exchange.initiator_email_value = disclosed_values[settings.email_attribute].rawvalue

    exchange.expire_at = datetime.now(UTC) + timedelta(seconds=settings.exchange_ttl)

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
    storage: Annotated[Storage, Depends(get_storage)],
) -> RecipientExchangeResponse:
    """Get information about an exchange, allowing a recipient to decide to respond."""
    if not exchange.started:
        raise HTTPException(status_code=404, detail="Exchange not found")

    if exchange.type == ExchangeType.ONE_TO_ONE:
        replies = await storage.get_replies(exchange.id)
        if replies:
            raise HTTPException(status_code=404, detail="Exchange not found")

    disclosure_request = DisclosureRequestJWT(
        sprequest=ExtendedDisclosureRequest(
            request=DisclosureRequest(
                disclose=create_condiscon(exchange.attributes),
            ),
        ),
    ).signed_jwt()

    return RecipientExchangeResponse(
        attributes=exchange.attributes,
        public_initiator_attribute_values=exchange.public_initiator_attribute_values,  # type: ignore
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
    disclosure_result: Annotated[str, Body(title="Disclosure session result JWT", embed=True)],
    storage: Annotated[Storage, Depends(get_storage)],
) -> RecipientResponseResponse:
    """Submit the session result JWT of a recipient's disclosure."""
    if not exchange.started:
        raise HTTPException(status_code=404, detail="Exchange not found")

    if exchange.type == ExchangeType.ONE_TO_ONE:
        # TODO: prevent race condition that could allow saving multiple replies.
        replies = await storage.get_replies(exchange.id)
        if replies:
            raise HTTPException(status_code=404, detail="Exchange not found")

    try:
        result = DisclosureSessionResultJWT.parse_jwt(disclosure_result)
    except jwt.PyJWTError:
        raise HTTPException(status_code=400, detail="Invalid JWT")
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid session result")

    if not result.satisfies_condiscon(create_condiscon(exchange.attributes)):
        raise HTTPException(status_code=400, detail="Invalid session result")

    disclosed_values = {
        disclosed_attribute.id: disclosed_attribute
        for con in result.disclosed
        for disclosed_attribute in con
    }

    reply = ExchangeReply(
        exchange_id=exchange.id,
        attribute_values=[
            DisclosedValue(id=id, value=disclosed_values[id].value) for id in exchange.attributes
        ],
    )
    await storage.push_reply(exchange, reply)

    if exchange.send_email and exchange.initiator_email_value:
        # TODO: start backgroundtask to send email
        print(f"Sending an email with results to {exchange.initiator_email_value}")

    return RecipientResponseResponse(
        public_initiator_attribute_values=exchange.public_initiator_attribute_values,  # type: ignore
        initiator_attribute_values=exchange.initiator_attribute_values,  # type: ignore
        response_attribute_values=reply.attribute_values,
        recipient_secret=reply.recipient_secret,
    )


@router.get(
    "/{exchange_id}/result/",
    responses={
        404: {"model": HTTPExceptionResponse},
    },
)
async def get_exchange_result(
    exchange: Annotated[Exchange, Depends(get_exchange)],
    secret: Annotated[str, Query(pattern="^[0-9a-f]{32}$", embed=True)],
    storage: Annotated[Storage, Depends(get_storage)],
) -> ExchangeResultResponse:
    """Get the result of an exchange.

    This can be used by the initiator to retrieve the response of the recipient(s).
    A recipient can also use this by providing their `recipient_secret`, although it
    does not provide any new information for them.
    """
    if not exchange.started:
        raise HTTPException(status_code=404, detail="Exchange not found")

    replies = await storage.get_replies(exchange.id)

    if secret != exchange.initiator_secret and secret not in [
        reply.recipient_secret for reply in replies
    ]:
        raise HTTPException(status_code=404, detail="Exchange not found")

    if secret != exchange.initiator_secret and exchange.type == ExchangeType.ONE_TO_ONE:
        visible_replies = [next(reply for reply in replies if secret == reply.recipient_secret)]
    else:
        visible_replies = replies

    return ExchangeResultResponse(
        public_initiator_attribute_values=exchange.public_initiator_attribute_values,  # type: ignore
        initiator_attribute_values=exchange.initiator_attribute_values,  # type: ignore
        replies=[reply.attribute_values for reply in visible_replies],
    )
