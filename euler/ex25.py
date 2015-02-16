__author__ = 'davide'


def fib():
    a = 1
    b = 1

    yield a
    while True:
        a, b = b, a + b
        yield a


def main():
    for i, n in enumerate(fib(), start=1):
        if len(str(n)) == 1000:
            print(i)
            break


if __name__ == "__main__":
    main()