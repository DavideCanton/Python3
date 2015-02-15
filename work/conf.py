from bs4 import BeautifulSoup
from urllib.parse import urlencode
import requests
import sys
import re

__author__ = 'Kami'
URL = "http://www.informatik.uni-trier.de/~ley/db/conf/{0}/{0}{1}.html"
SCHOLAR = "http://scholar.google.it/scholar?"


def get_conf_data(conf, year, kwds):
    url = URL.format(conf.lower(), year)
    resp = requests.get(url)

    if resp.status_code != 200:
        raise ValueError("Exit with code {}".format(resp.status_code))

    bs = BeautifulSoup(resp.text)
    pattern = "|".join(kwds)
    for t in bs.select("span.title"):
        if re.search(pattern, t.text, re.IGNORECASE):
            yield t.text


if __name__ == "__main__":
    conf = "CHI"
    year = 2013
    kwds = "social", "topic", "model"

    print("Papers with the keywords", kwds, "on", conf, year)
    print("-" * 100)
    for n, text in enumerate(get_conf_data(conf, year, kwds)):
        print(text, " [", SCHOLAR, urlencode({'q': text}), "]", sep="")
    print("-" * 100)
    print("Found", n + 1, "papers.")