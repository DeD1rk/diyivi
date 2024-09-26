import secrets
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, Field, model_validator

from app.yivi.models import Attribute, Timestamp, TranslatedString


class ExchangeType(StrEnum):
    ONE_TO_ONE = "1-to-1"
    # ONE_TO_MANY = "1-to-many"
    # MANY_TO_MANY = "many-to-many"


class DisclosedValue(BaseModel):
    """A disclosed value of an attribute."""

    id: Attribute
    value: TranslatedString


DisclosedValues = list[DisclosedValue]


class Exchange(BaseModel):
    """An exchange in progress as saved in the backend."""

    id: str = Field(
        min_length=16,
        max_length=16,
        pattern="^[0-9a-f]{16}$",
        default_factory=lambda: secrets.token_hex(8),
    )

    type: ExchangeType

    initiator_secret: str = Field(
        description="Secret used to access the exchange as initiator.",
        min_length=32,
        max_length=32,
        pattern="^[0-9a-f]{32}$",
        default_factory=lambda: secrets.token_hex(16),
    )

    attributes: list[Attribute] = Field(min_length=1)

    public_initiator_attributes: list[Attribute] = Field(
        min_length=1,
        description="""Attributes that the recipient already knows about the initiator.

        This is used to prevent a party B from becoming a man-in-the-middle by forwarding an
        exchange with A to C. The intended recipient should know the value of these attributes
        already, such that party C will notice that a request was initiated by A and not by B,
        if B tries to forward A's request to C.
        """,
    )

    initiator_attribute_values: DisclosedValues | None = Field(
        default=None,
        description="""The initiator's disclosed attributes.

        If set, this is a mapping from the attributes in `attributes`
        to the corresponding disclosed values.
        """,
    )
    public_initiator_attribute_values: DisclosedValues | None = Field(
        default=None,
        description="""The initiator's disclosed public attributes.

        If set, this is a mapping from the attributes in `public_initiator_attributes`
        to the corresponding disclosed values.
        """,
    )

    expire_at: Timestamp = Field(
        description="Unix timestamp indicating when this exchange will be removed.",
    )

    @model_validator(mode="after")
    def check_initiator_attribute_values_match(self) -> Self:
        if self.initiator_attribute_values is not None and set(
            value.id for value in self.initiator_attribute_values
        ) != set(self.attributes):
            raise ValueError(
                "Initiator's disclosed attributes do not match the exchange's attributes"
            )
        return self

    @model_validator(mode="after")
    def check_public_initiator_attribute_values_match(self) -> Self:
        if self.public_initiator_attribute_values is not None and set(
            value.id for value in self.public_initiator_attribute_values
        ) != set(self.public_initiator_attributes):
            raise ValueError(
                "Initiator's disclosed public attributes do not match the exchange's attributes"
            )
        return self

    @property
    def started(self) -> bool:
        """Whether the exchange has been started."""
        return (
            self.initiator_attribute_values is not None
            and self.public_initiator_attribute_values is not None
        )


class ExchangeReply(BaseModel):
    """Reply to an exchange as saved in the backend."""

    exchange_id: str = Field(
        min_length=16,
        max_length=16,
        pattern="^[0-9a-f]{16}$",
    )

    recipient_secret: str = Field(
        description="Secret used to access the corresponding exchange as recipient.",
        min_length=32,
        max_length=32,
        pattern="^[0-9a-f]{32}$",
        default_factory=lambda: secrets.token_hex(16),
    )

    attribute_values: DisclosedValues = Field(
        description="""The recipient's disclosed attributes.

        This is a mapping from the attributes in `Exchange.attributes`
        to the corresponding disclosed values.
        """,
    )


class CreateExchangeRequest(BaseModel):
    """Request body to create an exchange."""

    type: ExchangeType = Field(default=ExchangeType.ONE_TO_ONE)

    # TODO: these can be replaced with pointers to predefined sets of attributes,
    #  or get validation based on configurable whitelisted attributes.
    attributes: list[Attribute] = Field(min_length=1)

    public_initiator_attributes: list[Attribute] = Field(
        description="""Attributes that the recipient already knows about the initiator.

        This is used to prevent a party B from becoming a man-in-the-middle by forwarding an
        exchange with A to C. The intended recipient should know the value of these attributes
        already, such that party C will notice that a request was initiated by A and not by B,
        if B tries to forward A's request to C.
        """,
        min_length=1,
    )


class InitiatorExchangeResponse(BaseModel):
    """Information about a newly created exchange for the initiator."""

    id: str = Field(
        min_length=16,
        max_length=16,
        pattern="^[0-9a-f]{16}$",
    )
    initiator_secret: str = Field(
        min_length=32,
        max_length=32,
        pattern="^[0-9a-f]{32}$",
    )
    request_jwt: str = Field(
        description="JWT containing a disclosure request for the initiator.",
    )


class RecipientExchangeResponse(BaseModel):
    """Information about an exchange for a recipient."""

    attributes: list[Attribute]
    public_initiator_attribute_values: DisclosedValues
    request_jwt: str = Field(
        description="JWT containing a disclosure request for the recipient.",
    )


class RecipientResponseResponse(BaseModel):
    """Response to a recipient's disclosure."""

    public_initiator_attribute_values: DisclosedValues
    initiator_attribute_values: DisclosedValues
    response_attribute_values: DisclosedValues

    recipient_secret: str = Field(
        min_length=32,
        max_length=32,
        pattern="^[0-9a-f]{32}$",
        description="Secret for the recipient to maintain access to the exchanged attributes.",
    )


class ExchangeResultResponse(BaseModel):
    """Response to a request for an exchange result."""

    public_initiator_attribute_values: DisclosedValues
    initiator_attribute_values: DisclosedValues

    replies: list[DisclosedValues] = Field(
        description="""The disclosed attributes of the recipients.

        Each element contains the disclosed attributes of one reply.
        The replies are ordered in the order the replies were received in.
        """,
    )
