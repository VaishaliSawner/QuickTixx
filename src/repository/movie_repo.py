from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.model.movie import Movie


class MovieRepository:
    def __init__(self,session:AsyncSession):
        self.session = session

    async def create_movie(self,movie:Movie):
        self.session.add(movie)
        await self.session.flush()
        await self.session.refresh(movie)
        return movie

    async def get_movie_by_id(self, movie_id: int):
        query = select(Movie).where(Movie.id == movie_id)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_all_movies(self):
        query = select(Movie)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_movie(self, movie: Movie):
        await self.session.flush()
        await self.session.refresh(movie)
        return movie

    async def delete_movie(self, movie: Movie):
        await self.session.delete(movie)
        await self.session.flush()