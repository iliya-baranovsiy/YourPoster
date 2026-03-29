from database.parseDB.models import CryptoCurrencyOrm
from parsing.baseSettings import BaseParse


class CryptoNewsParsing(BaseParse):
    def __init__(self):
        self.url = "https://forklog.com/news/"
        super().__init__(CryptoCurrencyOrm)

    def _get_urls(self):
        soup = self._get_soup(url=self.url)
        divs_list = soup.find_all('div', class_=['cell'])
        urls = [i.find('a', href=True).attrs['href'] for i in divs_list]
        return urls

    def _get_detail_info(self, url):
        soup = self._get_soup(url=url, encoding='utf-8')
        title = soup.find('h1').text
        if title in self._exists_titles:
            return 0
        else:
            paragraphs = soup.find_all('p')
            # input ai generate func
            content = ''.join([i.text for i in paragraphs])
            try:
                pic_url = soup.find('img', class_=['attachment-full size-full wp-post-image']).attrs['src']
            except:
                pic_url = None
            return [title, content, pic_url]


crypto_news = CryptoNewsParsing()
