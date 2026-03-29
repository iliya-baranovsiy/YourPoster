from parsing.itNewsParse import ItNewsParsing
from database.parseDB.models import AiNewsOrm


class AiNewsParsing(ItNewsParsing):
    def __init__(self):
        self.url = "https://habr.com/ru/flows/ai_and_ml/news/"
        super().__init__(AiNewsOrm, self.url)


ai_news = AiNewsParsing()
