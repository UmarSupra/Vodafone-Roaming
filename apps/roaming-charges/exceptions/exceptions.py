from fastapi import HTTPException

class PayLoadError(HTTPException):
    def __init__(self, detail="There was an issue with payload"):
        super().__init__(status_code=500, detail=detail)