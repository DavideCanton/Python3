import contextlib
import threading
import io

from concur import KamiSemaphore


class A(threading.Thread):
    def __init__(self, semA, semB, mutex):
        threading.Thread.__init__(self)
        self.semA = semA
        self.semB = semB
        self.mutex = mutex

    def run(self):
        self.semA.acquire(2)
        with self.mutex:
            print("A", end="")
        self.semB.release(2)


class B(threading.Thread):
    def __init__(self, semA, semB, mutex):
        threading.Thread.__init__(self)
        self.semA = semA
        self.semB = semB
        self.mutex = mutex

    def run(self):
        self.semB.acquire()
        with self.mutex:
            print("B", end="")
        self.semA.release()


output = io.StringIO()
with contextlib.redirect_stdout(output):
    semA = KamiSemaphore.KamiSemaphoreT(5)
    semB = KamiSemaphore.KamiSemaphoreT(-3)
    par = {"semA": semA, "semB": semB, "mutex": threading.Lock()}
    threads = [A(**par) for i in range(3)] + [B(**par) for j in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

result = output.getvalue()
if result == "AABABB":
    print("OK")
else:
    print("NO: {}".format(result))
