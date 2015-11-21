import multiprocessing

__author__ = 'Davide'


def f():
    print(multiprocessing.current_process().pid)
    while True:
        pass


if __name__ == "__main__":
    while True:
        p = multiprocessing.Process(target=f)
        p.start()
        p.join()
        print("Killed")
