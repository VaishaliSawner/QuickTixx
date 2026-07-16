from datetime import datetime

from sqlalchemy import DateTime,ForeignKey,Integer
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy.sql import func
from src.db_config.database import Base

class Booking(Base):
    __tablename__ = "booking"
    id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("user.id"),nullable=False)
    movie_id:Mapped[int]=mapped_column(ForeignKey("movie.id"),nullable=False)
    quantity:Mapped[int]=mapped_column(Integer,nullable=False)
    booking_date:Mapped[datetime]=mapped_column(DateTime,server_default=func.now())

    user=relationship("User",back_populates="bookings")
    movie=relationship("Movie",back_populates="bookings")