import random

limit = random.randint(1, 100)
mod = random.randint(2, 10)
print("Limit: {}\nMod: {}".format(limit, mod))
d = {i: i % mod for i in range(limit)}
r = {i: {k for k in d if d[k] == i} for i in range(mod)}
for x in r:
    print(x, r[x])
