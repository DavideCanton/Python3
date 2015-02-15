import asyncio
import os
import pathlib

import aiohttp
import bs4


__author__ = 'Davide Canton'

DIR = "gists"
USER = "DavideCanton"
CHUNK_SIZE = 1 << 16
MAX_CONNECTIONS = 20
MAX_PAGE = 30

URL = "https://gist.github.com"
PAGE_URL = "https://gist.github.com/{}?page={}"


@asyncio.coroutine
def get(*args, **kwargs):
    response = yield from aiohttp.request('GET', *args, **kwargs)
    return (yield from response.read())


def extract_links(content):
    soup = bs4.BeautifulSoup(content)
    spans = soup.find_all("span", class_="creator")
    for span in spans:
        links = span.find_all('a')
        yield links[1]['href']


@asyncio.coroutine
def download_gist(link, sem):
    with (yield from sem):
        content = yield from get(URL + link)

    soup = bs4.BeautifulSoup(content)
    link = soup.find("a", text="Raw")['href']

    filename = link.split("/")[-1]
    path = pathlib.Path(DIR, filename)

    print("Downloading", filename, "...")
    with (yield from sem):
        resp = yield from aiohttp.request('GET', URL + link)

    with path.open("wb") as fo:
        while True:
            with (yield from sem):
                chunk = yield from resp.content.read(CHUNK_SIZE)
            if not chunk:
                break
            fo.write(chunk)


@asyncio.coroutine
def process_page(page, sem, user):
    with (yield from sem):
        content = yield from get(PAGE_URL.format(user, page))

    for link in extract_links(content):
        with (yield from sem):
            yield from download_gist(link, sem)


def main():
    try:
        os.makedirs(DIR)
    except OSError:
        pass

    sem = asyncio.Semaphore(MAX_CONNECTIONS)
    loop = asyncio.get_event_loop()

    tasks = [process_page(i, sem, USER) for i in range(1, MAX_PAGE)]
    res = asyncio.wait(tasks)

    loop.run_until_complete(res)


if __name__ == "__main__":
    main()