__author__ = 'davide'

import time
import multiprocessing as mp

def father(p):
    print("Il padre invia")
    p.send(1)
    p.send(2)
    print("Il padre aspetta")
    print(p.recv())
    print("Il padre termina")


def son(p):
    print("Il figlio parte")
    v1 = p.recv()
    v2 = p.recv()
    print("Il figlio calcola")
    time.sleep(5)
    p.send(v1 + v2)
    print("Il figlio termina")

if __name__ == "__main__":
    (p1, p2) = mp.Pipe()

    f = mp.Process(target=father, args=(p1,))
    s = mp.Process(target=son, args=(p2,))

    f.start()
    s.start()

    f.join()
    s.join()