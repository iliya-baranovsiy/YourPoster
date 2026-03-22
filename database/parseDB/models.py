from sqlalchemy import Date, Index, String
from sqlalchemy.orm import Mapped, mapped_column
import datetime
from database.parseDB.engines import Base


class NewsOrm(Base):
    __tablename__ = "WorldNews"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str]
    pictureUrl: Mapped[str | None]
    addingDate: Mapped[datetime.date] = mapped_column(Date)
    dropDate: Mapped[datetime.date] = mapped_column(Date)

    __table_args__ = (
        Index('title|drop_index_news', 'title', 'dropDate'),
    )


class SportOrm(Base):
    __tablename__ = "Sports"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str]
    pictureUrl: Mapped[str | None]
    addingDate: Mapped[datetime.date] = mapped_column(Date)
    dropDate: Mapped[datetime.date] = mapped_column(Date)

    __table_args__ = (
        Index('title|drop_index_sports', 'title', 'dropDate'),
    )


class CryptoCurrencyOrm(Base):
    __tablename__ = "CryptoCurrency"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str]
    pictureUrl: Mapped[str | None]
    addingDate: Mapped[datetime.date] = mapped_column(Date)
    dropDate: Mapped[datetime.date] = mapped_column(Date)

    __table_args__ = (
        Index('title|drop_index_crypto', 'title', 'dropDate'),
    )


class ItTechnologiesOrm(Base):
    __tablename__ = "ItTechnologies"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str]
    pictureUrl: Mapped[str | None]
    addingDate: Mapped[datetime.date] = mapped_column(Date)
    dropDate: Mapped[datetime.date] = mapped_column(Date)

    __table_args__ = (
        Index('title|drop_index_IT', 'title', 'dropDate'),
    )


class AiNewsOrm(Base):
    __tablename__ = "AiNews"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str]
    pictureUrl: Mapped[str | None]
    addingDate: Mapped[datetime.date] = mapped_column(Date)
    dropDate: Mapped[datetime.date] = mapped_column(Date)

    __table_args__ = (
        Index('title|drop_index_AI', 'title', 'dropDate'),
    )


class ScienceOrm(Base):
    __tablename__ = "Science"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str]
    pictureUrl: Mapped[str | None]
    addingDate: Mapped[datetime.date] = mapped_column(Date)
    dropDate: Mapped[datetime.date] = mapped_column(Date)

    __table_args__ = (
        Index('title|drop_index_science', 'title', 'dropDate'),
    )
