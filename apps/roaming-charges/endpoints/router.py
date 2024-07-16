from fastapi import APIRouter, Response, Security, requests, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from endpoints.data_model import List_Response
from endpoints.data_model import String_Response

from dotenv import load_dotenv

from auth import authenticate_api_key

from services.postgres import QueryPostgres

import logging, os, json

router = APIRouter()
load_dotenv()

postgres = QueryPostgres()

@router.post("/random", response_model=String_Response)
async def random_function(
    api_key: str = Security(authenticate_api_key)
):
    return {"response":"hi"}

@router.post("/random2")
async def random_function_2(
    query: str,
    api_key: str = Security(authenticate_api_key)
):
    response = postgres.postgres(query)
    return response