from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession
from .models import User
from .schemas import UserCreate
from .utils import generate_password_hash, verify_password


class AuthService:

    async def get_user(self, email: str, username: str, session: AsyncSession):
        # email OR username check
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

        # password hashing
        user_data_dict["password"] = generate_password_hash(user_data_dict["password"])

        new_user = User(**user_data_dict)

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user