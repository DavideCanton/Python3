__author__ = 'davide'

import asyncio
import random
import math


async def compute(n):
    print("Calcolo exp({})".format(n))
    await asyncio.sleep(random.randint(1, 5))
    res = math.exp(n)
    print("exp({}) = {}".format(n, res))
    return res


async def calcola(lista):
    task_list = [compute(x) for x in lista]
    res = await asyncio.gather(*task_list)
    return sum(res)


async def main():
    elems = list(range(5))
    res = await calcola(elems)
    print(res)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
