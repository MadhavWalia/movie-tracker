import functools
import pytest
from api._tests.fixture import test_client
from api.entities.movie import Movie
from api.handlers.movie_v1 import movie_repository
from api.repository.movie.memory import MemoryMovieRepository


def memory_repository_dependency(dependency):
    return dependency


@pytest.mark.asyncio()
async def test_create_movie(test_client):
    # Setup Phase
    repo = MemoryMovieRepository()
    partial_dependency = functools.partial(memory_repository_dependency, repo)

    test_client.app.dependency_overrides[movie_repository] = partial_dependency

    # Test Phase
    result = test_client.post(
        "/api/v1/movies/",
        json={
            "title": "string",
            "description": "string",
            "released_year": 2000,
            "watched": False,
        },
    )

    # Assertion Phase
    movie_id = result.json().get("id")
    assert result.status_code == 201
    movie = await repo.get_by_id(movie_id=movie_id)
    assert movie is not None


@pytest.mark.parametrize(
    "movie_json",
    [
        (
            {
                "description": "string",
                "released_year": 2000,
                "watched": False,
            }
        ),
        (
            {
                "title": "string",
                "released_year": 2000,
                "watched": False,
            }
        ),
        (
            {
                "title": "string",
                "description": "string",
                "released_year": 0,
                "watched": False,
            }
        ),
        (
            {
                "title": "string",
                "description": "string",
                "released_year": 2025,
                "watched": False,
            }
        ),
        (
            {
                "title": "string",
                "description": "string",
                "watched": False,
            }
        ),
    ],
)
@pytest.mark.asyncio()
async def test_create_movie_validation_error(test_client, movie_json):
    # Setup Phase
    repo = MemoryMovieRepository()
    partial_dependency = functools.partial(memory_repository_dependency, repo)

    test_client.app.dependency_overrides[movie_repository] = partial_dependency

    # Test Phase
    result = test_client.post(
        "/api/v1/movies/",
        json=movie_json,
    )

    # Assertion Phase
    assert result.status_code == 422


@pytest.mark.parametrize(
    "movie_seed, movie_id, expected_status_code, expected_result",
    [
        pytest.param(
            [],
            "random_id",
            404,
            {"message": "Movie with id random_id not found"},
            id="movie not found",
        ),
        pytest.param(
            [
                Movie(
                    movie_id="found_id",
                    title="my_title",
                    description="my_description",
                    released_year=2020,
                    watched=False,
                )
            ],
            "found_id",
            200,
            {
                "description": "my_description",
                "id": "found_id",
                "released_year": 2020,
                "title": "my_title",
                "watched": False,
            },
            id="movie found",
        ),
    ],
)
@pytest.mark.asyncio()
async def test_getmovie_by_id(
    test_client, movie_seed, movie_id, expected_status_code, expected_result
):
    # Setup Phase
    repo = MemoryMovieRepository()
    partial_dependency = functools.partial(memory_repository_dependency, repo)

    test_client.app.dependency_overrides[movie_repository] = partial_dependency

    for movie in movie_seed:
        await repo.create(movie)

    # Test Phase
    result = test_client.get(f"/api/v1/movies/{movie_id}")

    # Assertion Phase
    assert result.status_code == expected_status_code
    assert result.json() == expected_result


@pytest.mark.parametrize(
    "movie_seed, movie_title, skip, limit, expected_result",
    [
        pytest.param([], "test_title", 0, 1000, [], id="empty results"),
        pytest.param(
            [
                Movie(
                    movie_id="my_id",
                    title="test_title",
                    description="my_description",
                    released_year=2020,
                    watched=False,
                ),
                Movie(
                    movie_id="my_id_2",
                    title="my_title",
                    description="my_description",
                    released_year=2021,
                    watched=False,
                ),
                Movie(
                    movie_id="my_id_3",
                    title="test_title",
                    description="my_description",
                    released_year=2022,
                    watched=False,
                ),
                Movie(
                    movie_id="my_id_5",
                    title="some_title",
                    description="my_description",
                    released_year=2019,
                    watched=False,
                ),
            ],
            "test_title",
            0,
            1000,
            [
                {
                    "description": "my_description",
                    "id": "my_id",
                    "released_year": 2020,
                    "title": "test_title",
                    "watched": False,
                },
                {
                    "description": "my_description",
                    "id": "my_id_3",
                    "released_year": 2022,
                    "title": "test_title",
                    "watched": False,
                },
            ],
            id="some results",
        ),
        pytest.param(
            [
                Movie(
                    movie_id="my_id",
                    title="test_title",
                    description="my_description",
                    released_year=2020,
                    watched=False,
                ),
                Movie(
                    movie_id="my_id_2",
                    title="my_title",
                    description="my_description",
                    released_year=2021,
                    watched=False,
                ),
                Movie(
                    movie_id="my_id_3",
                    title="test_title",
                    description="my_description",
                    released_year=2022,
                    watched=False,
                ),
                Movie(
                    movie_id="my_id_5",
                    title="test_title",
                    description="my_description",
                    released_year=2019,
                    watched=True,
                ),
            ],
            "test_title",
            1,
            1000,
            [
                {
                    "description": "my_description",
                    "id": "my_id_3",
                    "released_year": 2022,
                    "title": "test_title",
                    "watched": False,
                },
                {
                    "description": "my_description",
                    "id": "my_id_5",
                    "released_year": 2019,
                    "title": "test_title",
                    "watched": True,
                },
            ],
            id="paginated results",
        ),
    ],
)
@pytest.mark.asyncio()
async def test_getmovie_by_title(
    test_client, movie_seed, movie_title, skip, limit, expected_result
):
    # Setup Phase
    repo = MemoryMovieRepository()
    partial_dependency = functools.partial(memory_repository_dependency, repo)

    test_client.app.dependency_overrides[movie_repository] = partial_dependency

    for movie in movie_seed:
        await repo.create(movie)

    # Test Phase
    result = test_client.get(
        f"/api/v1/movies/?title={movie_title}&skip={skip}&limit={limit}"
    )

    # Assertion Phase
    assert result.status_code == 200
    assert result.json() == expected_result


@pytest.mark.parametrize(
    "movie_seed, movie_id, update_parameters, expected_status_code, expected_result",
    [
        pytest.param(
            [],
            "test_id",
            {"title": "new_title"},
            404,
            {"message": "Movie with id test_id not found"},
            id="movie not found",
        ),
        pytest.param(
            [
                Movie(
                    movie_id="test_id",
                    title="test_title",
                    description="my_description",
                    released_year=2020,
                    watched=False,
                )
            ],
            "test_id",
            {"title": "new_title"},
            200,
            {"message": "Movie with id test_id updated"},
            id="updated title successfully",
        ),
    ],
)
@pytest.mark.asyncio()
async def test_update_movie(
    test_client,
    movie_seed,
    movie_id,
    update_parameters,
    expected_status_code,
    expected_result,
):
    # Setup Phase
    repo = MemoryMovieRepository()
    partial_dependency = functools.partial(memory_repository_dependency, repo)

    test_client.app.dependency_overrides[movie_repository] = partial_dependency

    for movie in movie_seed:
        await repo.create(movie)

    # Test Phase
    result = test_client.patch(f"/api/v1/movies/{movie_id}", json=update_parameters)

    # Assertion Phase
    assert result.status_code == expected_status_code
    assert result.json() == expected_result


@pytest.mark.asyncio()
async def test_delete_movie(test_client):
    # Setup Phase
    repo = MemoryMovieRepository()
    partial_dependency = functools.partial(memory_repository_dependency, repo)

    test_client.app.dependency_overrides[movie_repository] = partial_dependency

    await repo.create(
        Movie(
            movie_id="test_id",
            title="test_title",
            description="my_description",
            released_year=2020,
            watched=False,
        )
    )

    # Test Phase
    result = test_client.delete("/api/v1/movies/test_id")

    # Assertion Phase
    assert result.status_code == 204
    assert await repo.get_by_id("test_id") is None
