import requests
from bs4 import BeautifulSoup
import concurrent.futures
from database.parseDB.parseOrm import create_records, get_titles
from parsing.parseTools.uniqueValues import unique


class BaseParse:
    def __init__(self, model):
        self.model = model
        self._exists_titles = get_titles(self.model)

    def _get_html(self, url, headers=None):
        response = requests.get(url=url, headers=headers)
        return response.text

    def _get_soup(self, url, headers=None):
        soup = BeautifulSoup(self._get_html(url, headers=headers), 'html.parser')
        return soup

    def parse(self):
        urls = self._get_urls()
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            preview = list(executor.map(self._get_detail_info, urls))
            result = [i for i in preview if i != 0]
            unique_result = unique(result)
            create_records(unique_result, self.model)
