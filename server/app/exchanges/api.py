from typing import Annotated

from fastapi import APIRouter, Body, Depends

from app.exchanges.dependencies import Storage, get_exchange, get_storage
from app.exchanges.models import (
    CreateExchangeRequest,
    Exchange,
)
from app.models import HTTPExceptionResponse

router = APIRouter()


@router.post("/create/")
async def create(
    exchange_request: CreateExchangeRequest,
    storage: Annotated[Storage, Depends(get_storage)],
):
    """Create a new exchange.

    This endpoint allows the initiator to choose configuration options for the exchange.
    """


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
