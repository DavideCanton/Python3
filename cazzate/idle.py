__author__ = 'Davide'

from multiprocessing import Process, current_process


def f():
    print(current_process().pid)
    while True:
        pass


if __name__ == "__main__":
    while True:
        p = Process(target=f)
        p.start()
        p.join()
        print("Killed")