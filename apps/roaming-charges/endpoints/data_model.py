from pydantic import BaseModel

class genericResponse(BaseModel):
    response: list[str]