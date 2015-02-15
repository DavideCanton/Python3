__author__ = 'davide'

import fsm

# automa di a+bc*

class Q0(fsm.State):
    def next(self, input, fsm):
        if input == 'a':
            return fsm.q1
        else:
            return None


class Q1(fsm.State):
    def next(self, input, fsm):
        if input == 'a':
            return self
        elif input == 'b':
            return fsm.q2
        else:
            return None


class Q2(fsm.AcceptState):
    def next(self, input, _):
        if input == 'c':
            return self
        else:
            return None


if __name__ == "__main__":
    f = fsm.FSM('q0')
    f.q0 = Q0()
    f.q1 = Q1()
    f.q2 = Q2()
    while True:
        s = input(">>")
        if not s:
            break
        print(f.runAll(s))
