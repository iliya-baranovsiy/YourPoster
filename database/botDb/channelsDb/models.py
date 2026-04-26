from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Index, BigInteger
from database.engines import Base


class ChannelsModel(Base):
    __tablename__ = "Channels"

    id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    title: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey("Users.tg_id"))
    owner: Mapped["UserModel"] = relationship("UserModel", back_populates="channels")

    __table_args__ = (Index("channels_index", "channel_id", "owner_id"),)
