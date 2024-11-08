import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.exchanges.api import router as exchanges_router
from app.signatures.api import router as signatures_router

app = FastAPI(
    title="DIYivi",
    summary="Backend for DIYivi, a DIY tool for exchanging Yivi attributes.",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.client_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(exchanges_router, prefix="/api/exchanges")
app.include_router(signatures_router, prefix="/api/signatures/requests")


def output_schema():
    schema = app.openapi()
    print(json.dumps(schema, indent=2))  # noqa: T201
