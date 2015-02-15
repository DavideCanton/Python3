def completeAddSub(cl):
    hasadd = hasattr(cl, "__add__")
    hassub = hasattr(cl, "__sub__")
    hasneg = hasattr(cl, "__neg__")
    if not hasneg:
        raise TypeError("class doesn't declare __neg__")
    if not hasadd and not hassub:
        raise TypeError("class doesn't declare __add__ neither __sub__")
    if not hasadd:
        cl.__add__ = lambda c1, c2: c1 - (-c2)
    elif not hassub:
        cl.__sub__ = lambda c1, c2: c1 + (-c2)
    return cl


@completeAddSub
class Punto(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, p2):
        return Punto(self.x + p2.x, self.y + p2.y)

    def __str__(self):
        return "<{:0.2f},{:0.2f}>".format(self.x, self.y)

    def __neg__(self):
        return Punto(-self.x, -self.y)


if __name__ == '__main__':
    p = Punto(4, 3)
    p2 = Punto(5, 2)
    print("P1:", p)
    print("P2:", p2)
    print("Somma:", p + p2)
    print("Opposto di P1:", -p)
    print("Differenza:", p - p2)
