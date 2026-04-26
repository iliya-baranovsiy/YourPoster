from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Index, Numeric, text
from database.engines import Base
from ..botDb.channelsDb.models import ChannelsModel
from database.botDb.paymentPlansDB.models import PaymentModel


class UserModel(Base):
    __tablename__ = "Users"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str | None] = mapped_column(String(256))
    balance: Mapped[Numeric] = mapped_column(Numeric(12, 2), default=0, server_default=text('0'))
    channels: Mapped[list["ChannelsModel"]] = relationship("ChannelsModel", back_populates="owner")
    payments: Mapped[list["PaymentModel"]] = relationship("PaymentModel", back_populates="user")

    __table_args__ = (Index("tg_id_index", "tg_id"),)
