import datetime
from urllib.parse import urlparse, parse_qs

from .base import BaseComicModel


class DirkJan(BaseComicModel):
    base_url = "http://dirkjan.nl/"
    name = "Dirkjan"
    author = "Mark Retera"

    css_selector = "#main .post-navigation a"

    def extract_comic(self,):
        self.page_url = self.element.get('href')
        self.id = self.page_url.strip("/").rsplit('/')[-1]
        self.date = datetime.datetime.strptime(self.id.split("_")[0],
                                               "%Y%m%d")


class Sigmund(BaseComicModel):
    base_url = "http://www.volkskrant.nl/foto/sigmund-2~p4368403/"
    name = "Sigmund"
    author = "Peter de Wit"

    css_selector = '.photo-set__list figure'

    def extract_comic(self):
        self.page_url = self.element.cssselect('a')[0].get('href')
        self.image_url = self.element.get('data-hires')
        self.id = self.element.get('data-pid')


class Dingemans(BaseComicModel):
    base_url = "https://www.trouw.nl/cartoons/de-wereld-van-anton-dingeman~b21b94dc/"
    name = "Anton Dingeman"
    author = "Pieter Geenen"

    css_selector = 'article.artstyle section'

    def extract_comic(self):
        self.page_url = self.base_url
        date = self.element.cssselect('h3.title')
        self.id = date
        self.date = datetime.datetime.strptime(date, "%d %B %Y") # 21 augustus 2019
        self.image_url = self.element.cssselect('figure img')[0].get('href')


class Jeroom(BaseComicModel):
    base_url = "http://www.humo.be/jeroom/"
    name = "Jeroom"
    author = "Jeroom"

    css_selector = '.grid-item-4'

    def extract_comic(self):
        self.page_url = self.element.cssselect('a')[0].get('href')
        date = self.element.cssselect('.desc')[0].text
        self.id = date
        self.date = datetime.datetime.strptime(date, "%d-%m-%Y")


class FokkeEnSukke(BaseComicModel):
    base_url = "http://www.foksuk.nl/nl"
    name = "Fokke en Sukke"
    author = " Jean-Marc van Tol"

    css_selector = '.cartoon'

    def extract_comic(self):
        img = self.element.cssselect('img[src^=content]')[0]
        self.page_url = self.element.cssselect('a.active')[0].get('href')
        print(self.page_url)
        self.image_url = img.get('src')
        self.title = img.get('alt').rsplit('(', 1)[0]

        qs = urlparse(self.page_url).query
        qs = dict(parse_qs(qs))
        print (qs)
        date_sec = int(qs['ctime'][0])
        self.id = date_sec
        self.date = (datetime.datetime(1970, 1, 1) + 
                     datetime.timedelta(seconds=date_sec))
