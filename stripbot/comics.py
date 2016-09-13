import datetime

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
