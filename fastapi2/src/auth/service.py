from sqlmodel import select  
from sqlmodel.ext.asyncio.session import AsyncSession
from .models import User
from .schemas import UserCreate
from .utils import generate_password_hash, verify_password


class AuthService:

    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    async def get_user(self, email: str, username: str, session: AsyncSession):
        statement = select(User).where(
            (User.email == email) | (User.username == username)
        )
        result = await session.exec(statement)
        return result.first()

    async def user_exists(self, email: str, username: str, session: AsyncSession):
        user = await self.get_user(email, username, session)
        return user is not None  

    async def create_user(self, user_data: UserCreate, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        user_data_dict["password"] = generate_password_hash(user_data_dict["password"])
        new_user.role="user"

        new_user = User(**user_data_dict)

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user