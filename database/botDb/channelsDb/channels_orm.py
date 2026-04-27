from database.engines import async_session
from sqlalchemy import select, exists
from sqlalchemy.dialects.postgresql import insert
from database.commonDb.models import UserModel
from ..paymentPlansDB.models import PaymentModel
from .models import ChannelsModel
from .schemas import BaseParameters
from redisWork.autopostingCash.channels_cash import channels_cache
import asyncio


class ChannelsOrm:

    @staticmethod
    async def get_user_base_parameters(tg_id: int):
        async with async_session() as session:
            stmt = select(ChannelsModel.channel_id, ChannelsModel.title).where(ChannelsModel.owner_id == tg_id)
            payment_stmt = select(PaymentModel.payment_plan).where(PaymentModel.user_id == tg_id)
            channels_query = await session.execute(stmt)
            payment_query = await session.execute(payment_stmt)
            dto_data = BaseParameters(channels=channels_query.all(), payment_plan=payment_query.scalar())
            return dto_data

    @staticmethod
    async def add_user_channel(owner_id, channel_id, title):
        async with async_session() as session:
            stmt = insert(ChannelsModel).values(owner_id=owner_id, channel_id=channel_id, title=title)
            async with session.begin():
                await channels_cache.set_channels_cache(tg_id=owner_id, channel_tup=tuple([channel_id, title]))
                await session.execute(stmt)

    @staticmethod
    async def is_channel_exists(channel_id):
        async with async_session() as session:
            stmt = select(exists().where(ChannelsModel.channel_id == channel_id))
            result = await session.execute(stmt)
            return result.scalar()


channels_orm = ChannelsOrm()
