import select

__author__ = 'Davide'

from collections import deque


def coroutine(coro):
    def wrapper(*a, **kw):
        started_coro = coro(*a, **kw)
        next(started_coro)
        return started_coro

    return wrapper


class SystemCall:
    def __init__(self):
        self.task = None
        self.sched = None

    def handle(self):
        raise NotImplementedError


class Task:
    taskid = 0

    def __init__(self, target):
        self.tid = Task.taskid
        self.target = target
        self.sendval = None
        Task.taskid += 1

    def run(self):
        return self.target.send(self.sendval)


class Scheduler:
    def __init__(self):
        self.ready = deque()
        self.task_map = {}
        self.exit_waiting = {}
        self.read_waiting = {}
        self.write_waiting = {}

    def _iotask(self):
        while True:
            if self.ready:
                self._iopoll(0)
            else:
                self._iopoll(None)
            yield

    def _wait_for_read(self, task, fd):
        self.read_waiting[fd] = task

    def _wait_for_write(self, task, fd):
        self.write_waiting[fd] = task

    def _iopoll(self, timeout):
        if self.read_waiting or self.write_waiting:
            r, w, e = select.select(self.read_waiting, self.write_waiting, [],
                                    timeout)
            for fd in r:
                self._schedule(self.read_waiting.pop(fd))
            for fd in w:
                self._schedule(self.write_waiting.pop(fd))

    def execute(self, target):
        self.new(target)
        self.mainloop()

    def new(self, target):
        newtask = Task(target)
        self.task_map[newtask.tid] = newtask
        self._schedule(newtask)
        return newtask.tid

    def _schedule(self, task):
        self.ready.append(task)

    def _exit(self, task):
        del self.task_map[task.tid]
        for task in self.exit_waiting.pop(task.tid, []):
            self._schedule(task)

    def _wait_for_exit(self, task, wait_tid):
        if wait_tid in self.task_map:
            self.exit_waiting.setdefault(wait_tid, []).append(task)
            return True
        else:
            return False

    def mainloop(self):
        self.new(self._iotask())
        while self.task_map:
            task = self.ready.popleft()
            try:
                result = task.run()
                if isinstance(result, SystemCall):
                    result.task = task
                    result.sched = self
                    result.handle()
                    continue
            except StopIteration:
                self._exit(task)
                continue
            self._schedule(task)