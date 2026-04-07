from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Index, Numeric, ForeignKey, Enum, Date, text
from datetime import date
from database.botDb.optionsDb.payment_options import PaymentOptions
from database.engines import Base


class UserModel(Base):
    __tablename__ = "Users"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str | None] = mapped_column(String(256))
    channels: Mapped[list["ChannelsModel"]] = relationship("ChannelsModel", back_populates="owner")
    payments: Mapped[list["PaymentModel"]] = relationship("PaymentModel", back_populates="user")

    def __init__(self, tg_id, username):
        self.tg_id = tg_id
        self.username = username

    __table_args__ = (Index("tg_id_index", "tg_id"),)


class ChannelsModel(Base):
    __tablename__ = "Channels"

    id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(unique=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("Users.tg_id"))
    owner: Mapped["UserModel"] = relationship("UserModel", back_populates="channels")


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
