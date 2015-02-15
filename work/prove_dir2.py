__author__ = 'Kami'

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


a = np.array([1, 5, 10])
b = np.random.dirichlet(a, size=3000)
x, y, z = np.transpose(b)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, "bo")
plt.show()