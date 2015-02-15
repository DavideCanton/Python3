__author__ = 'davide'

import asyncio
from random import randint
from math import exp


@asyncio.coroutine
def compute(n):
    print("Calcolo exp({})".format(n))
    yield from asyncio.sleep(randint(1, 5))
    res = exp(n)
    print("exp({}) = {}".format(n, res))
    return res


@asyncio.coroutine
def calcola(lista):
    task_list = [asyncio.Task(compute(x)) for x in lista]
    acc = 0
    for task in task_list:
        acc += yield from task
    return acc


@asyncio.coroutine
def main():
    elems = list(range(2))
    res = yield from calcola(elems)
    print(res)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    assert isinstance(loop, asyncio.AbstractEventLoop)
    loop.set_debug(True)
    loop.run_until_complete(main())