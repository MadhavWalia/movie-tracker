import pytest

from api._tests.fixture import mongo_user_repo_fixture
from api.entities.user import User
from api.repository.user.abstractions import RepositoryException
from api.repository.user.mongo import MongoUserRepository


@pytest.mark.asyncio
async def test_create(mongo_user_repo_fixture):
    await mongo_user_repo_fixture.create(
        user=User(user_id="test_id", username="test", password="test123")
    )

    user: User = await mongo_user_repo_fixture.get_user(username="test")
    assert user == User(user_id="test_id", username="test", password="test123")


@pytest.mark.asyncio
async def test_create_fail(mongo_user_repo_fixture):
    await mongo_user_repo_fixture.create(
        user=User(user_id="test_id", username="test", password="test123")
    )

    user_duplicate = User(user_id="test_id", username="test", password="#test123")
    with pytest.raises(RepositoryException):
        await mongo_user_repo_fixture.create(user_duplicate)


@pytest.mark.parametrize(
    "users_seed, username, expected_result",
    [
        pytest.param([], "my_username", None, id="empty"),
        pytest.param(
            [
                User(
                    user_id="test_id",
                    username="my_username",
                    password="my_password",
                )
            ],
            "my_username",
            User(
                user_id="test_id",
                username="my_username",
                password="my_password",
            ),
            id="Found",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_user(mongo_user_repo_fixture, users_seed, username, expected_result):
    for user in users_seed:
        await mongo_user_repo_fixture.create(user)

    user = await mongo_user_repo_fixture.get_user(username=username)
    assert user == expected_result


@pytest.mark.parametrize(
    "users_seed, user, expected_result",
    [
        pytest.param(
            [User(user_id="test_id", username="my_username", password="my_password")],
            User(user_id="test_id", username="my_username", password="my_password"),
            True,
            id="Valid",
        ),
    ],
)
@pytest.mark.asyncio
async def test_verify_account(
    mongo_user_repo_fixture, users_seed, user, expected_result
):
    for users in users_seed:
        await mongo_user_repo_fixture.create(users)

    result = await mongo_user_repo_fixture.verify_account(user=user)
    assert result == expected_result


@pytest.mark.parametrize(
    "users_seed, user, expected_result",
    [
        pytest.param(
            [],
            User(user_id="test_id", username="my_username", password="my_password"),
            False,
            id="Not_Found",
        ),
        pytest.param(
            [User(user_id="test_id", username="my_username", password="my_password")],
            User(user_id="test_id", username="my_username", password="not_my_password"),
            True,
            id="InValid",
        ),
    ],
)
@pytest.mark.asyncio
async def test_verify_account_fail(
    mongo_user_repo_fixture, users_seed, user, expected_result
):
    for users in users_seed:
        await mongo_user_repo_fixture.create(users)

    with pytest.raises(RepositoryException):
        result = await mongo_user_repo_fixture.verify_account(user)


@pytest.mark.asyncio
async def test_delete(mongo_user_repo_fixture):
    await mongo_user_repo_fixture.create(
        User(user_id="test_id", username="my_username", password="my_password")
    )
    await mongo_user_repo_fixture.delete(username="my_username")
    assert await mongo_user_repo_fixture.get_user(username="my_username") is None


@pytest.mark.asyncio
async def test_update(mongo_user_repo_fixture):
    await mongo_user_repo_fixture.create(
        User(user_id="test_id", username="my_username", password="my_password")
    )

    await mongo_user_repo_fixture.update(
        user=User(user_id="test_id", username="my_username", password="my_password"),
        update_parameters={
            "username": "new_username",
            "password": "new_password",
        },
    )

    updated_user = User(
        user_id="test_id", username="new_username", password="new_password"
    )
    assert await mongo_user_repo_fixture.verify_account(updated_user) is True


@pytest.mark.parametrize(
    "users_seed, user, update_parameters",
    [
        pytest.param(
            [User(user_id="test_id", username="my_username", password="my_password")],
            User(user_id="test_id", username="my_username", password="my_password"),
            {"username": "my_username", "password": "my_password"},
            id="Same_Password",
        )
    ],
)
@pytest.mark.asyncio
async def test_update_fail(
    mongo_user_repo_fixture, users_seed, user, update_parameters
):
    for users in users_seed:
        await mongo_user_repo_fixture.create(users)

    with pytest.raises(RepositoryException):
        await mongo_user_repo_fixture.update(
            user=user,
            update_parameters=update_parameters,
        )
