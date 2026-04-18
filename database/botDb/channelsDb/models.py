from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from database.engines import Base


class ChannelsModel(Base):
    __tablename__ = "Channels"

    id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(unique=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("Users.tg_id"))
    owner: Mapped["UserModel"] = relationship("UserModel", back_populates="channels")
