__author__ = 'davide'

from pyIA2.logic import Rule, Variable, _generateSubsets, ImplyFormula, Formula

if __name__ == "__main__":
    l = [Variable(s) for s in "abcd"]
    a, b, c, d = l
    r = Rule(head=[a, b])
    r2 = Rule(head=[c], body_pos=[a])
    r3 = Rule(head=[a, d], body_pos=[b, c])
    r4 = Rule(head=[b], body_pos=[d])
    v = {a, b, c, d}
    i = ImplyFormula(vars=v, rules=[r, r2, r3, r4])
    print(i)
    print(i.disj_form)
    print()
    for m in _generateSubsets([a, b, c, d]):
        print(m, "->", i.satisfied(m))
    for m in i.models:
        print(m)
    print("")
    for m in i.stable_models:
        print(m)