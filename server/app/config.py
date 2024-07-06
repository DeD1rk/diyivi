from pydantic import BaseModel, Field, HttpUrl, SecretStr
from pydantic_settings import BaseSettings


class IRMAServerConfig(BaseModel):
    server_url: HttpUrl = Field(
        description="URL of the IRMA server to use.",
        default="http://localhost:8088",
    )

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
        default="unsafe_secret_key",
    )

    session_request_issuer_id: str = Field(
        description="Issuer ID to use in session request JWTs. This tells the IRMA server which key to verify a session request JWT with.",
        default="diyivi",
    )


class Settings(BaseSettings):
    base_url: HttpUrl = Field(
        description="Base URL of the DIYivi API.",
        default="http://localhost:8000",
    )

    irma: IRMAServerConfig = IRMAServerConfig()


settings = Settings()

__all__ = ["settings"]
