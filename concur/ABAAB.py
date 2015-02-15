from threading import Thread, Lock
from KamiSemaphore import *


class A(Thread):
    def __init__(self, semA, semB, mutex):
        Thread.__init__(self)
        self.semA = semA
        self.semB = semB
        self.mutex = mutex

    def run(self):
        self.semA.acquire()
        with self.mutex:
            print("A", end="")
        self.semB.release()


class B(Thread):
    def __init__(self, semA, semB, mutex):
        Thread.__init__(self)
        self.semA = semA
        self.semB = semB
        self.mutex = mutex

    def run(self):
        self.semB.acquire(2)
        with self.mutex:
            print("B", end="")
        self.semA.release(2)


import sys
from io import StringIO
output = StringIO()
sys.stdout = output
semA = KamiSemaphoreT(1)
semB = KamiSemaphoreT(1)
mutex = Lock()
threads = ([A(semA, semB, mutex) for _ in range(3)] +
           [B(semA, semB, mutex) for _ in range(2)])
for t in threads:
    t.start()
for t in threads:
    t.join()
sys.stdout = sys.__stdout__
result = output.getvalue()
if result == "ABAAB":
    print("OK")
else:
    print("NO: {}".format(result))
