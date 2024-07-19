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

def LLM_call(user_query):
    api_key=os.environ.get("WATSONX_APIKEY")
    ibm_cloud_url=os.environ.get("WATSONX_URL")
    project_id=os.environ.get("WATSONX_PROJECT_ID")

    params = {
    	"decoding_method": "greedy",
		"max_new_tokens": 100,
		"stop_sequences": ["\\n"],
		"repetition_penalty": 1
}
    chat = ChatWatsonx(
        model_id="ibm/granite-13b-instruct-v2",
        url=ibm_cloud_url,
        project_id=project_id,
        params=params,
    )

    prompt = f"""input: Extract all countries from the customer queries. Input: Im travelling to Istanbul and Paris. What are the roaming charges? Output: Turkey, France Input: Im travelling to Norway. Output: Norway
    Input: {user_query} 
    Output:"""

    
    messages = [HumanMessage(prompt)]
    ai_msg = chat.invoke(messages)
    # print('The LLM response: ', ai_msg.content)
    return(ai_msg.content)

def LLM_roaming_query(user_query, roaming_charges):

    api_key=os.environ.get("WATSONX_APIKEY")
    ibm_cloud_url=os.environ.get("WATSONX_URL")
    project_id=os.environ.get("WATSONX_PROJECT_ID")

    params = {
    	"decoding_method": "greedy",
		"max_new_tokens": 300,
		"repetition_penalty": 1
}
    chat = ChatWatsonx(
        model_id="ibm/granite-13b-chat-v2",
        url=ibm_cloud_url,
        project_id=project_id,
        params=params,
    )

    prompt = f"""You are a helpful customer service representative assisting customers with their roaming queries. 
    Answer user query based on information provided within #roaming information#. 
    Roaming information will be given to you in a 2D Array which follows the following format: [[country1, country1 roaming cost], [country2, country2 roaming cost]]. 
    Do not use any information outside of that provided. \n #roaming information# {roaming_charges} \n
     query: {user_query} \n answer: 
 """
    
    messages = [HumanMessage(prompt)]
    ai_msg = chat.invoke(messages)
    return(ai_msg.content)

def plan_type_and_country_to_roaming_cost_query(
    plan_type: str,
    country: str
):
    sql_query = (f"""
            SELECT cost
            FROM public.vodafone_roaming_charges
            WHERE plan_type='{plan_type}' AND country='{country}'""")
    
    response = postgres.postgres(sql_query)
    
    roaming_charge = response[0][0]
    return({"response": roaming_charge})

def main(phone_number, country_prompt):
    # query = 'Im travelling to Belgium and Denmark. What are the roaming charges'
    query=f'{country_prompt}'

    countries = (LLM_call(query))

    countries.strip()
    countries.replace('\n','')
    countries.replace("'","")
    countries = countries.split(',')


    plan_type = phone_number_to_plan_type_query(phone_number)

    country_array = []


    for country in countries : 
        roaming_charge = plan_type_and_country_to_roaming_cost_query(plan_type, country.strip())
        country_array.append([country, roaming_charge["response"]])

    query_response = LLM_roaming_query(query,country_array)
    return (query_response)