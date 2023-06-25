import pytest

from api._tests.fixture import mongo_auth_repo_fixture
from api.entities.auth import AuthUser
from api.repository.auth.abstractions import RepositoryException
from api.repository.auth.mongo import MongoAuthRepository


@pytest.mark.asyncio
async def test_create(mongo_auth_repo_fixture):
    await mongo_auth_repo_fixture.create(
        authuser=AuthUser(user_id="test_id", username="test", password="test123")
    )

    authuser: AuthUser = await mongo_auth_repo_fixture.get_user(username="test")
    assert authuser == AuthUser(user_id="test_id", username="test", password="test123")


@pytest.mark.asyncio
async def test_create_fail(mongo_auth_repo_fixture):
    await mongo_auth_repo_fixture.create(
        authuser=AuthUser(user_id="test_id", username="test", password="test123")
    )

    authuser_duplicate = AuthUser(
        user_id="test_id", username="test", password="#test123"
    )
    with pytest.raises(RepositoryException):
        await mongo_auth_repo_fixture.create(authuser_duplicate)


@pytest.mark.parametrize(
    "authusers_seed, username, expected_result",
    [
        pytest.param([], "my_username", None, id="empty"),
        pytest.param(
            [
                AuthUser(
                    user_id="test_id",
                    username="my_username",
                    password="my_password",
                )
            ],
            "my_username",
            AuthUser(
                user_id="test_id",
                username="my_username",
                password="my_password",
            ),
            id="Found",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_user(
    mongo_auth_repo_fixture, authusers_seed, username, expected_result
):
    for authuser in authusers_seed:
        await mongo_auth_repo_fixture.create(authuser)

    authuser = await mongo_auth_repo_fixture.get_user(username=username)
    assert authuser == expected_result


@pytest.mark.parametrize(
    "authusers_seed, username, password, expected_result",
    [
        pytest.param(
            [
                AuthUser(
                    user_id="test_id", username="my_username", password="my_password"
                )
            ],
            "my_username",
            "my_password",
            True,
            id="Valid",
        ),
    ],
)
@pytest.mark.asyncio
async def test_verify_account(
    mongo_auth_repo_fixture, authusers_seed, username, password, expected_result
):
    for authusers in authusers_seed:
        await mongo_auth_repo_fixture.create(authusers)

    result = await mongo_auth_repo_fixture.verify_account(
        username=username, password=password
    )
    assert result == expected_result


@pytest.mark.parametrize(
    "authusers_seed, username, password, expected_result",
    [
        pytest.param(
            [],
            "my_username",
            "my_password",
            False,
            id="Not_Found",
        ),
        pytest.param(
            [
                AuthUser(
                    user_id="test_id", username="my_username", password="my_password"
                )
            ],
            "my_username",
            "not_my_password",
            True,
            id="InValid",
        ),
    ],
)
@pytest.mark.asyncio
async def test_verify_account_fail(
    mongo_auth_repo_fixture, authusers_seed, username, password, expected_result
):
    for authusers in authusers_seed:
        await mongo_auth_repo_fixture.create(authusers)

    with pytest.raises(RepositoryException):
        result = await mongo_auth_repo_fixture.verify_account(
            username=username, password=password
        )


@pytest.mark.asyncio
async def test_delete(mongo_auth_repo_fixture):
    await mongo_auth_repo_fixture.create(
        AuthUser(user_id="test_id", username="my_username", password="my_password")
    )
    await mongo_auth_repo_fixture.delete(username="my_username")
    assert await mongo_auth_repo_fixture.get_user(username="my_username") is None


@pytest.mark.asyncio
async def test_update(mongo_auth_repo_fixture):
    await mongo_auth_repo_fixture.create(
        AuthUser(user_id="test_id", username="my_username", password="my_password")
    )

    await mongo_auth_repo_fixture.update(
        authuser=AuthUser(
            user_id="test_id", username="my_username", password="my_password"
        ),
        update_parameters={
            "username": "new_username",
            "password": "new_password",
        },
    )

    assert (
        await mongo_auth_repo_fixture.verify_account(
            username="new_username", password="new_password"
        )
        is True
    )


@pytest.mark.parametrize(
    "authusers_seed, authuser, update_parameters",
    [
        pytest.param(
            [
                AuthUser(
                    user_id="test_id", username="my_username", password="my_password"
                )
            ],
            AuthUser(user_id="test_id", username="my_username", password="my_password"),
            {"username": "my_username", "password": "my_password"},
            id="Same_Password",
        )
    ],
)
@pytest.mark.asyncio
async def test_update_fail(
    mongo_auth_repo_fixture, authusers_seed, authuser, update_parameters
):
    for authusers in authusers_seed:
        await mongo_auth_repo_fixture.create(authusers)

    with pytest.raises(RepositoryException):
        await mongo_auth_repo_fixture.update(
            authuser=authuser,
            update_parameters=update_parameters,
        )
