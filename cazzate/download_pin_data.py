from pandas import json

__author__ = 'Davide'

from multiprocessing.pool import Pool
import pathlib
import requests
from bs4 import BeautifulSoup


def process(out_dir, url_template, n):
    if n < 10:
        n = "00" + str(n)
    elif n < 100:
        n = "0" + str(n)
    else:
        n = str(n)
    url = url_template.format(n)
    with (out_dir / ("d_" + n + ".txt")).open("w", encoding="utf8") as fo:
        data = None
        while True:
            try:
                data = requests.get(url)
                break
            except requests.ConnectionError:
                print("{}> Retrying...".format(n))
        soup = BeautifulSoup(data.content)
        rows = soup.find("div", {'id': 'mw-content-text'}).table

        data_dict = {}
        for row in rows.findAll('tr'):
            try:
                h = row.th.text.strip()
                v = "|".join(row.td.text.strip().split("\n"))
                data_dict[h] = v
            except AttributeError:
                pass
        if 'Comments' in data_dict:
            del data_dict['Comments']
        if 'Damage @ATK=200' in data_dict:
            del data_dict['Damage @ATK=200']
        if 'Efficiency' in data_dict:
            del data_dict['Efficiency']
        json.dump(data_dict, fo, ensure_ascii=False)
    return n


def main():
    #needed = set(range(1, 305))
    needed = {215}

    out_dir = pathlib.Path("data")
    try:
        out_dir.mkdir()
    except FileExistsError:
        pass

    url_template = "http://twewy.wikia.com/wiki/Pin_{}"

    p = Pool(8)
    res = [p.apply_async(process, (out_dir, url_template, n))
           for n in needed]
    for r in res:
        print("Terminato", r.get())
    p.close()
    p.join()


if __name__ == "__main__":
    main()