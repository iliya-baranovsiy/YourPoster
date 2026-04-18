from ..engines import async_session
from sqlalchemy.dialects.postgresql import insert
from .models import UserModel
from ..botDb.paymentPlansDB.models import PaymentModel


class UserOrm:
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


user_orm = UserOrm()
