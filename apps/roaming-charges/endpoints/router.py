from fastapi import APIRouter, Response, Security, requests, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from endpoints.data_model import genericResponse

from dotenv import load_dotenv

from auth import authenticate_api_key


import logging, os, json

router = APIRouter()
load_dotenv()

@router.post("/random", response_model=genericResponse)
async def random_function(
    api_key: str = Security(authenticate_api_key)
):
    return JSONResponse(content=jsonable_encoder("hi"))