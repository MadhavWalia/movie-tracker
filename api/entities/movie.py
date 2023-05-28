class Movie:
    def __init__(
        self,
        *,
        movie_id: str,
        title: str,
        description: str,
        released_year: int,
        watched: bool = False
    ):
        if movie_id is None:
            raise ValueError("id is required")

        self._id = movie_id
        self._title = title
        self._description = description
        self._released_year = released_year
        self._watched = watched

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def released_year(self) -> int:
        return self._released_year

    @property
    def watched(self) -> bool:
        return self._watched

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Movie):
            return False
        else:
            return (
                self.id == o.id
                and self.title == o.title
                and self.description == o.description
                and self.released_year == o.released_year
                and self.watched == o.watched
            )
