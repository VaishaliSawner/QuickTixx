from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.model.booking import Booking


class BookingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_booking(self, booking: Booking):
        self.session.add(booking)
        await self.session.flush()
        await self.session.refresh(booking)
        return booking

    async def get_booking_by_id(self, booking_id: int):
        query = select(Booking).where(Booking.id == booking_id)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_all_bookings(self):
        query = select(Booking)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_bookings_by_user(self, user_id: int):
        query = (
            select(Booking)
            .where(Booking.user_id == user_id)
            .options(selectinload(Booking.movie))
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def delete_booking(self, booking: Booking):
        await self.session.delete(booking)
        await self.session.flush()


















'''
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.booking import Booking


class BookingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_booking(self, booking: Booking):
        self.session.add(booking)
        await self.session.flush()
        await self.session.refresh(booking)
        return booking

    async def get_booking_by_id(self, booking_id: int):
        query = select(Booking).where(Booking.id == booking_id)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_all_bookings(self):
        query = select(Booking)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_bookings_by_user(self, user_id: int):
        query = select(Booking).where(Booking.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def delete_booking(self, booking: Booking):
        await self.session.delete(booking)
        await self.session.flush()

'''