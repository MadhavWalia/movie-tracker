from functools import lru_cache
from http import HTTPStatus
import uuid

from fastapi import APIRouter, Body, Depends
from api.dto.movie import CreateMovieBody
from api.entities.movie import Movie
from api.repository.movie.abstractions import MovieRepository
from api.repository.movie.mongo import MongoMovieRepository

from api.responses.movie import MovieCreatedResponse
from api.settings import Settings


router = APIRouter(prefix="/api/v1/movies", tags=["movies"])


@lru_cache()
def settings_instance():
    """
    Creates a singleton instance of Fast API Settings Dependency
    """
    return Settings()


@lru_cache()
def movie_repository(settings: Settings = Depends(settings_instance)):
    """
    Creates a singleton instance of Movie Repository Dependency
    """
    return MongoMovieRepository(
        connection_string=settings.mongo_connection_string,
        database=settings.mongo_database_name,
    )


@router.post("/", status_code=HTTPStatus.CREATED, response_model=MovieCreatedResponse)
async def create_movie(
    movie: CreateMovieBody = Body(..., title="my_title", description="my_description"),
    repo: MovieRepository = Depends(movie_repository),
):
    """
    Creates a movie

    """
    movie_id = str(uuid.uuid4())

    await repo.create(
        movie=Movie(
            movie_id=movie_id,
            title=movie.title,
            description=movie.description,
            released_year=movie.released_year,
            watched=movie.watched,
        )
    )
    return MovieCreatedResponse(movie_id=movie_id)
