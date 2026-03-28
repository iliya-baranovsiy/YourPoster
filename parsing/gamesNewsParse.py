from database.parseDB.models import GamesOrm
from parsing.baseSettings import BaseParse


class GamesParsing(BaseParse):
    def __init__(self):
        self.url = "https://www.playground.ru/news"
        super().__init__(GamesOrm)

    def _get_urls(self):
        count = 1
        urls = []
        for i in range(0, 2):
            soup = self._get_soup(self.url + f'?p={count}')
            post_divs = soup.find_all('div', class_=['post-title'])
            for i in post_divs:
                urls.append(i.find('a', href=True).attrs['href'])
            count += 1
        return urls

    def _get_detail_info(self, url):
        soup = self._get_soup(url)
        title = soup.find('h1', class_=['post-title']).text.lstrip()
        if title in self._exists_titles:
            return 0
        else:
            content_div = soup.find('div', class_=['article-content js-post-item-content js-redirect'])
            paragraphs = content_div.find_all('p')
            # input ai_generate func
            content = ''.join([i.text for i in paragraphs])
            try:
                pic_url = content_div.find('figure').find('a', href=True).attrs['href']
            except:
                pic_url = None
            return [title, content, pic_url]


games_news = GamesParsing()
