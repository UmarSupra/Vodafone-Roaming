## Vodafone Roaming FastAPI Webservice

Create and activate a virtual environment using venv tpye:

python3 -m venv venv
source venv/bin/activate

## Run Vodafone Roaming FastAPI Webservice

Run the application on port 8080 with  
pip3 install -r requirements.txt  
uvicorn main:app --port 8080 --reload

## Access Open API UI

http://127.0.0.1:8080/docs

## Access Open API spec for Watson Assistant to import into Watson Assistant (if needs be)

http://127.0.0.1:8080/openapi.json