from tree.tree import BinaryTree
from pyIA2.searching import *
import random


max = 100
content = list(range(1, max + 1))
random.shuffle(content)
t = BinaryTree.buildTree(*content)
t.printTree()
h = lambda n: 0
goals = dict(t.leaves())
min_depth = min(goals.values())
print("Root: {}, Leaves: {}".format(t.root, goals))
is_goal = lambda n: n in goals
root = t.root

pa = a_star(root, is_goal, h, t.children)
print("A*:\t{}".format(pa))

pdr = depth_first(root, is_goal, t.children)
print("DFR:\t{}".format(pdr))

pdl = depth_first(root, is_goal, t.children, left=True)
print("DFL:\t{}".format(pdl))

pb = breadth_first(root, is_goal, t.children)
print("BF:\t{}".format(pb))

pid = iterative_deepening(root, is_goal, t.children)
print("ID:\t{}".format(pid))

pib = iterative_broadening(root, is_goal, t.children, 2)
print("IB:\t{}".format(pib))

pida = ida_star(root, is_goal, h, t.children)
print("IDA*:\t{}".format(pida))
