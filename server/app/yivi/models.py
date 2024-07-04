from enum import StrEnum
from typing import Annotated, Literal, Self

import jwt
from pydantic import BaseModel, Field, model_validator

from app.config import settings

Attribute = Annotated[
    str,
    Field(
        pattern=r"^([a-zA-Z0-9_-]+\.){3}[a-zA-Z0-9_-]+$",
        examples=[
            "irma-demo.gemeente.personalData.firstnames",
            "pbdf.sidn-pbdf.mobilenumber.mobilenumber",
        ],
    ),
]

TranslatedString = Annotated[
    dict[str, str], Field(examples=[{"en": "Hello world!", "nl": "Hallo wereld!"}])
]


class AttributeValue(BaseModel):
    type: Attribute
    value: str | None
    not_null: bool | None = Field(serialization_alias="notNull", default=None)

    @model_validator(mode="after")
    def check_value_or_not_null(self) -> Self:
        if self.value is None and self.not_null is None:
            raise ValueError("value or notNull must be set")
        elif self.value is not None and self.not_null is not None:
            raise ValueError("value and notNull cannot both be set")
        return self


class DisclosureRequest(BaseModel):
    """Request for disclosure of attributes.

    See: https://irma.app/docs/session-requests/#disclosure-requests
    """

    context: Literal["https://irma.app/ld/request/disclosure/v2"] = Field(
        serialization_alias="@context",
        default="https://irma.app/ld/request/disclosure/v2",
    )

    disclose: list[list[list[Attribute]]] = Field(
        description="ConDisCon of attributes to disclose."
    )

    labels: (
        dict[
            Annotated[str, Field(pattern=r"^(0|([1-9]\d*))$")],
            TranslatedString,
        ]
        | None
    ) = Field(
        description="Optional labels for disjunctions. "
        "See: https://irma.app/docs/session-requests/#disjunction-labels",
        default=None,
    )

    client_return_url: str | None = Field(
        description="URL to which the device with the Yivi app should return after the session.",
        serialization_alias="clientReturnUrl",
    )

    augment_return_url: bool | None = Field(
        description="Whether to augment the client return URL with the session token.",
        serialization_alias="augmentReturnUrl",
        default=None,
    )

    @model_validator(mode="after")
    def check_label_keys(self) -> Self:
        num_disjunctions = len(self.disclose)
        if self.labels is not None:
            for key in self.labels.keys():
                if int(key) >= num_disjunctions:
                    raise ValueError("label key does not correspond to a disjunction")
        return self


class ExtendedDisclosureRequest(BaseModel):
    """Request for disclosure of attributes with additional options.

    See: https://irma.app/docs/session-requests/#extra-parameters
    """

    validity: int | None = Field(
        description="Validity of session result JWT in seconds.",
        default=None,
        ge=0,
    )

    timeout: int | None = Field(
        description="Wait this many seconds for the Yivi app to connect before the session times out.",
        default=None,
        ge=0,
    )

    callback_url: str | None = Field(
        serialization_alias="callbackUrl",
        description="URL to which the IRMA server should post the session result.",
        default=None,
    )

    request: DisclosureRequest

    def signed_jwt(self) -> str:
        return jwt.encode(
            self.model_dump(),
            settings.irma.secret_key,
            algorithm="HS256",
        )


class DisclosedAttribute(BaseModel):
    id: Attribute
    status: str
    rawvalue: str | None
    value: TranslatedString

    def satisfies(self, value: Attribute | AttributeValue) -> bool:
        if isinstance(value, AttributeValue):
            return self.id == value.type and (
                (value.not_null is None and self.rawvalue == value.value)
                or (value.not_null is True and self.rawvalue is not None)
                or (value.not_null is False and self.rawvalue is None)
            )
        return self.id == value
