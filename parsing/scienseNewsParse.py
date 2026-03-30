from parsing.baseSettings import BaseParse
from database.parseDB.models import ScienceOrm


class ScienceParsing(BaseParse):
    def __init__(self):
        self.url = "https://new-science.ru"
        super().__init__(ScienceOrm)

    def _get_urls(self):
        soup = self._get_soup(url=self.url)
        urls = [self.url + '/' + i.attrs['href'] for i in soup.find_all('a', class_=['post-thumb'], href=True)]
        return urls

    def _get_detail_info(self, url):
        soup = self._get_soup(url=url)
        title = soup.find('h1', class_=['post-title entry-title']).text.lstrip()
        if title in self._exists_titles:
            return 0
        else:
            content_div = soup.find('div', class_=['entry-content entry clearfix'])
            # input ai generate func
            content = ''.join([i.text for i in content_div.find_all('p')])
            try:
                pic_url = self.url + soup.find('img', class_=[
                    'attachment-jannah-image-post size-jannah-image-post wp-post-image']).attrs['src']
            except:
                pic_url = None
            return [title, content, pic_url]


science_news = ScienceParsing()
