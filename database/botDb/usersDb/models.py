from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Index
from database.botDb.channelsDb.models import ChannelsModel
from database.botDb.paymentsDb.models import PaymentModel
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
