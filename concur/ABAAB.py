import contextlib
import threading
import io

from concur import KamiSemaphore


class A(threading.Thread):
    def __init__(self, semA, semB, mutex):
        threading.Thread.__init__(self)
        self.setName("A")
        self.semA = semA
        self.semB = semB
        self.mutex = mutex

    def run(self):
        self.semA.acquire()
        with self.mutex:
            print("A", end="")
        self.semB.release()


class B(threading.Thread):
    def __init__(self, semA, semB, mutex):
        threading.Thread.__init__(self)
        self.setName("B")
        self.semA = semA
        self.semB = semB
        self.mutex = mutex

    def run(self):
        self.semB.acquire(2)
        with self.mutex:
            print("B", end="")
        self.semA.release(2)


output = io.StringIO()

with contextlib.redirect_stdout(output):
    semA = KamiSemaphore.KamiSemaphoreT(1)
    semB = KamiSemaphore.KamiSemaphoreT(1)
    mutex = threading.Lock()
    threads = ([A(semA, semB, mutex) for i in range(3)] +
               [B(semA, semB, mutex) for j in range(2)])
    for t in threads:
        t.start()
    for t in threads:
        t.join()

result = output.getvalue()
if result == "ABAAB":
    print("OK")
else:
    print("NO: {}".format(result))
