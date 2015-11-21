from bs4 import BeautifulSoup

__author__ = 'davide'

import urllib.error
import urllib.parse
import urllib.request


ARTIST = "ZZ"
TITLE = "Samurai Blue"
URL_TEMPLATE = "http://www.songlyrics.com/{}/{}-lyrics/"


def convert(s):
    return urllib.parse.quote_plus("-".join(s.lower().split()))


if __name__ == "__main__":
    url = URL_TEMPLATE.format(convert(ARTIST), convert(TITLE))
    print("Retrieving text from", url, "...")
    try:
        content = urllib.request.urlopen(url, timeout=5).read().decode()
        soup = BeautifulSoup(content)
        print("Text found, parsing...")
        data = soup.find(id="songLyricsDiv").text
        print("*" * 30, "TEXT", "*" * 30)
        print(data)
    except urllib.error.URLError as e:
        print(e)