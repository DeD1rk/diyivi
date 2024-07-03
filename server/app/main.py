import json

from fastapi import FastAPI

# from app.exchanges.api import router as exchanges_router

app = FastAPI(
    title="DIYivi",
    summary="Backend for DIYivi, a DIY tool for exchanging Yivi attributes.",
)

# app.include_router(exchanges_router, prefix="/exchanges")


def output_schema():
    schema = app.openapi()
    print(json.dumps(schema, indent=2))
