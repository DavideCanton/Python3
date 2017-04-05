import fractions
import itertools as it
import math


def main():
    nums = list(range(1, 10)) * 4

    perms = ([1 for n in range(0, 40, 3)]
             + [2 for n in range(1, 40, 3)]
             + [3 for n in range(2, 40, 3)])

    den = math.factorial(40) // math.factorial(4) ** 10
    tot = fractions.Fraction()

    for i in range(1, len(perms)):
        s = 0
        n = math.factorial(len(nums) - i)
        for comb in it.combinations(perms, i):
            d = math.factorial(4) ** 7
            for j in range(1, 4):
                d += math.factorial(4 - comb.count(i))
            s += n // d
        tot += fractions.Fraction((-1) ** (i + 1) * s, den)

    print(tot)


if __name__ == "__main__":
    main()
