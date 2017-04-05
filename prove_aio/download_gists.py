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


async def get(*args, **kwargs):
    response = await aiohttp.request('GET', *args, **kwargs)
    return await response.read()


def extract_links(content):
    soup = bs4.BeautifulSoup(content)
    spans = soup.find_all("span", class_="creator")
    for span in spans:
        links = span.find_all('a')
        yield links[1]['href']


async def download_gist(link, sem):
    async with sem:
        content = await get(URL + link)

    soup = bs4.BeautifulSoup(content)
    link = soup.find("a", text="Raw")['href']

    filename = link.split("/")[-1]
    path = pathlib.Path(DIR, filename)

    print("Downloading", filename, "...")
    async with sem:
        resp = await aiohttp.request('GET', URL + link)

    with path.open("wb") as fo:
        while True:
            async with sem:
                chunk = await resp.content.read(CHUNK_SIZE)
            if not chunk:
                break
            fo.write(chunk)


async def process_page(page, sem, user):
    async with sem:
        content = await get(PAGE_URL.format(user, page))

    for link in extract_links(content):
        async with sem:
            await download_gist(link, sem)


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