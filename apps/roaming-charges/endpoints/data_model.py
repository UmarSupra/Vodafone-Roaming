from pydantic import BaseModel

class List_Response(BaseModel):
    response: list[str]

class String_Response(BaseModel):
    response: str