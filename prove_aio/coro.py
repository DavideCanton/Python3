import asyncio


async def waiting(r):
    print("hello from waiting -", r)
    await asyncio.sleep(2)
    print("bye from waiting -", r)
    return r


async def serial():
    a = await waiting(1)
    b = await waiting(2)
    c = await waiting(a + b)

    print(c)


async def parallel():
    a, b = await asyncio.gather(waiting(1), waiting(2))
    c = await waiting(a + b)

    print(c)


async def postponed():
    a = await waiting(1)
    b = await waiting(2)
    await waiting('after')
    return a + b


async def pp_caller():
    r = await postponed()
    print("got result from postponed -", r)
    await asyncio.sleep(3)
    loop.stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    print("-- serial")
    loop.run_until_complete(serial())

    print("-- parallel")
    loop.run_until_complete(parallel())

    print("-- postponed")
    loop.run_until_complete(pp_caller())

    loop.close()
