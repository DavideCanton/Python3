import math


def is_sq1(x):
    s = math.floor(math.sqrt(x))
    return s * s == x


def is_sq2(x):
    for i in range(2, x + 1):
        last = 0
        while x % i == 0:
            x /= i
            last += 1

        if last % 2 != 0:
            return False

    return True


if __name__ == "__main__":
    for x in range(1, 1000):
        sq_1 = is_sq1(x)
        sq_2 = is_sq2(x)
        assert sq_1 == sq_2
