import os,logging
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
import os
api_key_header = APIKeyHeader(name="X-API-Key")
def authenticate_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in os.environ.get("CLIENT_API_KEY"):
        return api_key_header
    raise HTTPException(401, "Invalid api key")

