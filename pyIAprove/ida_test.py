from tree.tree import BinaryTree
import random
from pyIA2.searching import ida_star
import sys


def test(max, debug=False, seed=0):
    content = list(range(1, max + 1))
    if seed == 0:
        seed = random.randint(0, sys.maxsize)
    if debug:
        print("Seed: {}".format(seed))
    random.seed(seed)
    random.shuffle(content)
    tree = BinaryTree.buildTree(*content)
    if debug:
        tree.printTree()

    h = lambda: 0
    goals = dict(tree.leaves())
    min_depth = min(goals.values())
    min_leaves = [l for l in goals.keys() if goals[l] == min_depth]
    if debug:
        print("Root: {}, Leaves: {}".format(tree.root, goals))
        print("Min leaves: {}".format(min_leaves))
    goal = lambda n: n in goals

    p, v, info = ida_star(tree.root, goal, h, tree.children)
    if debug:
        print(p)
        print(v)
        print(info)
    return p[-1] in min_leaves, seed

if __name__ == '__main__':
    ok, seed = True, -1
    num = 1000
    while ok:
        ok, seed = test(num)
    test(num, True, seed)
