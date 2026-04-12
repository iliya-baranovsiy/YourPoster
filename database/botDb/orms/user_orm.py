from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, update
import asyncio
from database.engines import async_session
from database.botDb.models import UserModel, PaymentModel, ChannelsModel
from database.botDb.schemas import PaymentDTO
from datetime import date, timedelta
from redisWork.autopostingCash.subscribe_info_cashing import redis_cash


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

    @staticmethod
    async def update_user_payment_plan(tg_id, balance, payment_plan, cashing):
        async with async_session() as session:
            activate_date = date.today()
            end_date = date.today() + timedelta(days=31)
            stmt = update(PaymentModel).values(balance=balance, payment_plan=payment_plan, activate_date=activate_date,
                                               end_date=end_date).where(PaymentModel.user_id == tg_id)
            async with session.begin():
                if cashing:
                    await session.execute(stmt)
                    dto_data = PaymentDTO(balance=balance, payment_plan=payment_plan, end_date_row=end_date)
                    await redis_cash.set_cash(tg_id=tg_id,
                                              payment_plan=str(dto_data.payment_plan),
                                              balance=float(dto_data.balance),
                                              end_date=str(dto_data.end_date))
                else:
                    await session.execute(stmt)


user_db = UserOrmWork()
