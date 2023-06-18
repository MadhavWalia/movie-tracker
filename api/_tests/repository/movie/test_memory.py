import pytest

from api._tests.fixture import memory_movie_repo_fixture
from api.entities.movie import Movie
from api.repository.movie.abstractions import RepositoryException
from api.repository.movie.memory import MemoryMovieRepository


@pytest.mark.asyncio
async def test_create(memory_movie_repo_fixture):
    movie = Movie(movie_id="test", title="test", description="test", released_year=2020)
    await memory_movie_repo_fixture.create(movie)
    assert await memory_movie_repo_fixture.get_by_id("test") is not None


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
            id="Found",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_id(
    memory_movie_repo_fixture, movies_seed, movie_id, expected_result
):
    for movie in movies_seed:
        await memory_movie_repo_fixture.create(movie)
    movie = await memory_movie_repo_fixture.get_by_id(movie_id=movie_id)
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
async def test_get_by_title(
    memory_movie_repo_fixture, movies_seed, movie_title, expected_results
):
    for movie in movies_seed:
        await memory_movie_repo_fixture.create(movie)
    result = await memory_movie_repo_fixture.get_by_title(title=movie_title)
    assert result == expected_results


@pytest.mark.parametrize(
    "skip, limit, expected_results",
    [
        pytest.param(
            0,
            0,
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
                    released_year=2021,
                    watched=False,
                ),
                Movie(
                    movie_id="my_id_3",
                    title="my_title",
                    description="my_description",
                    released_year=2022,
                    watched=False,
                ),
            ],
            id="empty_result",
        ),
        pytest.param(
            0,
            1,
            [
                Movie(
                    movie_id="my_id",
                    title="my_title",
                    description="my_description",
                    released_year=2020,
                    watched=False,
                )
            ],
            id="first_page",
        ),
        pytest.param(
            1,
            1,
            [
                Movie(
                    movie_id="my_id_2",
                    title="my_title",
                    description="my_description",
                    released_year=2021,
                    watched=False,
                )
            ],
            id="second_page",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_title_pagination(
    memory_movie_repo_fixture, skip, limit, expected_results
):
    movies_seed = [
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
            released_year=2021,
            watched=False,
        ),
        Movie(
            movie_id="my_id_3",
            title="my_title",
            description="my_description",
            released_year=2022,
            watched=False,
        ),
    ]

    for movie in movies_seed:
        await memory_movie_repo_fixture.create(movie)
    result = await memory_movie_repo_fixture.get_by_title(
        title="my_title", skip=skip, limit=limit
    )
    assert result == expected_results


@pytest.mark.asyncio
async def test_delete(memory_movie_repo_fixture):
    await memory_movie_repo_fixture.create(
        Movie(
            movie_id="my_id",
            title="my_title",
            description="my_description",
            released_year=2020,
            watched=False,
        )
    )
    await memory_movie_repo_fixture.delete(movie_id="my_id")
    assert await memory_movie_repo_fixture.get_by_id(movie_id="my_id") is None


@pytest.mark.asyncio
async def test_update(memory_movie_repo_fixture):
    await memory_movie_repo_fixture.create(
        Movie(
            movie_id="my_id",
            title="my_title",
            description="my_description",
            released_year=2020,
            watched=False,
        )
    )
    await memory_movie_repo_fixture.update(
        movie_id="my_id",
        update_parameters={
            "title": "new_title",
            "description": "new_description",
            "released_year": 2021,
            "watched": True,
        },
    )
    assert await memory_movie_repo_fixture.get_by_id(movie_id="my_id") == Movie(
        movie_id="my_id",
        title="new_title",
        description="new_description",
        released_year=2021,
        watched=True,
    )


@pytest.mark.asyncio
async def test_update_fail(memory_movie_repo_fixture):
    await memory_movie_repo_fixture.create(
        Movie(
            movie_id="my_id",
            title="my_title",
            description="my_description",
            released_year=2020,
            watched=False,
        )
    )
    with pytest.raises(RepositoryException):
        await memory_movie_repo_fixture.update(
            movie_id="my_id", update_parameters={"id": "new_id"}
        )
