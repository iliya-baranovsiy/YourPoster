from database.engines import sync_session
from sqlalchemy import select, delete
from database.parseDB.models import *
from datetime import datetime, timedelta


def create_records(news_list: list, model: object):
    with sync_session() as session:
        if news_list is not None:
            news = list(model(title=list_[0], content=list_[1], pictureUrl=list_[2]) for list_ in news_list)
            session.add_all(news)
            session.commit()
        else:
            pass


def get_titles(model: object):
    with sync_session() as session:
        query = select(model.title)
        result = session.execute(query)
        titles = result.scalars().all()
        return titles


def clean_old_data():
    model_list = [NewsOrm, GamesOrm, ScienceOrm, CryptoCurrencyOrm, SportOrm, ShowBisOrm, AiNewsOrm, ItTechnologiesOrm]
    target_time = datetime.now().date() - timedelta(days=2)
    with sync_session() as session:
        for i in model_list:
            to_drop = delete(i).where(target_time == i.dropDate)
            session.execute(to_drop)
        session.commit()
