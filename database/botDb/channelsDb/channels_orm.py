from database.engines import async_session
from sqlalchemy import select
from database.commonDb.models import UserModel
from .models import ChannelsModel


class ChannelsOrm:
    @staticmethod
    async def get_users_channels(tg_id: int):
        async with async_session() as session:
            if tg_id:
                stmt = select(ChannelsModel.channel_id).join(UserModel.channels).where(UserModel.tg_id == tg_id)
                result = await session.execute(stmt)
                return result.scalars().all()


channels_orm = ChannelsOrm()
