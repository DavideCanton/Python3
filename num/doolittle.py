__author__ = 'davide'

import scipy as sp
import scipy.linalg as la


def doolittle(A):
    n = A.shape[0]
    L = sp.zeros_like(A)
    U = sp.zeros_like(A)
    for i in range(n):
        L[i, i] = 1
        for k in range(i, n):
            U[i, k] = A[i, k] - sp.dot(L[i, :i], U[:i, k])
        for k in range(i + 1, n):
            L[k, i] = (A[k, i] - sp.dot(L[k, :i], U[:i, i])) / U[i, i]
    return L, U


def valid(A):
    n, m = A.shape
    if n != m:
        raise ValueError("Matrice non quadrata")
    for i in range(1, n + 1):
        if la.det(A[:i, :i]) == 0:
            raise ValueError("No!")


if __name__ == "__main__":
    A = sp.array([[-2, 4, 8], [-4, 18, -16], [-6, 2, -20]])
    valid(A)
    L, U = doolittle(A)
    print(L)
    print(U)
    print(A)
    print(sp.dot(L, U))