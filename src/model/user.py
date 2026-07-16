from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column,relationship
from src.db_config.database import Base


class User(Base):
    __tablename__ = "user"
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str]=mapped_column(String(100),nullable=False)
    email:Mapped[str]=mapped_column(String(100),unique=True,nullable=False)
    password:Mapped[str]=mapped_column(String(255),nullable=False)
    role:Mapped[str]=mapped_column(String(20),default="user",nullable=False)

    bookings = relationship("Booking",back_populates="user")