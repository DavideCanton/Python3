__author__ = 'davide'

import numpy as np
from numpy.lib.stride_tricks import as_strided


def _sum_sq_diff(input_image, template, valid_mask):
    """This function performs template matching. The metric used is Sum of
    Squared Difference (SSD). The input taken is the template who's match is
    to be found in image.
    Parameters
    ---------
    input_image : array, np.float
        Input image of shape (M, N)
    template : array, np.float
        (window, window) Template who's match is to be found in input_image.
    valid_mask : array, np.float
        (window, window), governs differences which are to be considered for
        SSD computation. Masks out the unknown or unfilled pixels and gives a
        higher weightage to the center pixel, decreasing as the distance from
        center pixel increases.
    Returns
    ------
    ssd : array, np.float
        (M - window +1, N - window + 1) The desired SSD values for all
        positions in the input_image
    """
    total_weight = valid_mask.sum()
    window_size = template.shape
    y = as_strided(input_image,
                   shape=((input_image.shape[0] - window_size[0] + 1,
                           input_image.shape[1] - window_size[1] + 1,) +
                          window_size),
                   strides=input_image.strides * 2)
    ssd = np.einsum('ijkl, kl, kl->ij', y, template, valid_mask,
                    dtype=np.float)
    # Refer to the comment below for the explanation
    ssd *= - 2
    ssd += np.einsum('ijkl, ijkl, kl->ij', y, y, valid_mask)
    ssd += np.einsum('ij, ij, ij', template, template, valid_mask)
    ssd /= total_weight

    min_template = np.unravel_index(ssd.argmin(), ssd.shape)
    return min_template


if __name__ == "__main__":
    img = np.random.random_integers(0, 3, (4, 4))
    print(img)

    template = np.ones(9).reshape(3, 3)
    valid_mask = template.copy()
    valid_mask[1, 1] = 10

    s = _sum_sq_diff(img, template, valid_mask)
    print(s)