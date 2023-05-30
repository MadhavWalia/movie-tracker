import datetime
from pydantic import BaseModel, validator


class CreateMovieBody(BaseModel):
    """
    Used as the request body for creating a movie endpoint.
    """

    title: str
    description: str
    released_year: int
    watched: bool = False

    @validator("title")
    def title_length_gt_three(cls, v):
        if len(v) < 4:
            raise ValueError("title must be at least 3 characters long")
        return v

    @validator("description")
    def description_length_gt_three(cls, v):
        if len(v) < 4:
            raise ValueError("description must be at least 3 characters long")
        return v

    @validator("released_year")
    def released_year_gt_1900(cls, v):
        if v < 1900:
            raise ValueError("released_year must be greater than 1900")
        return v

    @validator("released_year")
    def released_year_lt_curr(cls, v):
        today = datetime.datetime.today()
        if v > today.year:
            raise ValueError("released_year must be less than current year")
        return v
