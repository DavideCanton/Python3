import itertools as it
from collections import defaultdict


class FuncDep:
    def __init__(self, left, right):
        """
        Creates a FuncDep.
        @param left: the left hand
        @type left: set[str]
        @param right: the right hand
        @type right: set[str]
        """
        if len(left) and len(right):
            self.left = set(left)
            self.right = set(right) - self.left
        else:
            raise ValueError("empty arg")

    def splitRight(self):
        """
        Yields the atoms in the right hand
        @return: an iterator
        """
        for elem in self.right:
            yield FuncDep(self.left, set(elem))

    def __add__(self, fd):
        """
        @type fd: FuncDep
        @return a funcdep
        """
        if fd.left != self.left:
            raise ValueError("!= left")
        return FuncDep(self.left, self.right | fd.right)

    def __repr__(self):
        strl = "".join(sorted(self.left))
        strr = "".join(sorted(self.right))
        return "{} -> {}".format(strl, strr)

    def copy(self):
        """
        @return: copy of self
        """
        return FuncDep(self.left, self.right)

    @property
    def atts(self):
        """
        @return: the attlist of self
        """
        return self.left | self.right

    def del_right(self, att):
        """
        @param att: the attribute to remove
        @type att: str
        """
        self.right.discard(att)

    def add_right(self, att):
        """
        @param att: the attribute to add
        @type att: str
        """
        self.right.add(att)


def closure_of(attrs, func_set):
    """
    Computes the closure of attrs in func_set
    @param attrs: the attrs
    @type attrs: set[str]
    @param func_set: the func_set
    @type func_set: set[FuncDep]
    @return:
    """
    func_set = set(func_set)
    closure = set(attrs)
    changed = True
    while changed:
        changed = False
        for fd in func_set:
            # contenuto
            if fd.left <= closure:
                # unione
                closure |= fd.right
                changed = True
                func_set.remove(fd)
                break
    return closure


def keys_of(attrlist, func_set):
    keys = []
    for key in subset_asc(attrlist, empty=False):
        closure = closure_of(key, func_set)
        if len(closure) == len(attrlist):
            for el in keys:
                if key >= el:
                    break
            else:
                keys.append(key)
                yield key


def subset_asc(myset, empty=True, full=True):
    if empty:
        yield set()
    for r in range(1, len(myset)):
        for subset in it.combinations(myset, r):
            yield set(subset)
    if full:
        yield set(myset)


def subset_desc(myset, empty=True, full=True):
    if full:
        yield myset
    for r in range(len(myset) - 1, 0, -1):
        for subset in it.combinations(myset, r):
            yield set(subset)
    if empty:
        yield set()


def simplify_left(func_set):
    result = func_set.copy()
    changed = True
    while changed:
        changed = False
        for fd in result.copy():
            if len(fd.left) == 1:
                continue
            result.remove(fd)
            for a in fd.left.copy():
                s = set(fd.left)
                s.remove(a)
                cl = closure_of(s, result)
                if a in cl:
                    fd = FuncDep(frozenset(s), fd.right)
                    result.add(fd)
                    changed = True
                    break
            else:
                result.add(fd)
    return result


def simplify_right(func_set):
    result = func_set.copy()
    for fd in func_set:
        for a in fd.right.copy():
            fd.del_right(a)
            cl = closure_of(fd.left, result)
            if a not in cl:
                fd.add_right(a)
    return result


def merge(func_set):
    fdm = defaultdict(set)
    for fd in func_set:
        fdm[frozenset(fd.left)] |= fd.right
    return {FuncDep(k, v) for (k, v) in fdm.items()}


def reduce_set(func_set):
    func_set = simplify_left(func_set)
    func_set = simplify_right(func_set)
    func_set = merge(func_set)
    return func_set


if __name__ == '__main__':
    f1 = FuncDep("A", "BC")
    f2 = FuncDep("B", "C")
    f3 = FuncDep("C", "A")
    func_set = {f1, f2, f3}
    atts = set().union(*[f.atts for f in func_set])
    atts = sorted(atts)
    print(list(keys_of(atts, func_set)))
    func_set = reduce_set(func_set)
    print(list(keys_of(atts, func_set)))