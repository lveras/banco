from fastapi import FastAPI
import uvicorn
from app.api.api_v1.api import api_router
from app.core import config
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI(title=config.PROJECT_NAME, openapi_url="/api/v1/openapi.json")

app.include_router(api_router, prefix=config.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
