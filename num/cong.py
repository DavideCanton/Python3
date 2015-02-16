__author__ = 'Kami'

diz = {}


def triangle_number(k):
    return k * (k + 1) // 2


T = [triangle_number(i) for i in range(2000)]
d = {n: [k % n for k in T] for n in range(3, 20, 2)}

for k in sorted(d.keys()):
    # print(str(k).rjust(2), sorted(set(range(k)) - set(d[k])))
    v = d[k]
    for x in range(10):
        assert (v[:k] == v[x * k:(x + 1) * k])
    print(str(k).rjust(2), d[k])