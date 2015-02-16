__author__ = 'davide'

import numpy as np
import numpy.linalg as l


def doolittle(a_matrix):
    n = a_matrix.shape[0]
    l_mat = np.eye(n)
    u_mat = np.zeros_like(a_matrix, dtype=np.float)

    for i in range(n):
        u_mat[i, :] = a_matrix[i, :] - l_mat[i, :i].dot(u_mat[:i, :])
        l_mat[:, i] = a_matrix[:, i] - l_mat[:, :i].dot(u_mat[:i, i])
        l_mat[:, i] /= u_mat[i, i]

    return np.tril(l_mat), np.triu(u_mat)


def valid(A):
    n, m = A.shape
    if n != m:
        raise ValueError("Matrice non quadrata")
    for i in range(1, n + 1):
        if l.det(A[:i, :i]) == 0:
            raise ValueError("No!")


def main():
    # A = np.array([[-2, 4, 8], [-4, 18, -16], [-6, 2, -20]])
    N = 5
    A = np.random.random_integers(-20, 20, (N, N)).astype(np.float64)
    valid(A)
    L, U = doolittle(A)
    print(L)
    print(U)
    print(np.allclose(A, L.dot(U)))


if __name__ == "__main__":
    main()