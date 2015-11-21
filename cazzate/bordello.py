f2 = lambda l, k: list(filter(lambda s: s == s[::-1], map(lambda i: l[i:i + k], range(0, len(l) - k))))


def main():
    l = "abaaaa"
    print(f2(l, 3))


if __name__ == "__main__":
    main()
