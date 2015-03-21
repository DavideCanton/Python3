__author__ = 'Davide'

from roba_coro.utils import Scheduler
from roba_coro.syscalls import *
import itertools as it


def foo(limit):
    tid = yield GetTid()
    if limit < 0:
        g = it.count()
    else:
        g = range(limit)
    for i in g:
        print(tid, "foo", i)
        yield


def main():
    t1 = yield NewTask(foo(-1))
    for i in range(10):
        yield
    yield KillTask(t1)

    t2 = yield NewTask(foo(10))
    yield WaitTask(t2)


if __name__ == "__main__":
    s = Scheduler()
    s.execute(main())