from sqlalchemy import select

from .models    import User
from .schemas   import UserCreate
from sqlmodel.ext.asyncio import AsyncSession


class AuthService:
    async def get_user(self, email: str, session: AsyncSession, username: str):#email ra username duita pani lekhna parxa kina bhane email ra username duita pani unique hunxa
      statement = select(User).where((User.email == email) | (User.username == username))
      result = await session.exec(statement)
      return result.first()#first() le result ma aako list bata pahilo element return garxa, jasma email ra username duita pani match hunxa
    

    async def user_exists(self, email: str, session: AsyncSession):
      user=await self.get_user_by_email(email, session)

      return True if user is not None else False #user xa vane True return garxa, user xaina vane False return garxa