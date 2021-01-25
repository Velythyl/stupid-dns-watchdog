import re

from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urlparse

# An extractor must return a tuple of this form:
# (<url to download the pdf>, <bibtex>, <title>, <authors>, <abstract>)

def rebuild_url(scheme, netloc, path):
    return scheme+"://"+netloc+path

def eprint2bibtex(eprint_number):
    def soup_from_url(url):
        main_page = urllib.request.urlopen(url).read()
        _url = url
        main_soup = BeautifulSoup(main_page, "html.parser")
        main_soup.prettify()
        return main_soup

    def dblp():
        search = soup_from_url(
            f"https://dblp.uni-trier.de/search?q={eprint_number}"
        ).select(".publ")

        if len(search) > 1:
            print("More than one dblp search result, assuming first is the correct one")

        search = search[0]
        a = search.contents[0].contents[1].contents[0].contents[0]
        bibtex_link = a.attrs["href"]

        bibtex = soup_from_url(
            bibtex_link
        ).select("#bibtex-section")

        if len(bibtex) > 1:
            raise NotImplemented("more than one selected")

        bibtex = bibtex[0].getText().strip()
        return bibtex

    def arxiv():
        bibtex = soup_from_url(
            f"https://arxiv2bibtex.org/?q={eprint_number}&format=bibtex"
        ).select(".wikiinfo")[0]

        bibtex = bibtex.getText().strip()
        return bibtex

    try:
        return dblp()
    except:
        pass

    print("Could not use DBLP to extract bibtex, falling back on arxiv")

    try:
        return arxiv()
    except:
        return "TODO (could not extract bibtex)"



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
        return eprint2bibtex(urlparse(self.url()).path.split("/")[-1])

    def abstract(self):
        selected = self.main_soup.select(".abstract.mathjax")

        if len(selected) > 1:
            raise NotImplemented("more than one selected")

        abstract = str(selected[0].contents[2]).strip()
        return abstract.strip()

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

        return matches[0].strip()

    def title(self):
        selected = self.main_soup.select(".title.mathjax")

        if len(selected) > 1:
            raise NotImplemented("more than one selected")

        title = str(selected[0].contents[1]).strip()
        return title.strip()

    def filename(self):
        parsedurl = urlparse(self.url())
        return parsedurl.path.replace("/abs/", "").strip()