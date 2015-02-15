__author__ = 'Kami'

from scipy.sparse import *
import numpy as np

if __name__ == "__main__":
    types = [np.uint8, np.uint16, np.uint32, np.uint64,
             np.int8, np.int16, np.int32, np.int64,
             np.float16, np.float32, np.float64]
    for t in types:
        print(t)
        P = dok_matrix((3, 3), dtype=t)
        P[0, 0] = 1
        P = P.tocsr()
        print(P.getcol(0))