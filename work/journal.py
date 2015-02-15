from bs4 import BeautifulSoup
from urllib.parse import urlencode
import requests
import sys
import re

__author__ = 'Kami'
URL = "http://www.informatik.uni-trier.de/~ley/db/journals/{0}/{0}{1}.html"
SCHOLAR = "http://scholar.google.it/scholar?"


def get_conf_data(conf, no, kwds):
    url = URL.format(conf.lower(), no)
    resp = requests.get(url)

    if resp.status_code != 200:
        raise ValueError("Exit with code {}".format(resp.status_code))

    bs = BeautifulSoup(resp.text)
    pattern = "|".join(kwds)
    for t in bs.select("span.title"):
        if re.search(pattern, t.text, re.IGNORECASE):
            yield t.text


if __name__ == "__main__":
    conf = "TIST"
    no = 5
    kwds = "twitter", "social", "trust", "spam", "user"

    print("Papers with the keywords", kwds, "on", conf, no)
    print("-" * 100)
    for n, text in enumerate(get_conf_data(conf, no, kwds)):
        print(text, " [", SCHOLAR, urlencode({'q': text}), "]", sep="")
    print("-" * 100)
    print("Found", n + 1, "papers.")