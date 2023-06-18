from passlib.context import CryptContext


class User:
    def __init__(
        self,
        *,
        username: str,
        password: str,
    ):
        if username is None:
            raise ValueError("username is required")
        if password is None:
            raise ValueError("password is required")

        self._username = username
        self._password = password

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    def __repr__(self):
        return f"User(username='{self._username}, password='{self._password}')"

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, User):
            return False
        else:
            pwd_context = CryptContext(schemes=["bcrypt"])
            return self.username == o.username and pwd_context.verify(
                o.password, self.password
            )
