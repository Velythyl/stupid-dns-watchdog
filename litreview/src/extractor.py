import re

from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urlparse

# An extractor must return a tuple of this form:
# (<url to download the pdf>, <bibtex>, <title>, <authors>, <abstract>)

def rebuild_url(scheme, netloc, path):
    return scheme+"://"+netloc+path

class _Extractor():
    def __init__(self, url):
        self.main_page = urllib.request.urlopen(url).read()
        self._url = url
        self.main_soup = BeautifulSoup(self.main_page, "html.parser")
        self.main_soup.prettify()

    def url(self):
        return self._url

    def pdflink(self):
        raise NotImplemented()

    def bibtex(self):
        raise NotImplemented()

    def abstract(self):
        raise NotImplemented()

    def authors(self):
        raise NotImplemented()

    def title(self):
        raise NotImplemented()

    def date(self):
        raise NotImplemented()

    def filename(self):
        return re.sub(r"\W+", "", self.title())

class Arxiv(_Extractor):
    def pdflink(self):
        parsedurl = urlparse(self.url())

        newpath = parsedurl.path.replace("/abs", "/pdf")+".pdf"
        return rebuild_url(parsedurl.scheme, parsedurl.netloc, newpath)

    def bibtex(self):
        #temp = self.main_soup.select("#bib-cite-target")
        return "TODO"

    def abstract(self):
        selected = self.main_soup.select(".abstract.mathjax")

        if len(selected) > 1:
            raise NotImplemented("more than one selected")

        abstract = str(selected[0].contents[2]).strip()
        return abstract

    def authors(self):
        selected = self.main_soup.select(".authors")

        if len(selected) > 1:
            raise NotImplemented("more than one selected")

        try:
            selected[0].find("span").replace_with("")
        except:
            pass
        authors = str(selected[0].get_text()).strip()
        return authors

    def date(self):
        selected = self.main_soup.select(".dateline")
        if len(selected) > 1:
            raise NotImplemented("more tha one selected")

        date_text = None
        for i in reversed(range(len(selected[0].contents))):
            date_text = str(selected[0].contents[i])
            matches = re.findall(r"\d\d? [A-Z][a-z][a-z] \d\d\d\d", date_text)
            if len(matches) == 1:
                break

        if date_text is None:
            raise NotImplemented("oh no no date")

        return matches[0]

    def title(self):
        selected = self.main_soup.select(".title.mathjax")

        if len(selected) > 1:
            raise NotImplemented("more than one selected")

        title = str(selected[0].contents[1]).strip()
        return title

    def filename(self):
        parsedurl = urlparse(self.url())
        return parsedurl.path.replace("/abs/", "")