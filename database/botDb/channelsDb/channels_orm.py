from database.engines import async_session
from sqlalchemy import select, exists
from sqlalchemy.dialects.postgresql import insert
from database.commonDb.models import UserModel
from .models import ChannelsModel
import asyncio


class ChannelsOrm:
    @staticmethod
    async def get_users_channels(tg_id: int):
        async with async_session() as session:
            if tg_id:
                stmt = select(ChannelsModel.channel_id, ChannelsModel.title).where(ChannelsModel.owner_id == tg_id)
                result = await session.execute(stmt)
                return result.all()

    @staticmethod
    async def add_user_channel(owner_id, channel_id, title):
        async with async_session() as session:
            stmt = insert(ChannelsModel).values(owner_id=owner_id, channel_id=channel_id, title=title)
            async with session.begin():
                await session.execute(stmt)

    @staticmethod
    async def is_channel_exists(channel_id):
        async with async_session() as session:
            stmt = select(exists().where(ChannelsModel.channel_id==channel_id))
            result = await session.execute(stmt)
            return result.scalar()


channels_orm = ChannelsOrm()
