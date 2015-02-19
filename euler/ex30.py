__author__ = 'Davide'


def verify(n):
    return sum(int(d) ** 5 for d in str(n)) == n


def main():
    print(sum(n for n in range(2, 9 ** 5 * 20) if verify(n)))


if __name__ == "__main__":
    main()