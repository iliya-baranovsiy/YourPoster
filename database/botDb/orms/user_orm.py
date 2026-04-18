from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, update
import asyncio
from database.engines import async_session
from database.botDb.models import PaymentModel, ChannelsModel
from database.commonDb.models import UserModel
from database.botDb.schemas import PaymentDTO
from datetime import date, timedelta
from redisWork.autopostingCash.user_payment_cash import user_payment_cash


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
                query = select(UserModel.balance, PaymentModel).join(
                    PaymentModel, UserModel.tg_id == PaymentModel.user_id
                ).where(
                    UserModel.tg_id == tg_id
                )
                executing = await session.execute(query)
                result = executing.all()[0]
                dto_result = PaymentDTO(
                    balance=result[0],
                    payment_plan=result[1].payment_plan,
                    activate_date=result[1].activate_date,
                    end_date_row=result[1].end_date,
                    auto_pay=result[1].automatic_buy
                )

                return dto_result

    @staticmethod
    async def update_user_payment_plan(tg_id, balance, payment_plan, cashing):
        async with async_session() as session:
            activate_date = date.today()
            end_date = date.today() + timedelta(days=31)
            stmt_payment = update(PaymentModel).values(payment_plan=payment_plan,
                                                       activate_date=activate_date,
                                                       end_date=end_date,
                                                       automatic_buy=False).where(PaymentModel.user_id == tg_id)
            stmt_user = update(UserModel).values(balance=balance).where(UserModel.tg_id == tg_id)
            async with session.begin():
                if cashing:
                    await session.execute(stmt_payment)
                    await session.execute(stmt_user)
                    dto_data = PaymentDTO(balance=balance, payment_plan=payment_plan, end_date_row=end_date,
                                          auto_pay=False)
                    await user_payment_cash.set_cash(tg_id=tg_id,
                                              payment_plan=str(dto_data.payment_plan),
                                              balance=float(dto_data.balance),
                                              end_date=str(dto_data.end_date),
                                              auto_pay=False)
                else:
                    await session.execute(stmt_payment)
                    await session.execute(stmt_user)

    @staticmethod
    async def reset_auto_pay_value(tg_id, auto_pay, cashing):
        async with async_session() as session:
            stmt = update(PaymentModel).values(automatic_buy=auto_pay).where(PaymentModel.user_id == tg_id)
            async with session.begin():
                if cashing:
                    await user_payment_cash.reset_auto_pay(auto_pay=auto_pay, tg_id=tg_id)
                    await session.execute(stmt)
                else:
                    await session.execute(stmt)

    @staticmethod
    async def extend_payment_plan_date(tg_id, new_date, result_balance, cashing):
        async with async_session() as session:
            stmt_pays = update(PaymentModel).values(end_date=new_date, automatic_buy=False).where(
                PaymentModel.user_id == tg_id)
            stmt_balance = update(UserModel).values(balance=result_balance).where(UserModel.tg_id == tg_id)
            dto_data = PaymentDTO(balance=result_balance, payment_plan=None, end_date_row=new_date,
                                  auto_pay=False)
            async with session.begin():
                if cashing:
                    await user_payment_cash.extend_payment_plan_date(new_date=str(dto_data.end_date),
                                                              result_balance=float(dto_data.balance),
                                                              tg_id=tg_id)
                    pass
                await session.execute(stmt_balance)
                await session.execute(stmt_pays)


user_db = UserOrmWork()
