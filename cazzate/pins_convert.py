__author__ = 'Kami'

import json

import bs4

PATH = r"C:\Users\Kami\Google Drive\pins\Pin Evolution Table.html"
DST = r"C:\Users\Kami\Google Drive\pins\Pin Evolution Table.json"

if __name__ == "__main__":
    content = open(PATH).read()
    soup = bs4.BeautifulSoup(content)

    iterator = iter(soup.find_all("tr"))
    next(iterator)

    objs = []

    for row in iterator:
        tds = row.find_all("td")

        objs.append({"brand": tds[0].a.text.strip(),
                     "id_1": tds[2].a.text.strip(),
                     "name_1": tds[3].text.strip(),
                     "ev_type": tds[4].b.text.strip(),
                     "id_2": tds[6].a.text.strip(),
                     "name_2": tds[7].text.strip()})

    with open(DST, "w") as dst:
        json.dump(objs, dst)
