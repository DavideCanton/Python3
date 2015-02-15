__author__ = 'davide'

import asyncio
import datetime
import time
import random


def p(i):
    time.sleep(2)
    print("{}> Ciao {}!".format(datetime.datetime.now(), i))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    for i in range(10):
        r = random.randint(1, 10)
        print("Calling {} at {}".format(i, r))
        loop.call_later(r, p, i)
    loop.run_forever()
