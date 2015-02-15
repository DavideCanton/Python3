import threading as T
import multiprocessing as M


class KamiSemaphoreT:

    def __init__(self, value=1):
        self._permits = value
        self.waiting = T.Condition()

    def acquire(self, permits=1, blocking=True):
        with self.waiting:
            if not blocking and self._permits < permits:
                return False
            elif blocking:
                while self._permits < permits:
                    self.waiting.wait()
            self._permits -= permits
        return True

    __enter__ = acquire

    def __exit__(self, type, value, traceback):
        self.release()

    def release(self, permits=1):
        with self.waiting:
            self._permits += permits
            if self._permits > 0:
                self.waiting.notifyAll()

    @property
    def permits(self):
        return self._permits


class KamiSemaphoreM:
    def __init__(self, value=1):
        self._permits = value
        self.waiting = M.Condition()

    def acquire(self, permits=1, blocking=True):
        with self.waiting:
            if not blocking and self._permits < permits:
                return False
            elif blocking:
                while self._permits < permits:
                    self.waiting.wait()
            self._permits -= permits
        return True

    __enter__ = acquire

    def __exit__(self, type, value, traceback):
        self.release()

    def release(self, permits=1):
        with self.waiting:
            self._permits += permits
            if self._permits > 0:
                self.waiting.notify_all()

    @property
    def permits(self):
        return self._permits


if __name__ == '__main__':
    m = KamiSemaphoreM(-3)
    print(m.permits)
    m.release(10)
    m.acquire(permits=2)
    print(m.permits)
