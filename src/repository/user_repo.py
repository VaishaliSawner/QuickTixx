from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.model.user import User

class UserRepository:
    def __init__(self,session:AsyncSession):
        self.session = session

    async def create_user(self,user:User):
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def get_user_by_email(self,email:str):
        query=select(User).where(User.email == email)
        result=await self.session.execute(query)
        return result.scalar()


    async def get_user_by_id(self, user_id: int):
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_all_users(self):
        query = select(User)
        result = await self.session.execute(query)
        return result.scalars().all()