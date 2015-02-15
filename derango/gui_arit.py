__author__ = 'davide'

from collections import Counter, OrderedDict
from decimal import Decimal as D

try:
    from tkinter import Tk, StringVar
    from tkinter import ttk
    from tkinter.messagebox import showerror
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest
    from Tkinter import Tk, StringVar
    import Tkinter as ttk
    from tkMessageBox import showerror


def encode(s, p):
    s += "\0"
    a, b = D("0"), D("1")
    for ch in s:
        bk = a
        for k in p:
            ak, bk = bk, bk + p[k] * (b - a)
            if k == ch:
                a, b = ak, bk
                break
    return a, b


def encode_step(s, p):
    s += "@"
    a, b = D("0"), D("1")
    for ch in s:
        bk = a
        for k in p:
            ak, bk = bk, bk + p[k] * (b - a)
            yield k, ak, bk
            if k == ch:
                a, b = ak, bk
                break
        yield None
    yield "@", a, b


def decode(n, p):
    a, b = D("0"), D("1")
    s = []
    while True:
        bk = a
        for k in p:
            ak = bk
            bk = ak + p[k] * (b - a)
            if ak <= n <= bk:
                if k == "\0":
                    return "".join(s)
                s.append(k)
                a, b = ak, bk
                break


def computeP(s):
    s += "\0"
    l = D(len(s))
    c = Counter(s)
    p = {k: D(v) / l for k, v in c.items()}
    return p


def getN(a, b):
    sa, sb = map(str, (a, b))
    flag = False
    l = ["0", "."]
    i = 0
    for i, t in enumerate(zip_longest(sa[2:], sb[2:], fillvalue="0")):
        ia, ib = map(int, t)
        l.append(str(ia))
        if flag:
            break
        if ia != ib:
            flag = True
    d = D("".join(l))
    d += D("." + "0" * i + "1")
    return d


class Show_error_in_messagebox:
    def __init__(self, exctypes, aft_raise=False):
        self.exctypes = exctypes
        self.aft_raise = aft_raise

    def __call__(self, func):
        def wrapper(*a, **k):
            try:
                ret = func(*a, **k)
            except Exception as e:
                if type(e) in self.exctypes:
                    showerror("Errore", str(e))
                    if self.aft_raise:
                        raise e
                    else:
                        return
                else:
                    raise e
            return ret

        return wrapper


class GUI(Tk):
    def __init__(self, master=None):
        Tk.__init__(self, master)
        self.title("Codifica Aritmetica")
        ttk.Label(self, text="Stringa:").grid(row=0, column=0)
        self.s = StringVar()
        ttk.Entry(self, textvariable=self.s).grid(row=0, column=1)
        for i, c in enumerate("abcz"):
            ttk.Label(self, text="P[{}]".format(c)).grid(row=i + 1, column=0)
            e = ttk.Entry(self)
            setattr(self, "p{}".format(i), e)
            e.grid(row=i + 1, column=1)
        ttk.Button(self, text="Calcola!", command=self.compute).grid(row=5, columnspan=2)
        self.res = ttk.Label(self)
        self.res.grid(row=6, columnspan=2)

    @Show_error_in_messagebox([Exception])
    def compute(self, *e):
        try:
            o = OrderedDict()
            o["a"] = D(self.p0.get())
            o["b"] = D(self.p1.get())
            o["c"] = D(self.p2.get())
            if o["c"] == D("0"):
                del o["c"]
            o["@"] = D(self.p3.get())
            st = self.s.get()
            if st[-1] != "@":
                self.s.set(self.s.get() + "@")
            l = []
            for t in encode_step(st, o):
                if t is None:
                    l.append("-------------------")
                else:
                    k, ak, bk = t
                    l.append("{} -> [{}, {}[".format(k, ak, bk))
            self.res.configure(text="\n".join(l))
        except:
            raise Exception("Errore nei dati!")


if __name__ == "__main__":
    g = GUI()
    g.mainloop()
