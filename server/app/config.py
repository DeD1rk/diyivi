from pydantic import BaseModel, Field, HttpUrl
from pydantic_settings import BaseSettings


class IRMAServerConfig(BaseModel):
    server_url: HttpUrl = Field(
        description="URL of the IRMA server to use.",
        default="http://localhost:8088",
    )

    secret_key: str = Field(
        description="Secret key to use for signing and verifying JWTs between DIYivi and the IRMA server.",
        default="unsafe_secret_key",
    )

    issuer_id: str = Field(
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
