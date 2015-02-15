from functools import total_ordering
from heapq import heappop, heappush
from collections import Counter
import itertools as it
import os
from math import log


@total_ordering
class Node:
    def __init__(self, freq, val=None, left=None, right=None):
        self.freq = freq
        self.val = val
        self.left = left
        self.right = right

    __lt__ = lambda self, v: self.freq < v.freq
    __eq__ = lambda self, v: self.freq == v.freq

    def __repr__(self):
        return "({}, {})".format(self.val, self.freq)


class Decoder:
    def __init__(self, tree):
        self.tree = tree
        self.reset()

    def advance(self, bit):
        if self.root.val is None:
            if bit == "0":
                self.root = self.root.left
            else:
                self.root = self.root.right

    def get(self):
        return self.root.val

    def reset(self):
        self.root = self.tree


def build_encoding(c):
    h = []
    for k in c:
        heappush(h, Node(c[k], k))
    while len(h) > 1:
        n1, n2 = heappop(h), heappop(h)
        f = n1.freq + n2.freq
        n = Node(freq=f, left=n1, right=n2)
        heappush(h, n)
    return _visit(h[0]), h[0]


def _visit(node):
    d = {}
    _visitNode(node, "", d)
    kl = list(d.keys())
    if len(kl) == 1:
        d[kl[0]] = "0"
    return d


def _visitNode(node, code, d):
    if node.val is not None:
        d[node.val] = code
    else:
        if node.left:
            _visitNode(node.left, code + "0", d)
        if node.right:
            _visitNode(node.right, code + "1", d)


def encode(encoding, text):
    d, _ = encoding
    return "".join(d[c] for c in text)


def decode(encoding, text):
    s = []
    d = Decoder(encoding[1])
    for c in text:
        d.advance(c)
        if d.get():
            s.append(d.get())
            d.reset()
    return "".join(s)


def write_to_file(coded, f):
    buffer = []
    for c in coded:
        buffer.append(c)
        if len(buffer) == 8:
            c = chr(int("".join(buffer), 2))
            f.write(bytes(c, "latin_1"))
            del buffer[:]
    l = len(buffer)
    buffer.extend(["0"] * (8 - l))
    i = chr(int("".join(buffer), 2))
    f.write(bytes(i, "latin_1"))
    f.write(bytes(chr(l), "latin_1"))


def read_from_file(f):
    s = []
    while True:
        b = f.read(1)
        if not b:
            break
        binary = bin(ord(b))[2:]
        s.append("{:>08}".format(binary))
    try:
        l = s[-2]
        c = int(s[-1], 2)
        del s[-2:]
        if c:
            s.append(l[:c])
    except ValueError:
        pass
    return "".join(s)


def main():
    path1 = r"D:\readme.txt"
    path2 = r"D:\readme2.txt"

    l1 = os.path.getsize(path1)
    with open(path1, encoding="latin-1") as f:
        s = "".join(f.readlines())
    e = build_encoding(Counter(s))

    for k, v in e[0].items():
        if k.isprintable():
            print("{}\t|\t{}".format(k, v))
        else:
            print("[{}]\t|\t{}".format(ord(k), v))

    encoded = encode(e, s)
    # print(encoded)
    print(len(encoded) / 8)

    with open(path2, "wb") as f2:
        write_to_file(encoded, f2)

    l2 = os.path.getsize(path2)
    print("Compression ratio: {}/{} = {:1.2f}%".format(l2, l1,
                                                       l2 / l1 * 100))

    with open(path2, "rb") as f2:
        r = read_from_file(f2)

    # print(r)
    print(len(r) / 8)
    decoded = decode(e, r)
    print(s == decoded)
    # print(decoded)


def g():
    d = {'0': .1, '1': .9}
    d2 = {i + j + k + l: round(d[i] * d[j] * d[k] * d[l], 5)
          for i, j, k, l in it.product(d.keys(), repeat=4)}

    print(d2)
    e = build_encoding(d2)[0]

    s = 0
    for k, v in e.items():
        s += d2[k] * len(e[k])
    print(s)

    h = 0
    log2 = lambda x: log(x) / log(2)
    for k, v in d2.items():
        h += d2[k] * log2(1 / d2[k])
    print(h)

if __name__ == "__main__":
    s = input("Stringa> ")
    e = build_encoding(Counter(s))
    encoded = encode(e, s)
    for k, v in e[0].items():
        print("{}:\t{}".format(k, v))
    print(encoded)
    d = decode(e, encoded)
    print(s == d)
    print("Ratio: {}/{}={}%".format(len(encoded), len(s) * 8,
                             len(encoded) / len(s) / 8 * 100))