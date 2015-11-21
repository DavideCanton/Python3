__author__ = 'Davide'


# prob models
def equiprob(n):
    return {i: 1 / (n + 1) for i in range(n + 1)}


def from_list(l):
    assert sum(l) == 1
    return dict(enumerate(l))


def wins(m1, m2):
    h1, f1 = m1
    h2, f2 = m2

    if h1 == h2 and f1 == f2:
        return 0

    goals_a = h1 + f2
    goals_b = h2 + f1
    if goals_a > goals_b:
        return 1
    if goals_a < goals_b:
        return -1
    goals_a = h1 + 2 * f2
    goals_b = h2 + 2 * f1
    if goals_a > goals_b:
        return 1
    if goals_a < goals_b:
        return -1
    return 0


def halves(tol=1e-8):
    res = {}
    cur = 0
    acc = 0
    val = 0.5
    while abs(acc - 1) > tol:
        res[cur] = val
        acc += val
        val /= 2
        cur += 1
    return res


if __name__ == "__main__":
    m1 = 1, 2

    d1 = halves(tol=1e-2)
    d2 = halves(tol=1e-2)

    w = []
    l = []
    p = []

    for i, p1 in d1.items():
        for j, p2 in d2.items():
            m2 = i, j

            # print("Andata: {}-{}".format(*m1))
            # print("Ritorno: {}-{}".format(*m2))

            r = wins(m1, m2)
            if r > 0:
                w.append((m2, p1 * p2))
            elif r < 0:
                l.append((m2, p1 * p2))
            else:
                p.append((m2, p1 * p2))

    w.sort(key=lambda t: -t[1])
    l.sort(key=lambda t: -t[1])
    p.sort(key=lambda t: -t[1])
    f = sum(a[1] for a in w + l + p)

    print("Risultati favorevoli:")
    for t in w:
        print("{}-{}: {}%".format(t[0][0], t[0][1], round(t[1] / f * 100, 2)))
    print("Risultati sfavorevoli:")
    for t in l:
        print("{}-{}: {}%".format(t[0][0], t[0][1], round(t[1] / f * 100, 2)))
    print("Risultati pareggio:")
    for t in p:
        print("{}-{}: {}%".format(t[0][0], t[0][1], round(t[1] / f * 100, 2)))

    print(f)