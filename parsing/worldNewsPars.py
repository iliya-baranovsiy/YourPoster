from baseSettings import BaseParse
from database.parseDB.models import NewsOrm


class WorldNewsParsing(BaseParse):
    def __init__(self):
        self.__url = "https://ria.ru/world/"
        super().__init__(NewsOrm)

    def _get_urls(self):
        soup = self._get_soup(self.__url)
        list_items = soup.find_all('div', class_=['list-item'])
        url_list = []
        for i in list_items:
            url = i.find('a', href=True)
            url_list.append(url['href'])
        return url_list

    def _get_detail_info(self, url):
        soup = self._get_soup(url)
        try:
            title = soup.find('div', class_=['article__title']).text
        except:
            return 0
        content = ''
        if title in self._exists_titles:
            return 0
        else:
            content_list = soup.find_all('div', class_=['article__text'])
            content_list[0].find('strong').decompose()
            for i in content_list:
                content += i.text
            # input ai_generate func
            result_content = content.lstrip()
            try:
                pic_url = soup.find('div', class_=['photoview__open']).find('img').attrs['src']
            except:
                pic_url = None
            return [title, result_content, pic_url]


world_news = WorldNewsParsing()
