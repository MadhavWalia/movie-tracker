import pytest
from api._tests.fixture import mongo_movie_repo_fixture
from api.entities.movie import Movie
from api.repository.movie.abstractions import RepositoryException

from api.repository.movie.mongo import MongoMovieRepository


@pytest.mark.asyncio
async def test_create(mongo_movie_repo_fixture):
    await mongo_movie_repo_fixture.create(
        movie=Movie(
            movie_id="test",
            title="test",
            description="test",
            released_year=2020,
            watched=False,
        )
    )
    movie: Movie = await mongo_movie_repo_fixture.get_by_id(movie_id="test")
    assert movie == Movie(
        movie_id="test",
        title="test",
        description="test",
        released_year=2020,
        watched=False,
    )


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
async def test_get_by_id(
    mongo_movie_repo_fixture, movies_seed, movie_id, expected_result
):
    for movie in movies_seed:
        await mongo_movie_repo_fixture.create(movie)

    movie: Movie = await mongo_movie_repo_fixture.get_by_id(movie_id=movie_id)
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
    mongo_movie_repo_fixture, movies_seed, movie_title, expected_results
):
    for movie in movies_seed:
        await mongo_movie_repo_fixture.create(movie)

    movie: Movie = await mongo_movie_repo_fixture.get_by_title(title=movie_title)
    assert movie == expected_results


@pytest.mark.asyncio
async def test_delete(mongo_movie_repo_fixture):
    await mongo_movie_repo_fixture.create(
        Movie(
            movie_id="my_id",
            title="my_title",
            description="my_description",
            released_year=2020,
            watched=False,
        )
    )
    await mongo_movie_repo_fixture.delete(movie_id="my_id")
    assert await mongo_movie_repo_fixture.get_by_id(movie_id="my_id") is None


@pytest.mark.asyncio
async def test_update(mongo_movie_repo_fixture):
    await mongo_movie_repo_fixture.create(
        Movie(
            movie_id="my_id",
            title="my_title",
            description="my_description",
            released_year=2020,
            watched=False,
        )
    )
    await mongo_movie_repo_fixture.update(
        movie_id="my_id",
        update_parameters={
            "title": "new_title",
            "description": "new_description",
            "released_year": 2021,
            "watched": True,
        },
    )
    assert await mongo_movie_repo_fixture.get_by_id(movie_id="my_id") == Movie(
        movie_id="my_id",
        title="new_title",
        description="new_description",
        released_year=2021,
        watched=True,
    )


@pytest.mark.asyncio
async def test_update_fail(mongo_movie_repo_fixture):
    await mongo_movie_repo_fixture.create(
        Movie(
            movie_id="my_id",
            title="my_title",
            description="my_description",
            released_year=2020,
            watched=False,
        )
    )
    with pytest.raises(RepositoryException):
        await mongo_movie_repo_fixture.update(
            movie_id="my_id", update_parameters={"id": "new_id"}
        )
