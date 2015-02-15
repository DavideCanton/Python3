import numpy as np
from scipy.sparse import dok_matrix
from scipy.sparse.sparsetools import csr_scale_rows
import csv


def compute_direct_trust(file_in):
    with open(file_in, "r", newline="") as in_file:
        reader = csv.reader(in_file, delimiter=";")
        iter_reader = iter(reader)
        next(iter_reader)
        dim = 700000
        T = dok_matrix((dim, dim))

        for row in iter_reader:
            if len(row) != 0:
                source, target, role = map(int, row)
                T[source, target] = (5 - role) / 4
                dim = max(source, target)
        dim += 1
        T = T.tocsr()[:dim, :dim]

        out_degree = T.sum(axis=1)
        out_degree[out_degree == 0] = 1
        out_degree = 1.0 / out_degree
        out_degree = np.array(out_degree)[0]
        csr_scale_rows(T.shape[0], T.shape[1], T.indptr,
                       T.indices, T.data, out_degree)

    return T


def get_ratio(M):
    """
    Calcola il rapporto entry non nulle / dimensione totale
    """
    if M is not None:
        return M.getnnz() / M.shape[0] / M.shape[1]
    return -1


def compute_trustWebRank(file_in, beta, threshold=1e-8):
    S = compute_direct_trust(file_in)
    T_old = S.copy()
    T = None
    it_count = 0
    while True:
        T = S + beta * S.dot(T_old)

        diff = abs(T - T_old).max()
        if diff < threshold:
            break

        T_old = T
        it_count += 1

        print("Iterazione {}, errore max {}...".format(it_count, diff))

    del S
    del T_old

    out_degree = T.sum(axis=1)
    out_degree[out_degree == 0] = 1
    out_degree = 1.0 / out_degree
    out_degree = np.array(out_degree)[0]
    csr_scale_rows(T.shape[0], T.shape[1], T.indptr,
                   T.indices, T.data, out_degree)

    return T, it_count


def write_res_to_file(T, out_file):
    n = T.shape[0]
    with open(out_file, "w") as fout:
        fout.write("Source Target Trust_Value\n")
        for i in range(n):
            for j in range(n):
                #Se si decommenta questa riga, scrive solo le entry non nulle
                #if T[i,j] == 0: continue
                #Se si decommenta questa invece, scrive solo quelle >= 10^-8
                #if T[i,j] < 1e-8: continue
                fout.write("{} {} {}\n".format(i, j, T[i, j]))


if __name__ == '__main__':
    file_in = r"complete_dataset_last_cert_mappato.txt"
    file_out = r"complete_dataset_last_cert_trustwebrank"
    T, it_count = compute_trustWebRank(file_in, 0.8)
    write_res_to_file(T, file_out)
