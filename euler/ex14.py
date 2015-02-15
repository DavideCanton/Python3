__author__ = 'Kami'


def collatz(n):
    length = 0
    while n > 1:
        length += 1
        if n & 1:
            n = 3 * n + 1
        else:
            n >>= 1
    return length


if __name__ == "__main__":
    lenghts = list(enumerate((collatz(i)
                              for i in range(1, 1000001)),
                             start=1))
    print(max(lenghts, key=lambda t: t[1]))