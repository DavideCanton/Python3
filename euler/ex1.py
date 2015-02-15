# coding=utf-8

"""
Calcolare la somma dei numeri multipli di 3 o 5 minori di 1000.
"""

__author__ = 'davide'

import numpy as np


# Mettiamo in evidenza d in tutti i multipli di d minori di n
# otteniamo d + 2d + 3d + ... = d (1+2+...)
# il massimo è (n-1) // d = p, quindi d(1+...+p) = d * p * (p+1) / 2
def mult_sum(n, d):
    p = (n - 1) // d
    return d * p * (p + 1) // 2


def ex1(n=1000):
    return mult_sum(n, 3) + mult_sum(n, 5) - mult_sum(n, 15)

if __name__ == "__main__":
    print(ex1())
