import uuid
from collections import namedtuple
from functools import lru_cache
from http import HTTPStatus

from fastapi import APIRouter, Body, Depends, Path, Query, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from api.dto.detail import DetailResponse
from api.dto.movie import (
    CreateMovieBody,
    MovieCreatedResponse,
    MovieResponse,
    UpdateMovieBody,
)
from api.entities.movie import Movie
from api.repository.movie.abstractions import MovieRepository, RepositoryException
from api.repository.movie.mongo import MongoMovieRepository
from api.settings import Settings, settings_instance

router = APIRouter(prefix="/api/v1/movies", tags=["movies"])


@lru_cache()
def movie_repository(settings: Settings = Depends(settings_instance)):
    """
    Creates a singleton instance of Movie Repository Dependency
    """
    return MongoMovieRepository(
        connection_string=settings.mongo_connection_string,
        database=settings.mongo_database_name,
    )


def pagination_params(
    skip: int = Query(0, title="Page", description="The page number", ge=0),
    limit: int = Query(1000, title="Limit", description="The page size", ge=0, le=1000),
):
    """
    Pagination parameters
    """
    return namedtuple("Pagination", ["skip", "limit"])(skip, limit)


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
    return MovieCreatedResponse(id=movie_id)


@router.get(
    "/{movie_id}",
    responses={
        HTTPStatus.OK.value: {"model": MovieResponse, "description": "Movie found"},
        HTTPStatus.NOT_FOUND.value: {
            "model": DetailResponse,
            "description": "Movie not found",
        },
    },
)
async def get_movie_by_id(
    movie_id: str, repo: MovieRepository = Depends(movie_repository)
):
    """
    Returns a movie by id if found, otherwise returns None
    """
    movie = await repo.get_by_id(movie_id=movie_id)
    if movie is None:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND.value,
            content=jsonable_encoder(
                DetailResponse(message=f"Movie with id {movie_id} not found")
            ),
        )
    return MovieResponse(
        id=movie.id,
        title=movie.title,
        description=movie.description,
        released_year=movie.released_year,
        watched=movie.watched,
    )


@router.get("/", response_model=list[MovieResponse])
async def get_movie_by_title(
    title: str = Query(
        ..., title="Title", description="The title of the movie", min_length=3
    ),
    pagination: namedtuple = Depends(pagination_params),
    repo: MovieRepository = Depends(movie_repository),
):
    movies = await repo.get_by_title(
        title=title, skip=pagination.skip, limit=pagination.limit
    )
    movie_return_value = []
    for movie in movies:
        movie_return_value.append(
            MovieResponse(
                id=movie.id,
                title=movie.title,
                description=movie.description,
                released_year=movie.released_year,
                watched=movie.watched,
            )
        )
    return movie_return_value


@router.patch(
    "/{movie_id}",
    responses={
        HTTPStatus.OK.value: {"model": DetailResponse},
        HTTPStatus.NOT_FOUND.value: {"model": DetailResponse},
    },
)
async def update_movie(
    movie_id: str = Path(..., title="Movie Id", description="The id of the movie"),
    update_parameters: UpdateMovieBody = Body(
        ..., title="Update Body", description="The parameters to be updated"
    ),
    repo: MovieRepository = Depends(movie_repository),
):
    """
    Updates a movie
    """
    try:
        await repo.update(
            movie_id=movie_id,
            update_parameters=update_parameters.dict(
                exclude_unset=True, exclude_none=True
            ),
        )
        return DetailResponse(message=f"Movie with id {movie_id} updated")
    except RepositoryException as e:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND.value,
            content=jsonable_encoder(DetailResponse(message=str(e))),
        )


@router.delete("/{movie_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_movie(
    movie_id: str = Path(..., title="Movie Id", description="The id of the movie"),
    repo: MovieRepository = Depends(movie_repository),
):
    await repo.delete(movie_id=movie_id)
    return Response(status_code=HTTPStatus.NO_CONTENT.value)
