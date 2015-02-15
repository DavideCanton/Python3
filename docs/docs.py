__author__ = 'davide'

import pathlib
import string
import math
from collections import defaultdict

def compute_inverse(fdt, docs, terms):
    ft = defaultdict(int)

    for t in terms:
        for d in docs:
            ft[t] += fdt[t, d]

    return ft


def index():
    terms = set()
    docs = []
    fdt = defaultdict(int)

    folder = pathlib.Path("D:/documenti prova")
    for fp in folder.glob("*.txt"):
        docs.append(fp.name)
        with fp.open() as f:
            for line in f:
                for word in line.split():
                    word = word.strip(string.punctuation)
                    if word:
                        terms.add(word)
                        fdt[word, fp.name] += 1

    ft = compute_inverse(fdt, docs, terms)
    return terms, docs, fdt, ft


if __name__ == "__main__":
    terms, docs, fdt, ft = index()
    N = len(docs)
    q = input("Query>")

    f1 = lambda t: math.log(1 + N / ft[t]) if ft[t] > 0 else 0
    f2 = lambda t, d: 1 + math.log(fdt[t, d]) if fdt[t, d] > 0 else 0

    qt = [x.strip(string.punctuation) for x in q.split()]
    wqt = {t: f1(t) for t in qt}
    wdt = {(t, d): f2(t, d) for t in qt for d in docs}
    wd = math.sqrt(sum(wdt[t, d] ** 2 for t in qt for d in docs))

    if abs(wd) < 1E-10:
        sd = []
    else:
        sd = [(d, sum(wdt[t, d] * wqt[t] for t in qt for d in docs) / wd )
              for d in docs]
    sd.sort(key=lambda t: -t[1])
    for el in sd:
        print(el)

    for t in qt:
        for d in docs:
            print("{},{} => {}".format(t, d, fdt[t, d]))