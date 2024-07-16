from fastapi import APIRouter, Response, Security, requests, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from langchain_ibm import ChatWatsonx
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage


from endpoints.data_model import String_Response, Roaming

from dotenv import load_dotenv

from auth import authenticate_api_key

from services.postgres import QueryPostgres

import logging, os, json

router = APIRouter()
load_dotenv()

api_key=os.environ.get("WATSONX_APIKEY")
ibm_cloud_url=os.environ.get("WATSONX_URL")
project_id=os.environ.get("WATSONX_PROJECT_ID")

params = {
    "decoding_method": "greedy",
    "max_new_tokens": 200,
    "min_new_tokens": 1,
}

chat = ChatWatsonx(
    model_id="mistralai/mixtral-8x7b-instruct-v01",
    url=ibm_cloud_url,
    project_id=project_id,
    params=params,
)

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

@router.post("/phone-number-sql-query", response_model=String_Response)
async def phone_number_to_plan_type(
    phone_number: str,
    api_key: str = Security(authenticate_api_key)
):
    response = postgres.postgres(f"""
            SELECT plan_type
            FROM customer 
            WHERE mobile_number ='{phone_number}';
        """)
    plan_type = response[0][0]
    return({"response": plan_type})