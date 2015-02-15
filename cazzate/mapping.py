import random
import string
import itertools as it

__author__ = 'Kami'


class MappingError(Exception):
    pass


class Mapping:
    """
    Mapping type, a kind of dict (but not a subclass of dict!)
    that maps a key to a value. Repeated inserts of the same
    key have no effect.

    N.B. if a key is added and the generator is exhausted,
    MappingError is raised.
    """

    def __init__(self, iterable=None, gen=None):
        """
        Creates a Mapping object, iterable is the
        iterable that has to be added, while gen is an
        iterator that returns consecutive values for added keys.
        """
        if gen is None:
            gen = it.count()
        self.gen = gen
        self.data = {}
        self.update(iterable)

    def update(self, iterable):
        """
        Inserts all the elements in iterable.
        Raises MappingError if internal
        generator is exhausted.
        """
        for elem in iterable:
            self.insert(elem)

    def insert(self, elem):
        """
        Inserts elem in the Mapping.
        Raises MappingError if internal
        generator is exhausted.
        """
        try:
            if elem not in self.data:
                val = next(self.gen)
                self.data[elem] = val
        except StopIteration:
            raise MappingError("Provided iterator exhausted")

    def __iter__(self):
        """
        Iterator over keys.
        """
        yield from self.data

    def __getitem__(self, item):
        """
        Returns the mapping value of item.
        """
        return self.data[item]

    def items(self):
        """
        Iterator yielding pairs (key,value).
        """
        yield from self.data.items()

    def __len__(self):
        """
        Size of mapping
        """
        return len(self.data)


def test():
    from collections import OrderedDict

    #s = "".join(random.choice(string.ascii_lowercase) for _ in range(random.randint(3, 40)))
    #print("Mapping of", s)
    with open("D:/07 The Divided Heart - 2 Cut.mp3", "rb") as f:
        s = f.read()
    uniques = list(OrderedDict.fromkeys(s))

    m = Mapping(s)
    for k, v in m.items():
        print(k, "=>", v)

    values = list(map(m.__getitem__, uniques))
    assert values == sorted(values)


if __name__ == "__main__":
    test()