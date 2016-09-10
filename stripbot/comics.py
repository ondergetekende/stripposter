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
    base_url = "http://www.sigmund.nl/"
    name = "Sigmund"
    author = "Peter de Wit"

    css_selector = 'img[src^="strips/sig1"]'

    def extract_comic(self):
        self.image_url = self.element.get('src')
        self.id = self.image_url.split("/sig")[-1].rsplit('.')[0]
        self.date = datetime.datetime.strptime(self.id, "%y%m%d")
        self.page_url = ("http://www.sigmund.nl/?d=%s" %
                         self.date.isoweekday())

    @property
    def post_url(self):
        return self.image_url

    @property
    def post_comment(self):
        return ("[Hier](%s) staat de pagina met de strip. Omdat "
                "[sigmund](http://sigmund.nl) geen archief heeft, linkt de "
                "post naar het image plaatje, zodat deze reddit post over "
                "een week nog ergens naar linkt." % self.page_url)


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
