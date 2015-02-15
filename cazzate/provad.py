class Dec:
    def __init__(self, name, a):
        self.a = a
        self.name = name

    def __call__(self, func):
        instance = self

        def wr(self, *a, **kw):
            afunc = lambda *a, **kw: func(self, *a, **kw)
            return afunc(*a, **kw) + getattr(self, instance.name) - instance.a

        return wr


class C:
    def __init__(self, n):
        self.n = n

    @Dec("n", 10)
    def f(self, a, b):
        return a + b

c = C(3)
print(c.f(1, 2))  # stampa 1+2+3-10
