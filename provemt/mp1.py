from multiprocessing import Process, current_process
from os import getpid


def w(num):
    n = current_process().name
    print("Worker", num, ", pid =", getpid(), " name =", n)

if __name__ == '__main__':
    for i in range(10):
        Process(target=w, args=[i]).start()
