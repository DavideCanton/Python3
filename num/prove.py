__author__ = 'davide'

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

if __name__ == "__main__":
    u = np.r_[0:1:0.01]
    v = np.r_[0:1:0.01]

    c = np.dstack(np.meshgrid(u, v)).reshape((-1, 2))
    c = c[c.sum(axis=1) <= 1]

    x, y = np.hsplit(c, [1])
    x = x.ravel()
    y = y.ravel()
    z = -x - y + 1

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z, "-")
    plt.show()