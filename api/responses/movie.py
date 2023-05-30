from pydantic import BaseModel


class MovieCreatedResponse(BaseModel):
    movie_id: str
