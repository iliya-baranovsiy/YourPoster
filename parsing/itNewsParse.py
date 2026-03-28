from database.parseDB.models import ItTechnologiesOrm
from parsing.baseSettings import BaseParse


class ItNewsParsing(BaseParse):
    def __init__(self):
        self.url = "https://habr.com/ru/news/"
        self.domain = 'https://habr.com'
        super().__init__(ItTechnologiesOrm)

    def _get_urls(self):
        urls = []
        count = 1
        for i in range(0, 2):
            soup = self._get_soup(self.url + f'page{count}/')
            divs_list = soup.find_all('a', class_=['tm-title__link'])
            for i in divs_list:
                url = self.domain + i.attrs['href']
                urls.append(url)
            count += 1
        return urls

    def _get_detail_info(self, url):
        soup = self._get_soup(url)
        try:
            title = soup.find('h1', class_=['tm-title tm-title_h1']).text
        except:
            return 0
        if title in self._exists_titles:
            return 0
        else:
            try:
                content_div = soup.select_one('#post-content-body > div > div > div')
                paragraphs = content_div.find_all('p')
                # input ai generate func
                content = ''.join([i.text for i in paragraphs])
                try:
                    pic_url = content_div.find('figure').find('img').attrs['src']
                except:
                    pic_url = None
                return [title, content, pic_url]
            except:
                return 0


it_news = ItNewsParsing()
