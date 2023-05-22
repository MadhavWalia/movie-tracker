from pydantic import BaseModel


class DetailResponse(BaseModel):
    message: str
