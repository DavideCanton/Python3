__author__ = 'Davide'

from roba_coro.utils import SystemCall


class GetTid(SystemCall):
    def handle(self):
        self.task.sendval = self.task.tid
        self.sched._schedule(self.task)


class NewTask(SystemCall):
    def __init__(self, target):
        super().__init__()
        self.target = target

    def handle(self):
        tid = self.sched.new(self.target)
        self.task.sendval = tid
        self.sched._schedule(self.task)


class KillTask(SystemCall):
    def __init__(self, tid):
        super().__init__()
        self.tid = tid

    def handle(self):
        task = self.sched.task_map[self.tid]
        if task:
            task.target.close()
            self.task.sendval = True
        else:
            self.task.sendval = False
        self.sched._schedule(self.task)


class WaitTask(SystemCall):
    def __init__(self, tid):
        super().__init__()
        self.tid = tid

    def handle(self):
        res = self.sched._wait_for_exit(self.task, self.tid)
        self.task.sendval = res
        if not res:
            self.sched._schedule(self.task)


class ReadWait(SystemCall):
    def __init__(self, f):
        super().__init__()
        self.f = f

    def handle(self):
        fd = self.f.fileno()
        self.sched._wait_for_read(self.task, fd)


class WriteWait(SystemCall):
    def __init__(self, f):
        super().__init__()
        self.f = f

    def handle(self):
        fd = self.f.fileno()
        self.sched._wait_for_write(self.task, fd)