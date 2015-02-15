import itertools as it
from multiprocessing import Pool


class InvalidState(Exception):
    pass


def enabled(state, incr):
    for s, i in zip(state, incr[0]):
        if i < 0 and s < -i:
            return False
    return True


def execute(processes, initial, increments, log=True):
    state = initial[:]
    processes2 = processes[:]
    progress = []
    if log:
        print(" ", state)
    while sum(processes2) > 0:
        enabledProcesses = list(enabled(state, incr) for incr in increments)
        enabledNum = sum(enabledProcesses)
        if enabledNum == 0:
            raise InvalidState("No process enabled")
        elif enabledNum > 1:
            compressed = it.compress(range(len(state)), enabledProcesses)
            names = ", ".join(chr(ord("A") + index) for index in compressed)
            raise InvalidState("More than 1 enabled: " + str(names))
        index = enabledProcesses.index(True)
        state = [s + i + j for s, i, j in zip(state, *increments[index])]
        progress.append(chr(ord("A") + index))
        processes2[index] -= 1
        if log:
            print(chr(ord("A") + index), state)
    if len(progress) < sum(processes):
        raise InvalidState("Some processes have not finished yet")
    return "".join(progress)


def split(iterable, n):
    l = list(zip(*[iter(iterable)] * n))
    itl = iter(l)
    return [(next(itl), next(itl)) for _ in range(len(l) // 2)]


def simulate(processes, semaphores, max_threshold, max_drain, target):
    for initial in it.product(range(max_threshold + 1), repeat=semaphores):
        if sum(initial) == 0:
            continue
        repeat = semaphores * len(processes) * 2
        prod = it.product(range(-max_drain, max_drain + 1), repeat=repeat)
        for incrementsL in prod:
            try:
                if (all(i < 0 for i in incrementsL) or
                    all(i == 0 for i in incrementsL) or
                    all(i > 0 for i in incrementsL)):
                    continue
                print("Trying {} and {}".format(initial, incrementsL))
                inc = split(incrementsL, semaphores)
                res = execute(processes, initial, inc, log=False)
                if res == target:
                    print(initial)
                    print(incrementsL)
                    return True
            except:
                pass


def simulateInitial(initial, processes, semaphores,
                    max_drain, target):
    repeat = semaphores * len(processes) * 2
    prod = it.product(range(-max_drain, max_drain + 1), repeat=repeat)
    for incrementsL in prod:
        try:
            if (all(i < 0 for i in incrementsL) or
                all(i == 0 for i in incrementsL) or
                all(i > 0 for i in incrementsL)):
                continue
            # print("Trying {} and {}".format(initial, incrementsL))
            inc = split(incrementsL, semaphores)
            res = execute(processes, initial, inc, log=False)
            if res == target:
                print(initial)
                print(incrementsL)
                return True
        except:
            pass


def tryfind(initial=None):
    p = Pool(20)
    rl = []
    for s in range(1, 5):
        print("Provo con {} semafori".format(s))
        if initial is None:
            rl.append(p.apply_async(simulate, ([3, 2], s, 3, 3, "ABAAB")))
        else:
            rl.append(p.apply_async(simulateInitial,
                                    (initial, [3, 2], s, 2, "ABAAB")))
    for r in rl:
        if r.get():
            p.terminate()
            break

if __name__ == '__main__':
    tryfind(initial=[2, 0])
