__author__ = 'davide'

import numpy as np

a = np.zeros(10, dtype=[('x', np.int32), ('y', np.int32), ('z', np.int32),
                        ('name', "S1")])

a['x'] = np.r_[1:11]
a['y'] = np.r_[11:21]
a['z'] = np.r_[21:31]
a['name'] = list("abcdefghij")

print(a)
print(a['x'])