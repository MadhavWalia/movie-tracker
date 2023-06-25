import pytest

from api._tests.fixture import memory_auth_repo_fixture
from api.entities.auth import AuthUser
from api.repository.auth.abstractions import RepositoryException
from api.repository.auth.memory import MemoryAuthRepository


@pytest.mark.asyncio
async def test_create(memory_auth_repo_fixture):
    authuser = AuthUser(user_id="test_id", username="test", password="test123")
    await memory_auth_repo_fixture.create(authuser)
    assert await memory_auth_repo_fixture.get_user("test") is not None


@pytest.mark.asyncio
async def test_create_fail(memory_auth_repo_fixture):
    authuser = AuthUser(user_id="test_id", username="test", password="test123")
    await memory_auth_repo_fixture.create(authuser)

    authuser_duplicate = AuthUser(
        user_id="test_id", username="test", password="#test123"
    )
    with pytest.raises(RepositoryException):
        await memory_auth_repo_fixture.create(authuser_duplicate)


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
    memory_auth_repo_fixture, authusers_seed, username, expected_result
):
    for authuser in authusers_seed:
        await memory_auth_repo_fixture.create(authuser)
    authuser = await memory_auth_repo_fixture.get_user(username=username)
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
    memory_auth_repo_fixture, authusers_seed, username, password, expected_result
):
    for authusers in authusers_seed:
        await memory_auth_repo_fixture.create(authusers)

    result = await memory_auth_repo_fixture.verify_account(
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
    memory_auth_repo_fixture, authusers_seed, username, password, expected_result
):
    for authusers in authusers_seed:
        await memory_auth_repo_fixture.create(authusers)

    with pytest.raises(RepositoryException):
        result = await memory_auth_repo_fixture.verify_account(
            username=username, password=password
        )


@pytest.mark.asyncio
async def test_delete(memory_auth_repo_fixture):
    await memory_auth_repo_fixture.create(
        AuthUser(user_id="test_id", username="my_username", password="my_password")
    )
    await memory_auth_repo_fixture.delete(username="my_username")
    assert await memory_auth_repo_fixture.get_user(username="my_username") is None


@pytest.mark.asyncio
async def test_update(memory_auth_repo_fixture):
    await memory_auth_repo_fixture.create(
        AuthUser(user_id="test_id", username="my_username", password="my_password")
    )

    await memory_auth_repo_fixture.update(
        authuser=AuthUser(
            user_id="test_id", username="my_username", password="my_password"
        ),
        update_parameters={
            "username": "new_username",
            "password": "new_password",
        },
    )

    assert (
        await memory_auth_repo_fixture.verify_account(
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
    memory_auth_repo_fixture, authusers_seed, authuser, update_parameters
):
    for authusers in authusers_seed:
        await memory_auth_repo_fixture.create(authusers)

    with pytest.raises(RepositoryException):
        await memory_auth_repo_fixture.update(
            authuser=authuser,
            update_parameters=update_parameters,
        )
