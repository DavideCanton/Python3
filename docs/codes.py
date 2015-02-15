__author__ = 'davide'

from math import floor, log2, ceil
import random


def encode_unary(x):
    return "1" * (x - 1) + "0"


def encode_binary(x, e=-1):
    bin_code = bin(x)[2:]
    if e < 0:
        return bin_code
    return bin_code.rjust(e, "0")


def encode_gamma(x):
    e = x.bit_length()
    d = x - 2 ** e
    p1 = encode_unary(e + 1)
    p2 = encode_binary(d, e) if e else ""
    return p1 + p2


def encode_delta(x):
    e = x.bit_length()
    d = x - 2 ** e
    p1 = encode_gamma(e + 1)
    p2 = encode_binary(d, e) if e else ""
    return p1 + p2


def encoder_golomb(b):
    e = ceil(log2(b))
    g = 2 ** e - b

    def encoder(x):
        x -= 1
        q, r = divmod(x, b)
        u1 = encode_unary(q + 1)
        if 0 <= r < g:
            u2 = encode_binary(r, e - 1)
        else:
            u2 = encode_binary(r + g, e)
        return u1 + u2

    return encoder


if __name__ == "__main__":
    def encode_with_factor(factor):
        encoder = encoder_golomb(factor)
        coded = "".join(encoder(n) for n in nums)
        print(coded)
        print(len(coded) / len(nums) / 8)

    N = 10
    NUMS = 5
    p = NUMS / N
    nums = [1, 3, 5, 7, 8]
    nums = [n - m for n, m in zip(nums[1:], nums)]
    print(nums)

    factor = ceil(- log2(2 - p) / log2(1 - p))
    print("Optimal factor:", factor)
    encode_with_factor(factor)
    for i in range(1, 10):
        encode_with_factor(i)