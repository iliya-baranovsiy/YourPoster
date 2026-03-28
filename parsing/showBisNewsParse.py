from parsing.baseSettings import BaseParse
from database.parseDB.models import ShowBisOrm


class ShowBisNewsParsing(BaseParse):
    def __init__(self):
        self.url = "https://www.msk.kp.ru/daily/showbis/"
        self.domain = "https://www.msk.kp.ru"
        super().__init__(ShowBisOrm)

    def _get_urls(self):
        soup = self._get_soup(url=self.url)
        div_list = soup.find_all('div', class_=['sc-1tputnk-12 cizwKg'])
        url_list = []
        for i in div_list:
            preview_url = i.find('a', href=True)['href']
            if preview_url.startswith('https'):
                url_list.append(preview_url)
            else:
                url_list.append(self.domain + preview_url)
        return url_list

    def _get_detail_info(self, url):
        soup = self._get_soup(url)
        if '/daily/' in url:
            title = soup.find('h1', class_=['sc-j7em19-3 eyeguj']).text
            if title in self._exists_titles:
                return 0
            else:
                content_div = soup.find('div', class_=['sc-14f2vgk-1 WDCqj'])
                for i in content_div.find_all('div', class_=['sc-1qq61ae-9 bnbONe']):
                    i.decompose()
                for i in content_div.find_all('div', class_=['sc-1qq61ae-9 hmuIuG']):
                    i.decompose()
                paragraphs = content_div.find_all('p')
                # input ai_generate func
                content = ''.join([i.text for i in paragraphs])
                pic_url = soup.find('img', class_=['sc-foxktb-1 cYprnQ']).attrs['src']
                return [title, content, pic_url]
        else:
            return 0


showBis_news = ShowBisNewsParsing()
