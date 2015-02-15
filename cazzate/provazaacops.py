class C:
    def __init__(self, *a, **k):
        self.__dict__.update(("_{}".format(i), x) for i, x in enumerate(a))
        self.__dict__.update(k)

    def __str__(self):
        return "({})".format(self.__dict__)


c = C(3, a='a', b=1)
print(c)
