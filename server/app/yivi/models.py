import logging
from collections.abc import Sequence
from datetime import UTC, datetime
from enum import StrEnum
from typing import Annotated, Any, Literal, Self

import jwt
from pydantic import BaseModel, ConfigDict, Field, PlainSerializer, ValidationError, model_validator

from app.config import settings

logger = logging.getLogger(__name__)

Attribute = Annotated[
    str,
    Field(
        pattern=r"^([a-zA-Z0-9_-]+\.){3}[a-zA-Z0-9_-]+$",
        examples=[
            "pbdf.gemeente.personalData.firstnames",
            "pbdf.sidn-pbdf.mobilenumber.mobilenumber",
        ],
    ),
]

Timestamp = Annotated[datetime, PlainSerializer(lambda x: int(x.timestamp()), return_type=int)]


class SessionStatus(StrEnum):
    """Status of an IRMA session.

    See: https://github.com/privacybydesign/irmago/blob/v0.15.2/messages.go#L217-L222
    """

    INITIALIZED = "INITIALIZED"
    PAIRING = "PAIRING"
    CONNECTED = "CONNECTED"
    CANCELLED = "CANCELLED"
    DONE = "DONE"
    TIMEOUT = "TIMEOUT"


class ProofStatus(StrEnum):
    """Status of a proof in an IRMA session.

    See: https://github.com/privacybydesign/irmago/blob/v0.15.2/verify.go#L23-L28
    """

    VALID = "VALID"
    INVALID = "INVALID"
    INVALID_TIMESTAMP = "INVALID_TIMESTAMP"
    UNMATCHED_REQUEST = "UNMATCHED_REQUEST"
    MISSING_ATTRIBUTES = "MISSING_ATTRIBUTES"
    EXPIRED = "EXPIRED"


class AttributeProofStatus(StrEnum):
    """Status of a single attribute in an IRMA session.

    See: https://github.com/privacybydesign/irmago/blob/v0.15.2/verify.go#L30-L32
    """

    PRESENT = "PRESENT"
    EXTRA = "EXTRA"
    NULL = "NULL"


class TranslatedString(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    default: str = Field(alias="")
    nl: str = Field()
    en: str = Field()


class AttributeValue(BaseModel):
    type: Attribute
    value: str | None = None
    not_null: bool | None = Field(alias="notNull", default=None)

    @model_validator(mode="after")
    def check_value_or_not_null(self) -> Self:
        if self.value is None and self.not_null is None:
            raise ValueError("value or notNull must be set")
        elif self.value is not None and self.not_null is not None:
            raise ValueError("value and notNull cannot both be set")
        return self


class _BaseRequest(BaseModel):
    disclose: list[list[list[Attribute]]] = Field(
        description="ConDisCon of attributes to disclose."
    )

    client_return_url: str | None = Field(
        description="URL to which the device with the Yivi app should return after the session.",
        alias="clientReturnUrl",
        default=None,
    )

    augment_return_url: bool | None = Field(
        description="Whether to augment the client return URL with the session token.",
        alias="augmentReturnUrl",
        default=None,
    )


class DisclosureRequest(_BaseRequest):
    """Request for disclosure of attributes.

    See: https://irma.app/docs/session-requests/#disclosure-requests
    """

    context: Literal["https://irma.app/ld/request/disclosure/v2"] = Field(
        alias="@context",
        default="https://irma.app/ld/request/disclosure/v2",
    )


class SignatureRequest(_BaseRequest):
    """Request for an attribute-based signature.

    See: https://irma.app/docs/session-requests/#attribute-based-signature-requests
    """

    context: Literal["https://irma.app/ld/request/signature/v2"] = Field(
        alias="@context",
        default="https://irma.app/ld/request/signature/v2",
    )

    message: str = Field(min_length=1)


class _BaseExtendedRequest(BaseModel):
    validity: int | None = Field(
        description="Validity of session result JWT in seconds.",
        default=None,
        ge=0,
    )

    timeout: int | None = Field(
        description="Wait this many seconds"
        " for the Yivi app to connect before the session times out.",
        default=None,
        ge=0,
    )

    callback_url: str | None = Field(
        alias="callbackUrl",
        description="URL to which the IRMA server should post the session result.",
        default=None,
    )


class ExtendedDisclosureRequest(_BaseExtendedRequest):
    """Request for disclosure of attributes with additional options.

    See: https://irma.app/docs/session-requests/#extra-parameters
    """

    request: DisclosureRequest


class ExtendedSignatureRequest(_BaseExtendedRequest):
    """Request for disclosure of attributes with additional options.

    See: https://irma.app/docs/session-requests/#extra-parameters
    """

    request: SignatureRequest


class _BaseSessionRequestJWT(BaseModel):
    iss: str = settings.irma.session_request_issuer_id
    iat: Timestamp = Field(default_factory=lambda: datetime.now(UTC))

    def signed_jwt(self) -> str:
        return jwt.encode(
            self.model_dump(exclude_none=True, by_alias=True),
            settings.irma.session_request_secret_key.get_secret_value(),
            algorithm="HS256",
        )


class DisclosureRequestJWT(_BaseSessionRequestJWT):
    sub: Literal["verification_request"] = "verification_request"
    sprequest: ExtendedDisclosureRequest


class SignatureRequestJWT(_BaseSessionRequestJWT):
    sub: Literal["signature_request"] = "signature_request"
    absrequest: ExtendedSignatureRequest


class DisclosedAttribute(BaseModel):
    id: Attribute
    status: AttributeProofStatus
    rawvalue: str | None
    value: TranslatedString
    issuancetime: Timestamp

    def satisfies(self, value: Attribute | AttributeValue) -> bool:
        if isinstance(value, AttributeValue):
            return self.id == value.type and (
                (value.not_null is None and self.rawvalue == value.value)
                or (value.not_null is True and self.status != AttributeProofStatus.NULL)
                or (value.not_null is False and self.status == AttributeProofStatus.NULL)
            )
        return self.id == value


class _BaseSessionResultJWT(BaseModel):
    """Base class for session result JWTs."""

    iss: str = Field(
        description="Name of the current irma server as defined in its configuration.",
    )
    iat: Timestamp = Field(
        description="Unix timestamp indicating when this JWT was created",
    )
    exp: Timestamp = Field(
        description="Unix timestamp indicating until when this JWT is valid",
    )

    status: SessionStatus
    token: str

    proof_status: ProofStatus = Field(
        alias="proofStatus",
    )

    disclosed: list[list[DisclosedAttribute]] = Field(default_factory=list)

    @property
    def is_successful(self) -> bool:
        return (
            self.disclosed is not None
            and self.status == SessionStatus.DONE
            and self.proof_status == ProofStatus.VALID
        )

    def satisfies_condiscon(
        self, condiscon: Sequence[Sequence[Sequence[Attribute | AttributeValue]]]
    ) -> bool:
        """Return whether this session result satisfies the given ConDisCon.

        This result needs to be successful and the disclosed attributes need to match.
        That is, a disclosure should have the same number of elements as the number of
        disjunctions in the ConDisCon, and each disjunction should be satisfied by the
        disclosed attributes in the element at the same index.
        """
        if (
            self.disclosed is None
            or len(self.disclosed) != len(condiscon)
            or not self.is_successful
        ):
            return False

        for disjunction, disclosed in zip(condiscon, self.disclosed):
            if not satisfies_disjunction(disjunction, disclosed):
                return False

        return True

    @classmethod
    def parse_jwt(cls, raw_result: str) -> Self:
        """Parse and verify a session result JWT.

        :raises jwt.InvalidTokenError: If the input is not a valid JWT.
        :raises pydantic.ValidationError: If the input is not a valid session result.
        """
        try:
            result_dict = jwt.decode(
                raw_result,
                settings.irma.server_public_key,
                algorithms=["RS256"],
                # Allow for some inconsistency in system clocks between irma server and diyivi.
                # This can be necessary when the irma server is running on a different machine.
                leeway=5,
            )
            # The actual result type depends on the subclass this is called on.
            return cls.model_validate(result_dict)
        except jwt.InvalidTokenError:
            logger.debug("Invalid JWT", exc_info=True)
            raise
        except ValidationError:
            logger.debug("Invalid session result in JWT", exc_info=True)
            raise


class DisclosureSessionResultJWT(_BaseSessionResultJWT):
    """The result of a disclosure session, signed by the `irma server`."""

    sub: Literal["disclosing_result"] = "disclosing_result"
    type: Literal["disclosing"] = "disclosing"


class SignedMessage(BaseModel):
    """An attribute-based signature including the message.

    This is very loosely typed, as actual verification can be done by an `irma server`.
    """

    ldcontext: Literal["https://irma.app/ld/request/disclosure/v2"] = Field(alias="@context")
    signature: list[dict[str, str | dict[str, str]]]
    indices: list[list[dict[str, int]]]
    nonce: str
    context: str
    message: str
    timestamp: dict[str, Any]


class SignatureSessionResultJWT(_BaseSessionResultJWT):
    """The result of a signature session, signed by the `irma server`."""

    sub: Literal["signing_result"] = "signing_result"
    type: Literal["signing"] = "signing"

    signature: SignedMessage


def satisfies_disjunction(
    disjunction: Sequence[Sequence[Attribute | AttributeValue]],
    disclosed: Sequence[DisclosedAttribute],
) -> bool:
    return any(satisfies_conjunction(conjunction, disclosed) for conjunction in disjunction)


def satisfies_conjunction(
    conjunction: Sequence[Attribute | AttributeValue],
    disclosed: Sequence[DisclosedAttribute],
) -> bool:
    for required_attribute in conjunction:
        if any(attribute.satisfies(required_attribute) for attribute in disclosed):
            continue
        return False
    return True
