from gof.fsm import AcceptState, FSM, State

__author__ = 'davide'


class P(AcceptState):
    def next(self, i, fsm):
        return fsm.d if i == "1" else self


class D(State):
    def next(self, i, fsm):
        return fsm.p if i == "0" else self


f = FSM('p')
f.p = P()
f.d = D()
e = f.runAll("101010101011010")
print(e)
