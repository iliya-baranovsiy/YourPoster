from database.engines import sync_session
from sqlalchemy import select
from database.parseDB.models import *


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
