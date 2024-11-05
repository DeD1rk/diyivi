from pydantic import BaseModel, Field, HttpUrl, SecretStr
from pydantic_settings import BaseSettings


class IRMAServerSettings(BaseModel):
    server_public_key: bytes = Field(
        default=b"""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAjzh9XSDMKri2hJ5jpgSR
GySiAJ8SlfMwlTHeHNoKUzFlAgRN6CGzZWT2LVU30CWmRwfrZb3v1FPFkr2TyPnm
LUy3GwMsfclbjGd6oyzsSY+lREsyeYLKEN3gLb14dm8JTTILlcmkJEnmgIidiIrg
mBYoMjMDFo+1OB1aBTMnoe7XP8Wq7MbSNg9UKQblsHdIH1dkIVjI4ZXLgedNWakD
aoVW0whK9oUw9dxKjKCxiUd/vU25R2OGr0ipK6afMiaUFOXq5ku79wa7ZbmD6KZp
dzGoU63CTCQZrPw/g8vgNXNr65J7XKQBuEzJOh/3opwxHVjjyb77XeWQOTIQxNcP
8wIDAQAB
-----END PUBLIC KEY-----""",
        description="Public key of the IRMA server to use for verifying session result JWTs.",
    )

    session_request_secret_key: SecretStr = Field(
        description="Secret key to use for signing irma session request JWTs.",
        default=SecretStr("unsafe_secret_key"),
    )

    session_request_issuer_id: str = Field(
        description="Issuer ID to use in session request JWTs. "
        "This tells the IRMA server which key to verify a session request JWT with.",
        default="diyivi",
    )


class SMTPSettings(BaseModel):
    hostname: str
    username: str
    password: str


class Settings(BaseSettings):
    base_url: HttpUrl = Field(
        description="Base URL of the DIYivi API.",
        default="http://localhost:8000/",
    )

    client_origin: str = Field(
        description="Origin of the client application for CORS.",
        default="http://localhost:5173",
    )

    irma: IRMAServerSettings = IRMAServerSettings()

    redis_url: str | None = Field(
        default=None,
        description="URL of the Redis server to use.",
        examples=["redis://localhost:6379/0"],
    )

    exchange_ttl_before_start: int = Field(
        default=600,
        description="""Time in seconds to store an exchange before it starts.

        If an exchange is not started within this time, it will be deleted.
        This currently does not apply when no Redis storage is configured.
        """,
    )

    exchange_ttl: int = Field(
        default=3600 * 48,
        description="""Time in seconds to store an exchange that has started.

        After this time, an exchange and its replies will be deleted.
        This currently does not apply when no Redis storage is configured.
        """,
    )

    session_request_validity: int | None = Field(
        default=None,
        description="Time in seconds for which a Yivi session request JWT is valid.",
    )

    email_attribute: str = Field(
        default="pbdf.sidn-pbdf.email.email",
        description="Attribute ID for an email address to send emails to.",
    )

    email_from_domain: str = Field(
        default="localhost", description="Sender domain for outgoing email."
    )

    smtp: SMTPSettings | None = Field(
        default=None,
        description="Configuration for outgoing email.",
    )


settings = Settings()

__all__ = ["settings"]
