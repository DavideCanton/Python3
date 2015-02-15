__author__ = 'davide'

__all__ = ["State", "AcceptState", "FSM"]


class State:
    def __init__(self, accept=False):
        self.accept = accept

    def next(self, input, fsm):
        return None


class AcceptState(State):
    def __init__(self):
        super(AcceptState, self).__init__(True)


class FSM:
    def __init__(self, start, states=None):
        if states is not None:
            self.__dict__.update(states)
        self._start = start

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def runAll(self, input):
        self.current = self[self._start]
        for i in input:
            if self.current is None:
                return False
            self.current = self.current.next(i, self)
        return False if self.current is None else self.current.accept
