from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Index, ForeignKey, Enum, Date, text
from datetime import date
from .payment_options import PaymentOptions
from database.engines import Base


class PaymentModel(Base):
    __tablename__ = "User_payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('Users.tg_id'), unique=True)
    payment_plan: Mapped[PaymentOptions] = mapped_column(Enum(PaymentOptions),
                                                         default=PaymentOptions.STANDART,
                                                         server_default=text("'STANDART'"))
    automatic_buy: Mapped[bool] = mapped_column(default=False)
    activate_date: Mapped[date] = mapped_column(Date, nullable=True)
    end_date: Mapped[date] = mapped_column(Date, nullable=True)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="payments")

    __table_args__ = (Index("user_payment_index", "user_id", "end_date"),)
