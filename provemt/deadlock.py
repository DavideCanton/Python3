import random
import threading

import time


def f(i, mutexA, mutexB):
    if i % 2 == 0:
        with mutexA:
            with mutexB:
                print("Ciao", i)
                time.sleep(random.randint(1, 3))
    else:
        with mutexB:
            with mutexA:
                print("Ciao", i)
                time.sleep(random.randint(1, 3))


if __name__ == "__main__":
    mutexA = threading.BoundedSemaphore(1)
    mutexB = threading.BoundedSemaphore(1)
    for i in range(10):
        threading.Thread(target=f, args=[i, mutexA, mutexB]).start()
