__author__ = 'Davide'


class SingletonMeta(type):
    _cache = {}

    def __call__(cls, *args, **kwargs):
        name = cls.__name__
        if name not in SingletonMeta._cache:
            inst = type.__call__(cls, *args, **kwargs)
            SingletonMeta._cache[name] = inst
        return SingletonMeta._cache[name]


class C(metaclass=SingletonMeta):
    def __init__(self, n):
        self.n = n

    def __str__(self):
        return "{}".format(self.n)


if __name__ == "__main__":
    c = C(3)
    print(c)
    d = C(4)
    print(d)
    print(c is d)