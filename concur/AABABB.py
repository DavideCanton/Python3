from threading import Thread, Lock
from KamiSemaphore import KamiSemaphoreT as KSem


class A(Thread):
    def __init__(self, semA, semB, mutex):
        Thread.__init__(self)
        self.semA = semA
        self.semB = semB
        self.mutex = mutex

    def run(self):
        self.semA.acquire(2)
        with self.mutex:
            print("A", end="")
        self.semB.release(2)


class B(Thread):
    def __init__(self, semA, semB, mutex):
        Thread.__init__(self)
        self.semA = semA
        self.semB = semB
        self.mutex = mutex

    def run(self):
        self.semB.acquire()
        with self.mutex:
            print("B", end="")
        self.semA.release()


import sys
from io import StringIO
output = StringIO()
sys.stdout = output
semA = KSem(5)
semB = KSem(-3)
par = {"semA": semA, "semB": semB, "mutex": Lock()}
threads = ([A(**par) for _ in range(3)] +
           [B(**par) for _ in range(3)])
for t in threads:
    t.start()
for t in threads:
    t.join()
sys.stdout = sys.__stdout__
result = output.getvalue()
if result == "AABABB":
    print("OK")
else:
    print("NO: {}".format(result))
