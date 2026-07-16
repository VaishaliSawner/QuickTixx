
from src.exception.custom_exception import MovieNotFoundException
from src.model.movie import Movie
from src.repository.movie_repo import MovieRepository


class MovieService:
    def __init__(self,session):
        self.movie_repo = MovieRepository(session)

    async def create_movie(self,movie:Movie):
        return await self.movie_repo.create_movie(movie)

    async def get_movie_by_id(self, movie_id: int):
        movie = await self.movie_repo.get_movie_by_id(movie_id)

        if not movie:
            raise MovieNotFoundException()
        return movie

    async def get_all_movies(self):
        return await self.movie_repo.get_all_movies()

    async def update_movie(self, movie: Movie, db_movie: Movie):

        if not db_movie:
            raise MovieNotFoundException()
        db_movie.movie_name = movie.movie_name
        db_movie.language = movie.language
        db_movie.genre = movie.genre
        db_movie.duration = movie.duration
        db_movie.price = movie.price
        db_movie.available_seats = movie.available_seats
        db_movie.description = movie.description
        db_movie.image = movie.image
        return await self.movie_repo.update_movie(db_movie)

    async def delete_movie(self, movie_id: int):
        movie = await self.movie_repo.get_movie_by_id(movie_id)
        if not movie:
            raise MovieNotFoundException()
        await self.movie_repo.delete_movie(movie)