import pytest

from api._tests.fixture import memory_user_repo_fixture
from api.entities.user import User
from api.repository.user.abstractions import RepositoryException
from api.repository.user.memory import MemoryUserRepository


@pytest.mark.asyncio
async def test_create(memory_user_repo_fixture):
    user = User(username="test", password="test123")
    await memory_user_repo_fixture.create(user)
    assert await memory_user_repo_fixture.get_user("test") is not None


@pytest.mark.asyncio
async def test_create_fail(memory_user_repo_fixture):
    user = User(username="test", password="test123")
    await memory_user_repo_fixture.create(user)

    user_duplicate = User(username="test", password="#test123")
    with pytest.raises(RepositoryException):
        await memory_user_repo_fixture.create(user_duplicate)


@pytest.mark.parametrize(
    "users_seed, username, expected_result",
    [
        pytest.param([], "my_username", None, id="empty"),
        pytest.param(
            [
                User(
                    username="my_username",
                    password="my_password",
                )
            ],
            "my_username",
            User(
                username="my_username",
                password="my_password",
            ),
            id="Found",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_user(
    memory_user_repo_fixture, users_seed, username, expected_result
):
    for user in users_seed:
        await memory_user_repo_fixture.create(user)
    user = await memory_user_repo_fixture.get_user(username=username)
    assert user == expected_result


@pytest.mark.parametrize(
    "users_seed, user, expected_result",
    [
        pytest.param(
            [User(username="my_username", password="my_password")],
            User(username="my_username", password="my_password"),
            True,
            id="Valid",
        ),
    ],
)
@pytest.mark.asyncio
async def test_verify_account(
    memory_user_repo_fixture, users_seed, user, expected_result
):
    for users in users_seed:
        await memory_user_repo_fixture.create(users)

    result = await memory_user_repo_fixture.verify_account(user)
    assert result == expected_result


@pytest.mark.parametrize(
    "users_seed, user, expected_result",
    [
        pytest.param(
            [],
            User(username="my_username", password="my_password"),
            False,
            id="Not_Found",
        ),
        pytest.param(
            [User(username="my_username", password="my_password")],
            User(username="my_username", password="not_my_password"),
            True,
            id="InValid",
        ),
    ],
)
@pytest.mark.asyncio
async def test_verify_account_fail(
    memory_user_repo_fixture, users_seed, user, expected_result
):
    for users in users_seed:
        await memory_user_repo_fixture.create(users)

    with pytest.raises(RepositoryException):
        result = await memory_user_repo_fixture.verify_account(user)


@pytest.mark.asyncio
async def test_delete(memory_user_repo_fixture):
    await memory_user_repo_fixture.create(
        User(username="my_username", password="my_password")
    )
    await memory_user_repo_fixture.delete(username="my_username")
    assert await memory_user_repo_fixture.get_user(username="my_username") is None


@pytest.mark.asyncio
async def test_update(memory_user_repo_fixture):
    await memory_user_repo_fixture.create(
        User(username="my_username", password="my_password")
    )
    await memory_user_repo_fixture.update(
        user=User(username="my_username", password="my_password"),
        update_parameters={
            "username": "new_username",
            "password": "new_password",
        },
    )
    updated_user = User(username="new_username", password="new_password")
    print(memory_user_repo_fixture._storage)
    assert await memory_user_repo_fixture.verify_account(updated_user) is True


@pytest.mark.parametrize(
    "users_seed, user, update_parameters",
    [
        pytest.param(
            [User(username="my_username", password="my_password")],
            User(username="my_username", password="my_password"),
            {"username": "my_username", "password": "my_password"},
            id="Same_Password",
        )
    ],
)
@pytest.mark.asyncio
async def test_update_fail(
    memory_user_repo_fixture, users_seed, user, update_parameters
):
    for users in users_seed:
        await memory_user_repo_fixture.create(users)

    with pytest.raises(RepositoryException):
        await memory_user_repo_fixture.update(
            user=user,
            update_parameters=update_parameters,
        )
