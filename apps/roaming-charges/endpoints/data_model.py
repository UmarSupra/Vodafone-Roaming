from pydantic import BaseModel, Field

class String_Response(BaseModel):
    str

class Roaming(BaseModel):
    country: str = Field(..., description="a location")