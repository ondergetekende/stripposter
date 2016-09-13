import datetime
import lxml.html


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
        self._title = None
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
        if self._title:
            return self._title

        return (self.date or datetime.datetime.now()).strftime("%d/%m/%Y")

    @title.setter
    def title(self, value):
        self._title = value

    def __str__(self):
        return "#%s %s" % (self.id, self.image_url or self.page_url)
