
from typing import List, Optional
from api.entities.movie import Movie
from api.repository.movie.abstractions import MovieRepository, RepositoryException


class MemoryMovieRepository(MovieRepository):
    
    def __init__(self):
        self._storage = {}

    def create(self, movie: Movie):
        self._storage[movie.id] = movie

    def get_by_id(self, movie_id: str) -> Optional[Movie]:
        return self._storage.get(movie_id)

    def get_by_title(self, title: str) -> List[Movie]:
        return [movie for _, movie in self._storage.values() if movie.title == title]

    def delete(self, movie_id: str):
        self._storage.pop(movie_id, None)

    def update(self, movie_id: str, update_parameters: dict):
        movie = self._storage.get(movie_id)
        if movie is None:
            raise RepositoryException(f"Movie with id {movie_id} not found")
        
        for key, value in update_parameters.items():
          if key == "id":
              raise RepositoryException("Cannot update movie id")

          #Check that update parameters are fields from Movie Entity
          if hasattr(movie, key):
            setattr(movie, key, value)