import sys
import itertools as it
import re
import numpy as np
import work.advogato.mapping as mapping

__author__ = 'Kami'


def dirich_pr(A, mu, v):
    A = A.copy()
    N = A.shape[0]
    x = np.ones_like(v) / N
    omega = mu / (A.sum(axis=0) + mu)

    A *= (1 - omega)[:, np.newaxis]

    while True:
        x_old = x
        x = A.dot(x) + np.dot(x, omega) / N
        if np.allclose(x_old, x):
            break
    return x

def pagerank(A, alpha, v):
    """pagerank originale -> OK """
    #A = A.copy()
    N = A.shape[0]

    x = np.ones_like(v) / N
    while True:
        x_old = x
        x = alpha * np.dot(A, x) + (1 - alpha) * v
        if np.allclose(x_old, x):
            break
    return x


def load_matrix(file_dataset, filter_revoked=True):
    print("Filling matrix...")
    A = np.zeros((10000, 10000))
    pattern = re.compile("[\s,]")
    dim = 0
    mapp = mapping.Mapping()

    for line in file_dataset:
        line = line.strip()
        if filter_revoked and line.endswith("#"):
            continue
        users = pattern.split(line)[:2]
        mapp.update(users)
        src, dst = map(mapp.__getitem__, users)
        dim = max(dim, src, dst)
        if src != dst:
            A[dst, src] = 1

    dim += 1
    A.resize((dim, dim))

    print(dim)

    print("Removing sinks and scaling...")

    for i in range(dim):
        column = A[:, i].view()
        if np.count_nonzero(column) == 0:
            A[:, i] = 1 / dim
        else:
            A[:, i] /= column.sum()

    return A


if __name__ == "__main__":
    DATASET_PATH = r"C:\Users\Kami\Documents\workspace\Python3\work\advogato\complete-dataset"
    DST_PATH = r"C:\Users\Kami\Documents\workspace\Python3\work\advogato\adv_pr\pr_res.txt"

    print("Reading matrix...")
    with open(DATASET_PATH) as f:
        A = load_matrix(f, filter_revoked=True)
    print("Read matrix!")

    v = np.ones(A.shape[0])
    v /= v.sum()

    # for mu in range(5, 200, 15):
    #     print("mu =", mu)
    #     print("Started DR...")
    #     x = dirich_pr(A, mu, v)
    #     print("Ended DR!")
    #
    #     print("Writing...")
    #     with open(DST_PATH.format(mu), "w") as f:
    #         for user in range(A.shape[0]):
    #             print(user, x[user], file=f)
    #     print("End Writing!")

    print("Started PR...")
    x = pagerank(A, 0.85, v)
    print("Ended PR!")

    print("Writing...")
    with open(DST_PATH, "w") as f:
        for user in range(A.shape[0]):
            print(user, x[user], file=f)
    print("End Writing!")