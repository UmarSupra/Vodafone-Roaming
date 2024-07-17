from fastapi import APIRouter, Security, HTTPException

from endpoints.data_model import String_Response, Roaming

from auth import authenticate_api_key

from services.postgres import QueryPostgres

from services.get_roaming_charge import main


router = APIRouter()

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

@router.post("/get-roaming-cost")
async def get_roaming_cost(
    phone_number: str,
    from_country_name: str,
    to_country_name: str
):
    return main(phone_number, from_country_name, to_country_name)