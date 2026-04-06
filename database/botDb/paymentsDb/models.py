from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Numeric, Date, Enum, text
from datetime import date, timedelta
from database.botDb.paymentsDb.options import PaymentOptions
from database.engines import Base


class PaymentModel(Base):
    __tablename__ = "User_payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('Users.tg_id'), unique=True)
    balance: Mapped[Numeric] = mapped_column(Numeric(12, 2), default=0, server_default=text('0'))
    payment_plan: Mapped[PaymentOptions] = mapped_column(Enum(PaymentOptions),
                                                         default=PaymentOptions.STANDART,
                                                         server_default=text("'STANDART'"))
    activate_date: Mapped[date] = mapped_column(Date, nullable=True)
    end_date: Mapped[date] = mapped_column(Date, nullable=True)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="payments")
