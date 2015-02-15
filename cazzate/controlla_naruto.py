__author__ = 'Kami'

import requests
from bs4 import BeautifulSoup
import re
from datetime import date

MONTHS = dict(zip(["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio",
                   "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"], range(1, 13)))


def request_page_content(page_id):
    data = {"t": page_id}
    headers = {"user-agent": "Chrome/3"}
    u = requests.get("http://archive.forumcommunity.net/", params=data, headers=headers)
    return u.text


def parse_episode_list_page(text):
    s = BeautifulSoup(text)
    for t in s.select('img'):
        if "alt" in t.attrs and t.attrs["alt"] == "new":
            t = t.previous_sibling.previous_sibling
            if t:
                text2 = request_page_content(t.attrs["href"][3:])
                parse_episode_page(text2)


def parse_episode_page(text):
    months = "(?:{})".format("|".join(MONTHS.keys()))
    giorno_regex = re.compile(r'(\d+) ({}) (\d+)'.format(months), re.IGNORECASE)
    match = giorno_regex.search(text)
    if match:
        d, m, y = [match.group(i) for i in (1, 2, 3)]
        m = MONTHS[m]
        d, y = map(int, [d, y])
        episode_date = date(y, m, d)
        if episode_date > date.today():
            print("L'episodio uscira' il", episode_date.strftime("%d/%m/%Y"), ":(")
        else:
            print("L'episodio e' uscito il", episode_date.strftime("%d/%m/%Y"), ":)")
    else:
        raise ValueError("No!")


if __name__ == "__main__":
    text = request_page_content("55609519")
    parse_episode_list_page(text)
