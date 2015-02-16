__author__ = 'Kami'

import numpy as np
from numpy.lib.stride_tricks import as_strided
from numba import double, jit
from timeit import default_timer as timer

double_m = double[:, :]


@jit(double_m(double_m, double_m))
def filter2d(image, filt):
    M, N = image.shape
    Mf, Nf = filt.shape
    Mf2 = Mf // 2
    Nf2 = Nf // 2
    result = np.zeros_like(image)
    for i in range(Mf2, M - Mf2):
        for j in range(Nf2, N - Nf2):
            num = 0.0
            for ii in range(Mf):
                for jj in range(Nf):
                    num += (filt[Mf - 1 - ii, Nf - 1 - jj] *
                            image[i - Mf2 + ii, j - Nf2 + jj])
            result[i, j] = num
    return result


def filter2d_np(image, filt):
    M, N = image.shape
    Mf, Nf = filt.shape
    Mf2, Nf2 = Mf // 2, Nf // 2

    sq_view = as_strided(image,
                         shape=(M - Mf + 1, N - Nf + 1,
                                Mf, Nf),
                         strides=image.strides * 2)

    filt = filt[::-1, ::-1]
    out = np.zeros_like(image)

    np.einsum("ijkl, kl -> ij", sq_view, filt,
              out=out[:M - Mf + 1, :N - Nf + 1])

    out = np.roll(out, Mf2, axis=0)
    out = np.roll(out, Nf2, axis=1)

    out[-Mf2:, :] = 0
    out[:, -Nf2:] = 0

    return out


if __name__ == "__main__":
    image = np.random.random((500, 500))
    filt = np.random.random((90, 90))

    start = timer()
    res1 = filter2d(image, filt)
    print("1st:", timer() - start)
    start = timer()
    res2 = filter2d_np(image, filt)
    print("2st:", timer() - start)

    assert np.allclose(res1, res2)