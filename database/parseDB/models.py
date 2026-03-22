from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column
import datetime
from database.parseDB.engines import Base


class NewsOrm(Base):
    __tablename__ = "News"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    pictureUrl: Mapped[str | None]
    addingDate: Mapped[datetime.date] = mapped_column(Date)
    dropDate: Mapped[datetime.date] = mapped_column(Date)
