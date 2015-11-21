import itertools as it

__author__ = 'Davide'


def main():
    cnt = 0
    tot = 0
    nums = list(range(1, 4)) * 2
    for p in it.permutations(nums):
        print(p, end="")
        if p[0] == 1 or p[1] == 2 or p[3] == 1 or p[4] == 2:
            cnt += 1
            print(" OK")
        else:
            print()
        tot += 1

    print(cnt)
    print(tot)


if __name__ == "__main__":
    main()
