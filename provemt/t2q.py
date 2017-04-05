import threading
from multiprocessing import cpu_count
import time
import collections
import random


class Queue:
    def __init__(self):
        self.q = collections.deque()
        # implicit lock in the condition
        self.empty = threading.Condition()

    def get(self):
        with self.empty:
            self.empty.wait_for(lambda: self.q)
            v = self.q.pop()
            return v

    def put(self, el):
        with self.empty:
            self.q.appendleft(el)
            self.empty.notifyAll()


class Worker(threading.Thread):
    def __init__(self, task_q, result_q):
        super().__init__()
        self.task_q = task_q
        self.result_q = result_q

    def run(self):
        while True:
            task = self.task_q.get()
            if task is None:
                # print(self.name, "is exiting!")
                break
            # print("Doing some work in", self.name, ":", task)
            answer = task()
            self.result_q.put(answer)


class Task:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self):
        time.sleep(random.randint(1, 5))
        return "{} * {} = {}".format(self.a, self.b,
                                     self.a * self.b)

    def __str__(self):
        return "{} * {}".format(self.a, self.b)


if __name__ == '__main__':
    task_q = Queue()
    result_q = Queue()
    nc = cpu_count() * 2
    print("Creo", nc, "consumatori")
    # nt = randint(10, 20)
    nt = 200
    print("Creo", nt, "task")

    for i in range(nc):
        p = Worker(task_q, result_q)
        p.start()

    for i in range(nt):
        task_q.put(Task(i, i))

    for i in range(nc):
        task_q.put(None)

    for i in range(nt):
        res = result_q.get()
        print("Risultato:", res)
