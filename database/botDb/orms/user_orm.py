from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
import asyncio
from database.engines import async_session
from database.botDb.models import UserModel, PaymentModel, ChannelsModel
from database.botDb.schemas import PaymentDTO


class UserOrmWork:
    @staticmethod
    async def create_user(tg_id: int, username: str | None):
        async with async_session() as session:
            if tg_id:
                user = insert(UserModel).values(tg_id=tg_id, username=username)
                unique_user = user.on_conflict_do_nothing(index_elements=['tg_id'])
                payment = insert(PaymentModel).values(user_id=tg_id).on_conflict_do_nothing(index_elements=['user_id'])
                async with session.begin():
                    await session.execute(unique_user)
                    await session.execute(payment)

    @staticmethod
    async def get_users_channels(tg_id: int):
        async with async_session() as session:
            if tg_id:
                stmt = select(ChannelsModel.channel_id).join(UserModel.channels).where(UserModel.tg_id == tg_id)
                result = await session.execute(stmt)
                return result.scalars().all()

    @staticmethod
    async def get_user_payment_plan_info(tg_id):
        async with async_session() as session:
            if tg_id:
                query = select(PaymentModel.payment_plan,
                               PaymentModel.balance,
                               PaymentModel.activate_date,
                               PaymentModel.end_date).where(
                    PaymentModel.user_id == tg_id
                )
                executing = await session.execute(query)
                result = executing.all()
                result_dto = [PaymentDTO(
                    balance=row[1],
                    payment_plan=row[0],
                    activate_date=row[2],
                    end_date_row=row[3]
                ) for row in result]
                return result_dto[0]


user_db = UserOrmWork()
