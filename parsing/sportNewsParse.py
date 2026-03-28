from baseSettings import BaseParse
from database.parseDB.models import SportOrm


class SportNewsParsing(BaseParse):
    def __init__(self):
        self.url = "https://www.championat.com/news/1.html"
        self.domain = 'https://www.championat.com'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/115.0.0.0 Safari/537.36'
        }
        super().__init__(SportOrm)

    def _get_urls(self):
        soup = self._get_soup(self.url, self.headers)
        news_items_content = soup.find_all('div', class_=['news-item__content'])
        url_list = []
        for i in news_items_content:
            url = i.find('a', href=True)
            url_list.append(self.domain + url['href'])
        return url_list

    def _get_detail_info(self, url):
        soup = self._get_soup(url, headers=self.headers)
        title = soup.find('div', class_=['article-head__title']).text
        if title in self._exists_titles:
            return 0
        else:
            article_content = soup.find('div', class_=['article-content'])
            content_paragraphs = article_content.find_all('p')
            # input ai_generate func
            content = ''.join(
                [i.text for i in content_paragraphs if not i.find_parent('div', class_=['content-photo'])])
            try:
                article_photo_div = soup.find('div', class_=['article-head__photo'])
                picture_url = article_photo_div.find('img').attrs['src']
            except:
                picture_url = None
            return [title, content, picture_url]


sport_news = SportNewsParsing()
