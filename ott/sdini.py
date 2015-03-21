import ott.setcovering
import random
import numpy as np

I = random.randint(50, 100)

elem = set(range(I))

subsets = [set(random.sample(elem, random.randint(1, I)))
           for _ in range(random.randint(10, 20))]
costs = np.random.randint(10, 30, len(subsets))

print("Elements =", I)
print()
if I <= 1000:
    print("Subsets =")
    print()
    for s in subsets:
        print(s)
    print()
print("Costs =", costs)
print()

print(ott.setcovering.chvatal(elem, costs, subsets))
print()
print(ott.setcovering.aggMolt(elem, costs, subsets))
