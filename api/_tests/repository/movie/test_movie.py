import pytest

from api.entities.movie import Movie
from api.repository.movie.abstractions import RepositoryException
from api.repository.movie.movie import MemoryMovieRepository


@pytest.mark.asyncio
async def test_create():
    repo = MemoryMovieRepository()
    movie = Movie(movie_id="test", title="test", description="test", released_year=2020)
    await repo.create(movie)
    assert await repo.get_by_id("test") is not None


@pytest.mark.parametrize(
    "movies_seed, movie_id, expected_result",
    [
        pytest.param([], "my_id", None, id="empty"),
        pytest.param(
            [
                Movie(
                    movie_id="my_id",
                    title="my_title",
                    description="my_description",
                    released_year=2020,
                    watched=False,
                )
            ],
            "my_id",
            Movie(
                movie_id="my_id",
                title="my_title",
                description="my_description",
                released_year=2020,
                watched=False,
            ),
            id="empty",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_id(movies_seed, movie_id, expected_result):
    repo = MemoryMovieRepository()
    for movie in movies_seed:
        await repo.create(movie)
    movie = await repo.get_by_id(movie_id=movie_id)
    assert movie == expected_result


@pytest.mark.parametrize(
    "movies_seed, movie_title, expected_results",
    [
        pytest.param([], "my_title", [], id="empty_result"),
        pytest.param(
            [
                Movie(
                    movie_id="my_id",
                    title="my_title",
                    description="my_description",
                    released_year=2020,
                    watched=False,
                )
            ],
            "some_title",
            [],
            id="empty_result_2",
        ),
        pytest.param(
            [
                Movie(
                    movie_id="my_id",
                    title="my_title",
                    description="my_description",
                    released_year=2020,
                    watched=False,
                ),
                Movie(
                    movie_id="my_id_2",
                    title="my_title",
                    description="my_description",
                    released_year=2020,
                    watched=False,
                ),
            ],
            "my_title",
            [
                Movie(
                    movie_id="my_id",
                    title="my_title",
                    description="my_description",
                    released_year=2020,
                    watched=False,
                ),
                Movie(
                    movie_id="my_id_2",
                    title="my_title",
                    description="my_description",
                    released_year=2020,
                    watched=False,
                ),
            ],
            id="results",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_title(movies_seed, movie_title, expected_results):
    repo = MemoryMovieRepository()
    for movie in movies_seed:
        await repo.create(movie)
    result = await repo.get_by_title(title=movie_title)
    assert result == expected_results


@pytest.mark.asyncio
async def test_delete():
    repo = MemoryMovieRepository()
    await repo.create(
        Movie(
            movie_id="my_id",
            title="my_title",
            description="my_description",
            released_year=2020,
            watched=False,
        )
    )
    await repo.delete(movie_id="my_id")
    assert await repo.get_by_id(movie_id="my_id") is None


@pytest.mark.asyncio
async def test_update():
    repo = MemoryMovieRepository()
    await repo.create(
        Movie(
            movie_id="my_id",
            title="my_title",
            description="my_description",
            released_year=2020,
            watched=False,
        )
    )
    await repo.update(
        movie_id="my_id",
        update_parameters={
            "title": "new_title",
            "description": "new_description",
            "released_year": 2021,
            "watched": True,
        },
    )
    assert await repo.get_by_id(movie_id="my_id") == Movie(
        movie_id="my_id",
        title="new_title",
        description="new_description",
        released_year=2021,
        watched=True,
    )


@pytest.mark.asyncio
async def test_update_fail():
    repo = MemoryMovieRepository()
    await repo.create(
        Movie(
            movie_id="my_id",
            title="my_title",
            description="my_description",
            released_year=2020,
            watched=False,
        )
    )
    with pytest.raises(RepositoryException):
        await repo.update(movie_id="my_id", update_parameters={"id": "new_id"})
