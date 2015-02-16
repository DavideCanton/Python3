__author__ = 'davide'


def val(e):
    return sum(ord(c) - ord('A') + 1 for c in e)


def main():
    with open("extras/p022_names.txt") as f:
        l = [s.strip('"') for s in f.readline().split(",")]
    l.sort()

    s = 0
    for i, e in enumerate(l, start=1):
        s += val(e) * i
    print(s)


if __name__ == "__main__":
    main()