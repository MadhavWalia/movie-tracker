from passlib.context import CryptContext


class AuthUser:
    def __init__(
        self,
        *,
        user_id: str,
        username: str,
        password: str,
    ):
        if user_id is None:
            raise ValueError("user_id is required")
        if username is None:
            raise ValueError("username is required")
        if password is None:
            raise ValueError("password is required")

        self._user_id = user_id
        self._username = username
        self._password = password

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    def __repr__(self):
        return f"AuthUser(user_id = '{self._user_id}', username='{self._username}')"

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, AuthUser):
            return False
        else:
            pwd_context = CryptContext(schemes=["bcrypt"])
            return (
                self.user_id == o.user_id
                and self.username == o.username
                and pwd_context.verify(o.password, self.password)
            )
