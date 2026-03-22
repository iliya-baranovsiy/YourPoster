from engines import sync_session
from models import *


def create_record():
    with sync_session() as session:
        news = NewsOrm(title='test', content='testcontent', pictureUrl='url345')
        session.add(news)
        session.commit()


create_record()
