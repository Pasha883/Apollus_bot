from Database.models import async_session
from Database.models import User
from sqlalchemy import select


async def set_user(user_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.id == user_id))


async def get_users():
    async with async_session() as session:
        return await session.scalars(select(User))



async def in_database(user_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))

        if not user:
            return True #FALSE!!!!!!
        else:
            return True


async def register(user_id, user_name, status):
    async with async_session() as session:
        session.add(User(id=user_id, name=user_name, rights=status, messages=0))
        await session.commit()


async def messages_counter_update(user_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        user.messages = user.messages + 1
        await session.commit()


async def set_rights(user_id, rights):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        user.rights = rights
        await session.commit()
