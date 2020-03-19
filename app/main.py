from fastapi import FastAPI
from app.api.api_v1.api import api_router
from app.core import config

app = FastAPI(title=config.PROJECT_NAME, openapi_url="/api/v1/openapi.json")

app.include_router(api_router, prefix=config.API_V1_STR)
