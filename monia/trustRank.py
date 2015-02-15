import csv
from operator import itemgetter
import numpy as np
from collections import defaultdict, Counter
from scipy.sparse import dok_matrix
from scipy.sparse.sparsetools import csr_scale_columns

try:
    import oracle
except ImportError:
    from trustRank import oracle


def parser_file(file_in):
    with open(file_in, "r", newline="") as in_file:
        reader = csv.reader(in_file, delimiter=";")

        # Salta la riga corrsipondente all'header del file
        iter_reader = iter(reader)
        next(iter_reader)
        dim = 700000
        U = dok_matrix((dim, dim))
        T = dok_matrix((dim, dim))
        dim = 0
        in_neighbor_role = defaultdict(Counter)
        for row in iter_reader:
            if len(row) != 0:
                source, target, role = map(int, row)
                dim = max(dim, source, target)
                U[source, target] = 1.
                T[target, source] = 1.
                in_neighbor_role[target][role] += 1
        dim += 1
        U = U.tocsr()[:dim, :dim]
        T = T.tocsr()[:dim, :dim]

        in_degree = U.sum(axis=0)
        in_degree[in_degree == 0] = 1
        in_degree = 1.0 / in_degree
        in_degree = np.array(in_degree)[0]

        csr_scale_columns(U.shape[0], U.shape[1], U.indptr,
                          U.indices, U.data, in_degree)

        out_degree = T.sum(axis=0)
        out_degree[out_degree == 0] = 1
        out_degree = 1.0 / out_degree
        out_degree = np.array(out_degree)[0]

        csr_scale_columns(T.shape[0], T.shape[1], T.indptr,
                          T.indices, T.data, out_degree)
    return T, U, dim, in_neighbor_role


def select_seed(U, n, decay_factor, num_interations):
    s = np.ones(n)
    for _ in range(num_interations):
        s = decay_factor * U.dot(s) + (1 - decay_factor) / n
    return s


def rank(s):
    return [pair[0] for pair in sorted(list(enumerate(s)), key=itemgetter(1),
                                       reverse=True)]


def compute_trustrank(T, U, num_pages, limit_oracle, decay_factor_t,
                      decay_factor_u, num_interations_t, num_interations_u, in_neighbor_roles):
    s = select_seed(U, n, decay_factor_u, num_interations_u)
    sigma = np.array(rank(s))
    d = np.zeros(num_pages)
    oracle_vec = np.frompyfunc(oracle.oracle_max_master, 1, 1)
    indexes = np.where(oracle_vec([in_neighbor_roles[user] for user in sigma[:limit_oracle]]))[0]
    d[sigma[indexes]] = 1
    d /= d.sum()
    trust = d
    for _ in range(num_interations_t):
        trust = decay_factor_t * T.dot(trust) + (1 - decay_factor_t) * d
    return trust


if __name__ == '__main__':
    file_in = r"advogato/gni"
    t, u, n, in_neighbor = parser_file(file_in)
    trust = compute_trustrank(t, u, n, 6, 0.85, 0.85, 20, 20, in_neighbor)
    print(trust)