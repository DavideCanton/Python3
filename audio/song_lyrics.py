__author__ = 'davide'

import urllib.error
import urllib.parse
import urllib.request
import re

ARTIST = "Hammerfall"
TITLE = "One More Time"
URL_TEMPLATE = "http://www.songlyrics.com/{}/{}-lyrics/"


def convert(s):
    return urllib.parse.quote_plus("-".join(s.lower().split()))


def repl_function(group):
    char_code = group.group(1)
    return chr(int(char_code))

if __name__ == "__main__":
    url = URL_TEMPLATE.format(convert(ARTIST), convert(TITLE))
    print("Retrieving text from", url, "...")
    try:
        content = urllib.request.urlopen(url, timeout=5).read().decode()
        print("Text found, parsing...")
        regex = re.compile(r'<\s*p\s*id\s*=\s*"songLyricsDiv".*?>(.*?)</p>', re.DOTALL)
        # search for the text
        data = regex.search(content)
        if not data:
            exit("NO!")
        data = data.group(1)
        # remove <br/>
        data = re.sub(r"<br\s*?/?>", "", data)
        # replace HTML entities with characters
        data = re.sub(r"&#(\d+);", repl_function, data)
        print("*" * 30, "TEXT", "*" * 30)
        print(data)
    except urllib.error.URLError as e:
        print(e)