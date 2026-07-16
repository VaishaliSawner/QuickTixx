from src.exception.custom_exception import BookingNotFoundException,MovieNotFoundException

from src.model.booking import Booking
from src.repository.booking_repo import BookingRepository
from src.repository.movie_repo import MovieRepository


class BookingService:

    def __init__(self, session):
        self.booking_repo = BookingRepository(session)
        self.movie_repo = MovieRepository(session)

    async def book_ticket(self, booking: Booking):

        movie = await self.movie_repo.get_movie_by_id(booking.movie_id)

        if not movie:
            raise MovieNotFoundException()

        if booking.quantity > movie.available_seats:
            raise Exception("Seats are not available.")

        movie.available_seats -= booking.quantity

        await self.movie_repo.update_movie(movie)

        return await self.booking_repo.create_booking(booking)

    async def get_booking_by_id(self, booking_id: int):

        booking = await self.booking_repo.get_booking_by_id(booking_id)

        if not booking:
            raise BookingNotFoundException()
        return booking

    async def get_my_bookings(self, user_id: int):
        return await self.booking_repo.get_bookings_by_user(user_id)

    async def cancel_booking(self, booking_id: int):
        booking = await self.booking_repo.get_booking_by_id(booking_id)

        if not booking:
            raise BookingNotFoundException()

        movie = await self.movie_repo.get_movie_by_id(booking.movie_id)

        if movie:
            movie.available_seats += booking.quantity
            await self.movie_repo.update_movie(movie)
        await self.booking_repo.delete_booking(booking)