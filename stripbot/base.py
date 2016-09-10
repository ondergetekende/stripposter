import datetime
from urllib.parse import urljoin

import lxml.html
import requests


def update(comic_model):

    session = requests.Session()
    doc = comic_model.retrieve_index(session)

    #
    if comic_model.css_selector:
        instances = doc.cssselect(comic_model.css_selector)
    else:
        instances = [doc]

    # Find the comics on the index page
    results = []
    for element in instances:
        result = comic_model(element)
        result.extract_comic()

        # make sure the paths are absolute
        if result.image_url:
            result.image_url = urljoin(comic_model.base_url, result.image_url)

        if result.page_url:
            result.page_url = urljoin(comic_model.base_url, result.page_url)

        results.append(result)

    return results

    def extract_comic(self, elm):
        raise NotImplementedError()


class BaseComicModel():
    base_url = None  # The primary url to retrieve to update the comic
    author = None  # The author of this comic.
    name = None  # The name of this comic

    # The selector for CSS comics. This is used to find references to the
    # comics in the page at base_url. Leave empty for single page comics.
    css_selector = None

    @classmethod
    def retrieve_index(cls, session):
        response = session.get(cls.base_url)
        # Just throw an exception for non-success statuses
        response.raise_for_status()
        return lxml.html.document_fromstring(response.content)

    def __init__(self, element):
        self._id = None
        self.page_url = None
        self.image_url = None
        self.date = None
        self.element = element

    @property
    def id(self):
        if not self._id:
            self._id = self.page_url or self.image_url

        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def post_title(self):
        return "[%s] %s (%s)" % (self.name, self.title, self.author)

    @property
    def post_url(self):
        return self.page_url

    @property
    def post_comment(self):
        return ""

    @property
    def title(self):
        return self.date.strftime("%d/%m/%Y")
