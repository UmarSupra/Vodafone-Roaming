from fastapi import APIRouter, Security, HTTPException

from endpoints.data_model import String_Response, Roaming

from auth import authenticate_api_key

from services.postgres import QueryPostgres

from services.get_roaming_charge import main


router = APIRouter()

postgres = QueryPostgres()

@router.post("/get-roaming-cost", response_model=str)
async def get_roaming_cost(
    phone_number: str,
    country_prompt: str,
    api_key: str = Security(authenticate_api_key)
):
    return main(phone_number, country_prompt)