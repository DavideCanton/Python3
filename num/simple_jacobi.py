__author__ = 'davide'

import numpy as np

ITERATION_LIMIT = 1000

# initialize the matrix
A = np.array([[10., -1., 2., 0.],
              [-1., 11., -1., 3.],
              [2., -1., 10., -1.],
              [0.0, 3., -1., 8.]])
# initialize the RHS vector
b = np.array([6., 25., -11., 15.])

# prints the system
print("System:")
for i in range(A.shape[0]):
    row = ["{}*x{}".format(A[i, j], j + 1) for j in range(A.shape[1])]
    print(" + ".join(row), "=", b[i])
print()

x = np.zeros_like(b)
diag = np.diag(A)

for it_count in range(ITERATION_LIMIT):
    print("Current solution:", x)

    s = np.dot(A, x) - (diag * x)
    x_new = (b - s) / diag

    if np.allclose(x, x_new, atol=1e-16, rtol=0):
        break

    x = x_new

print("Solution:")
print(x)
error = np.dot(A, x) - b
print("Error:")
print(error)
