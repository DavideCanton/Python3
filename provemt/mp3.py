from random import random
from multiprocessing import Process, Manager, Lock, Semaphore, current_process
import time


class ActivePool(object):
    def __init__(self):
        super(ActivePool, self).__init__()
        self.mgr = Manager()
        self.active = self.mgr.list()
        self.lock = Lock()

    def __getstate__(self):
        d = self.__dict__.copy()
        del d["mgr"]
        return d

    def makeActive(self, name):
        with self.lock:
            self.active.append(name)

    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)

    def __str__(self):
        with self.lock:
            return str(self.active)


def worker(sem, pool):
    name = current_process().name
    with sem:
        pool.makeActive(name)
        print('Now running:', pool)
        time.sleep(random())
        pool.makeInactive(name)

if __name__ == '__main__':
    pool = ActivePool()
    s = Semaphore(3)
    jobs = [Process(target=worker, name=str(i), args=(s, pool))
            for i in range(10)]

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()
        print('Now running:', pool)
