import string
from pyIA2.logic import Parser
from pyIA2.sat import wsat_solve
from pyIA2.reductions import buildFormulaIS
from multiprocessing import Manager, Process, current_process,\
    Event, RLock
from random import choice


def solve(formula, ret, ev, lock):
    name = current_process().name
    print("Process", name, "started")
    iterations = 1000
    sol = []
    ok = lambda sol: len(sol) >= 3
    for _ in range(iterations):
        if ok(sol):
            with lock:
                if not ev.is_set():
                    ret.extend([var.name for var in sol])
                    ev.set()
                    break
        sol = wsat_solve(formula)


if __name__ == '__main__':
    nt = 4
    chars = string.ascii_lowercase
    s = set()
    while len(s) < 5:
        a = choice(chars)
        b = choice(chars)
        if a != b:
            s.add(a + b)
    edges = "|".join(s)

    # edges = "ab|bc|bd|ae|be|ac|ce"
    edges = [tuple(e) for e in edges.split("|")]
    formula = buildFormulaIS(edges)
    formula = Parser().build_formula(formula)
    # print(" ^ ".join(map(str, clauses)))

    m = Manager()
    sol = m.list()
    ev = Event()
    lock = RLock()

    jobs = [Process(target=solve, args=(formula, sol, ev, lock))
            for _ in range(nt)]
    all_ended = lambda jobs: all(map(lambda j: not j.is_alive, jobs))

    for j in jobs:
        j.start()

    while True:
        res = ev.wait(1)
        if res or all_ended(jobs):
            break

    if res:
        print(sol)
    else:
        print("No solution found")

    for j in jobs:
        j.terminate()
