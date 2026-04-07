from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
import asyncio
from database.engines import async_session
from database.botDb.models import UserModel, PaymentModel, ChannelsModel


class UserOrmWork:
    async def create_user(self, tg_id: int, username: str | None):
        async with async_session() as session:
            if tg_id:
                user = insert(UserModel).values(tg_id=tg_id, username=username)
                unique_user = user.on_conflict_do_nothing(index_elements=['tg_id'])
                payment = insert(PaymentModel).values(user_id=tg_id).on_conflict_do_nothing(index_elements=['user_id'])
                async with session.begin():
                    await session.execute(unique_user)
                    await session.execute(payment)

    async def get_users_channels(self, tg_id: int):
        async with async_session() as session:
            if tg_id:
                stmt = select(ChannelsModel.channel_id).join(UserModel.channels).where(UserModel.tg_id == tg_id)
                result = await session.execute(stmt)
                return result.scalars().all()

    async def set_user_payment_plan(self):
        pass


user_db = UserOrmWork()
