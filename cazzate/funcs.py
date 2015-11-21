__author__ = 'Kami'

import operator


class Function:
    def __call__(self, *args):
        raise NotImplementedError

    def derive(self):
        raise NotImplementedError

    def norm(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = Constant(other)
        return other

    def __add__(self, other):
        other = self.norm(other)
        return Add(self, other)

    def __sub__(self, other):
        other = self.norm(other)
        return Sub(self, other)

    def __mul__(self, other):
        other = self.norm(other)
        return Mul(self, other)

    def is_leaf(self):
        return True


class Constant(Function):
    def __init__(self, val):
        self.val = val

    def __call__(self, _):
        return self.val

    def __str__(self):
        return str(self.val)

    def derive(self):
        return Constant(0)


class Variable(Function):
    def __init__(self, name='x'):
        self.name = name

    def __call__(self, val):
        return val

    def __str__(self):
        return self.name

    def derive(self):
        return Constant(1)


class BinOp(Function):
    def __init__(self, symbol, op, f1, f2):
        self.symbol = symbol
        self.op = op
        self.f1 = f1
        self.f2 = f2

    def is_leaf(self):
        return False

    def __call__(self, v):
        return self.op(self.f1(v), self.f2(v))

    def __str__(self):
        s1 = str(self.f1)
        if isinstance(self.f1, BinOp):
            s1 = "({})".format(s1)
        s2 = str(self.f2)
        if isinstance(self.f2, BinOp):
            s2 = "({})".format(s2)
        return "{} {} {}".format(s1, self.symbol, s2)


class Add(BinOp):
    def __init__(self, f1, f2):
        super(Add, self).__init__("+", operator.add, f1, f2)

    def derive(self):
        return self.f1.derive() + self.f2.derive()


class Sub(BinOp):
    def __init__(self, f1, f2):
        super(Sub, self).__init__("-", operator.sub, f1, f2)

    def derive(self):
        return self.f1.derive() - self.f2.derive()


class Mul(BinOp):
    def __init__(self, f1, f2):
        super(Mul, self).__init__("*", operator.mul, f1, f2)

    def derive(self):
        return self.f1 * self.f2.derive() + self.f2 * self.f1.derive()


def simplify(func):
    if func.is_leaf():
        return func

    if isinstance(func, BinOp):
        f1, f2 = func.f1, func.f2
        if isinstance(f1, Constant) and isinstance(f2, Constant):
            return Constant(func.op(f1.val, f2.val))
        elif isinstance(func, Add) and isinstance(f1, Constant) and f1.val == 0:
            return simplify(f2)
        elif isinstance(func, Add) and isinstance(f2, Constant) and f2.val == 0:
            return simplify(f1)
        elif isinstance(func, Sub) and isinstance(f2, Constant) and f2.val == 0:
            return simplify(f1)
        elif isinstance(func, Mul) and isinstance(f1, Constant) and f1.val == 1:
            return simplify(f2)
        elif isinstance(func, Mul) and isinstance(f2, Constant) and f2.val == 1:
            return simplify(f1)
        else:
            func.f1 = simplify(func.f1)
            func.f2 = simplify(func.f2)

    return func


if __name__ == "__main__":
    x = Variable()
    y = x + 1
    z = x

    f = y * z
    f1 = f.derive()
    print(f)
    print(f1)

    # f = simplify(f)
    f1 = simplify(f1)
    print(f)
    print(f1)