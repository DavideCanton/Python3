__author__ = 'Davide'

from multiprocessing.pool import Pool
import re
import pathlib
import requests
from bs4 import BeautifulSoup


def process(out_dir, url_template, n, c):
    if n < 10:
        n = "00" + str(n)
    elif n < 100:
        n = "0" + str(n)
    else:
        n = str(n)
    url = url_template.format(n)
    with (out_dir / ("pin_" + n + ("c" if c else "") + ".png")).open("wb") as fo:
        data = requests.get(url)
        soup = BeautifulSoup(data.content)
        img_url = soup.find("div", {'class': 'fullMedia'}).a['href']
        img_data = requests.get(img_url).content
        fo.write(img_data)


def main():
    files = list(pathlib.Path(
        r"C:\Users\Davide\AndroidStudioProjects\TwewyPins\app\src\main\res"
        r"\drawable").iterdir())

    not_needed = set()
    for p in files:
        g = re.search("\d+", p.name)
        if g:
            not_needed.add(int(g.group(0)))

    #not_needed = set()
    needed = set(range(1, 305)) - not_needed

    out_dir = pathlib.Path("imgs")
    try:
        out_dir.mkdir()
    except FileExistsError:
        pass

    url_template = "http://twewy.wikia.com/wiki/File:Pin_{}c.png"

    p = Pool(4)
    res = [p.apply_async(process, (out_dir, url_template, n, True))
           for n in needed]
    for r in res:
        r.get()
    p.close()
    p.join()


if __name__ == "__main__":
    main()