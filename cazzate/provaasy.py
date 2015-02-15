import asyncio
import random


@asyncio.coroutine
def factorial(name, number):
    f = 1
    print("Task %s: Compute factorial(%s)..." % (name, number))
    for i in range(2, number + 1):
        yield from asyncio.sleep(random.randint(1, 10) / 10)
        f *= i
    print("Task %s: factorial(%s) = %s" % (name, number, f))


tasks = [asyncio.Task(factorial(str(n), n)) for n in range(100)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
loop.close()