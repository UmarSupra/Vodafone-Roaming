from services.postgres import QueryPostgres

from langchain_ibm import ChatWatsonx
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

from dotenv import load_dotenv
import os


postgres = QueryPostgres()

def phone_number_to_plan_type_query(
    phone_number: str,
):
    response = postgres.postgres(f"""
            SELECT plan_type
            FROM customer 
            WHERE mobile_number='{phone_number}';
        """)
    plan_type = response[0][0]
    return(plan_type)

def LLM_call():
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

    messages = [HumanMessage("What country if Paris in?")]
    ai_msg = chat.invoke(messages)
    return(ai_msg.content)

def plan_type_and_country_to_roaming_cost_query(
    plan_type: str,
    country_from: str,
    country_to:str
):
    response = postgres.postgres(f"""
            SELECT cost
            FROM customer 
            WHERE plan_type='{plan_type}' AND address='{country}';
        """)
    
    roaming_charge = response[0][0]
    return({"response": roaming_charge})

def main(phone_number, from_country_name, to_country_name):
    LLM_response = (LLM_call())
    plan_type = phone_number_to_plan_type_query(phone_number)
    roaming_charge = plan_type_and_country_to_roaming_cost_query(plan_type, country_from, country_to)
    return (roaming_charge)