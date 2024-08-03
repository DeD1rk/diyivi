import secrets

from pydantic import BaseModel, Field

from app.yivi.models import Attribute, DisclosedAttribute


class Exchange(BaseModel):
    """An exchange in progress as saved in the backend."""

    id: str = Field(
        min_length=16,
        max_length=16,
        pattern="^[0-9a-f]{16}$",
        default_factory=lambda: secrets.token_hex(8),
    )

    initiator_secret: str = Field(
        description="Secret used to access the exchange as initiator.",
        min_length=32,
        max_length=32,
        pattern="^[0-9a-f]{32}$",
        default_factory=lambda: secrets.token_hex(16),
    )

    attributes: list[list[list[Attribute]]]
    public_initiator_attributes: list[list[Attribute]] = Field(
        description="""Attributes that the recipient already knows about the initiator.

        This is used to prevent a party B from becoming a man-in-the-middle by forwarding an exchange with A to C. 
        The intended recipient should know the value of these attributes already, such that party C will
        notice that a request was initiated by A and not by B, if B tries to forward A's request to C.
        """,
    )

    initiator_attribute_values: list[list[DisclosedAttribute]] | None = Field(
        default=None,
        description="""The initiator's disclosed attributes.
        
        If set, this should satisfy the ConDisCon in `attributes`. This field only set 
        once the initiator has successfully disclosed their attributes.
        """,
    )
    public_initiator_attribute_values: list[DisclosedAttribute] | None = Field(
        default=None,
        description="""The initiator's disclosed public attributes.

        This should satisfy the disjunction in `public_initiator_attributes`. This field 
        is only set once the initiator has successfully disclosed their attributes.
        """,
    )


class ExchangeReply(BaseModel):
    """Reply to an exchange as saved in the backend."""

    id: str = Field(
        min_length=16,
        max_length=16,
        pattern="^[0-9a-f]{16}$",
        default_factory=lambda: secrets.token_hex(8),
    )

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

    attribute_values: list[list[DisclosedAttribute]] = Field(
        description="""The recipient's disclosed attributes.
        
        This should satisfy the ConDisCon in the corresponding Exchange's `attributes`.
        """,
    )


class CreateExchangeRequest(BaseModel):
    """Request body to create an exchange."""

    # TODO: these can be replaced with pointers to predefined sets of attributes, or get validation based on configurable whitelisted attributes.
    attributes: list[list[list[Attribute]]]

    public_initiator_attributes: list[list[Attribute]] = Field(
        description="""Attributes that the recipient already knows about the initiator.

        This is used to prevent a party B from becoming a man-in-the-middle by forwarding an exchange with A to C. 
        The intended recipient should know the value of these attributes already, such that party C will
        notice that a request was initiated by A and not by B, if B tries to forward A's request to C.
        """,
    )

