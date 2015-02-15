__author__ = 'Kami'

import asyncio


@asyncio.coroutine
def process(n):
    yield from asyncio.sleep(1.0)
    return n + 1


@asyncio.coroutine
def main():
    p = [process(i) for i in range(10)]
    n = yield from asyncio.gather(*p)
    print(n)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

