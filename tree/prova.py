from tree import BinaryTree
import random
import collections
from functools import total_ordering


@total_ordering
class Data(collections.namedtuple("Data", "key, value")):
    def __eq__(self, other):
        return self.key == other.key

    def __lt__(self, other):
        return self.key < other.key


l = [Data(key=n, value=str(n)) for n in range(20)]
random.shuffle(l)
print(l)
tree = BinaryTree.buildTree(*l)
print(list(tree.visit()))
k = random.randint(0, 20)
sk = tree.searchKey(Data(key=k, value=""),
                    key=lambda x: getattr(x, "key"), use=True)
s = tree._search(Data(key=k, value=""))
print(sk == s)
