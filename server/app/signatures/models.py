import secrets

from pydantic import BaseModel, EmailStr, Field

from app.yivi.models import Attribute, Timestamp


class SignatureRequest(BaseModel):
    """A request for someone to sign a message, as saved in the backend."""

    id: str = Field(
        min_length=16,
        max_length=16,
        pattern="^[0-9a-f]{16}$",
        default_factory=lambda: secrets.token_hex(8),
    )

    message: str = Field(min_length=1, max_length=64_000)
    attributes: list[Attribute] = Field(min_length=1)

    initiator_email_value: EmailStr | None = Field(
        default=None,
        description="The initiator's disclosed email address.",
    )
    expire_at: Timestamp = Field(
        description="Unix timestamp indicating when this request will be removed.",
    )


class CreateSignatureRequestRequest(BaseModel):
    message: str = Field(min_length=1, max_length=64_000)
    attributes: list[Attribute] = Field(min_length=1)


class SignatureRequestResponse(BaseModel):
    id: str = Field(
        min_length=16,
        max_length=16,
        pattern="^[0-9a-f]{16}$",
    )
    request_jwt: str = Field(
        description="JWT containing a disclosure request for the initiator's email.",
    )


class RecipientSignatureRequestResponse(BaseModel):
    attributes: list[Attribute]
    message: str = Field(min_length=1, max_length=64_000)
    initiator_email_value: EmailStr = Field(
        description="The initiator's disclosed email address.",
    )
    request_jwt: str = Field(
        description="JWT containing a signing request for the recipient.",
    )
