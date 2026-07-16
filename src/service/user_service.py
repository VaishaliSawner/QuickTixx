from src.exception.custom_exception import UserAlreadyExistsException,InvalidLoginException
from src.model.user import User
from src.repository.user_repo import UserRepository
from src.util.password import hash_password,verify_password


class UserService:
    def __init__(self,session):
        self.user_repo = UserRepository(session)

    async def register_user(self,user:User):
        existing_user=await self.user_repo.get_user_by_email(user.email)
        if existing_user:
            raise UserAlreadyExistsException()

        user.password=hash_password(user.password)
        if(
            user.name.lower() == "admin"
            and user.email.lower() == "admin@gmail.com"
        ):
         user.role = "admin"
        else:
            user.role = "user"
        return await self.user_repo.create_user(user)

    async def login_user(self,email:str,password:str):
        user = await self.user_repo.get_user_by_email(email)
        if not user:
            raise InvalidLoginException()
        if not verify_password(user.password,password):
            raise InvalidLoginException()
        return user

    async def get_user_by_id(self,user_id:int):
        return await self.user_repo.get_user_by_id(user_id)

