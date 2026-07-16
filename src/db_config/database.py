from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

DB_URL= "mysql+aiomysql://root:VAISHALI@localhost/movie_ticket_booking"

engine = create_async_engine(DB_URL,echo=True)

SessionLocal = async_sessionmaker(bind=engine,expire_on_commit=False)

class Base(DeclarativeBase):
    pass