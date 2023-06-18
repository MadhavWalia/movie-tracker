class User:
    def __init__(
        self,
        *,
        username: str,
        password: str,
    ):
        if username or password is None:
            raise ValueError("values is required")

        self._username = username
        self._password = password

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    def __repr__(self):
        return f"User(username='{self._username})"