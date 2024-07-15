import logging, os
from logging import getLogger
from fastapi import FastAPI, Security
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
from auth import authenticate_api_key

from endpoints.router import router as api

load_dotenv()

log_levels = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}

LOG_LEVEL = log_levels[os.environ.get("LOG_LEVEL", "INFO").upper()]

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        # logging.FileHandler("app.log"), # for logging to file
        logging.StreamHandler()
    ],
)

logger = getLogger(__name__)

app = FastAPI()

app.include_router(api, prefix="/api", tags=["example"])

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    logging.debug("Healthcheck endpoint called")
    return {"message": "UP!"}


@app.get("/protected")
def protected_route(api_key: str = Security(authenticate_api_key)):
    # Process the request for authenticated users
    return {"message": "Access granted!"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="OpenAPI UI",
        version="3.0.0",
        description="Generated OpenAPI 3.0.0 version for Watson Assistant",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    servers = [
        {
            "url": os.environ.get(
                "CODE_ENGINE_PROJECT_URL", "Code engine url not specified"
            ),
        },
        {
            "url": "http://127.0.0.1:8080",
        },
    ]
    openapi_schema["servers"] = servers

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
