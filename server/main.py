import json

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.exchanges.api import router as exchanges_router

app = FastAPI(
    title="DIYivi",
    summary="Backend for DIYivi, a DIY tool for exchanging Yivi attributes.",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(exchanges_router, prefix="/api/exchanges")


def output_schema():
    schema = app.openapi()
    print(json.dumps(schema, indent=2))  # noqa: T201


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
