__author__ = 'Kami'

import asyncio
import random


async def a():
    await b()

async def b():
    await a()


async def main():
    await a()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
