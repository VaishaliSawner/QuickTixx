from sqlalchemy import Float,Integer,String,Text
from sqlalchemy.orm import Mapped,mapped_column,relationship
from src.db_config.database import Base

class Movie(Base):
    __tablename__ = "movie"
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    movie_name:Mapped[str]=mapped_column(String(100),nullable=False)
    language:Mapped[str]=mapped_column(String(50),nullable=False)
    genre:Mapped[str]=mapped_column(String(50),nullable=False)
    duration:Mapped[str]=mapped_column(String(30),nullable=False)
    price:Mapped[float]=mapped_column(Float,nullable=False)
    available_seats:Mapped[int]=mapped_column(Integer,nullable=False)
    description:Mapped[str]=mapped_column(Text,nullable=False)
    image:Mapped[str]=mapped_column(String(255),nullable=False)

    bookings = relationship("Booking",back_populates="movie")
