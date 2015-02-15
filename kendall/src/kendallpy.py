import numpy as np


def kendall_distance(a, b):
    n = len(a)
    ia = np.argsort(a)
    ib = np.argsort(b)

    c = 0
    d = 0
    for i in range(n):
        for j in range(i + 1, n):
            if ia[i] > ia[j] and ib[i] < ib[j]:
                d += 1
            elif ia[i] < ia[j] and ib[i] > ib[j]:
                d += 1
            else:
                c += 1

    return (c - d) / (c + d)


def main():
    a = np.arange(0, 20)
    np.random.shuffle(a)
    b = np.array(a)
    np.random.shuffle(b)

    print(a)
    print(b)

    print(kendall_distance(a, b))


if __name__ == "__main__":
    main()