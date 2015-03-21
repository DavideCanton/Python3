import copy
import numpy as np


def check(subsets, elements):
    e = set().union(*subsets)
    if e != elements:
        res = e - elements or elements - e
        raise ValueError("Input not valid: {}".format(res))


def chvatal(elements, costs, subsets):
    """Chvatal's algorithm"""
    # check
    check(subsets, elements)
    elements = elements.copy()
    costs = np.array(costs)
    subsets = copy.deepcopy(subsets)

    # current solution
    sol = np.zeros(len(subsets), dtype='int')
    # big M for empty subsets
    M = costs.max() + 1
    s = np.array(list(map(len, subsets)))
    d = s.max()
    s[s == 0] = M

    while True:
        # compute subsets' value
        v = costs / s
        v[v < 0] = np.inf

        # minimum subset
        k = np.argmin(v)

        # set xk to 1
        sol[k] = 1
        # remove covered elements
        target = subsets[k]
        elements -= target

        # remove covered elements from subsets
        # (target subset will be set to empty set)
        for i, sets in enumerate(subsets):
            sets.difference_update(target)
            s[i] = len(sets) if sets else -1

        # end of algorithm
        if not elements:
            return (sol, np.dot(costs, sol),
                    (1 / np.arange(1, d + 1)).sum() - 1)

        # solution doesn't exist
        if not subsets:
            return None


def aggMolt(elements, costs, subsets):
    """Lambda adjustment algorithm"""
    check(subsets, elements)
    # setup lambda list, lambda cost and A matrix
    lambda_list = np.zeros(len(elements))
    lambda_cost = np.array(costs)
    A = np.zeros([len(subsets), len(elements)])
    for i, subset in enumerate(subsets):
        A[i, :].put(list(subset), 1)
    A = A.T
    zlr = 0
    x = np.zeros_like(lambda_cost)

    while True:
        x[lambda_cost <= 0] = 1
        # check if x is feasible
        x_covering = A[:, x != 0].sum(axis=1)

        if np.count_nonzero(x_covering) == len(elements):
            eps = np.dot(lambda_list, np.dot(A, x) - 1)
            return x, np.dot(costs, x), float(eps) / zlr

        # if not, search for the first element not present in solution
        h = np.argwhere(x_covering == 0)[0][0]

        # compute subsets that cover h
        jh = np.where(A[h] != 0)
        # compute delta
        delta = lambda_cost[jh].min()
        # increase lambda, decrease lambda cost
        lambda_list[h] += delta
        zlr += delta
        lambda_cost[jh] -= delta


if __name__ == '__main__':
    elem = set(range(5))

    subsets = [{1, 4}, {0, 1, 4}, {0, 3}, {0, 1, 3}, {4}, {0, 2, 3}, {1, 2}]

    print(chvatal(elem, [25, 22, 20, 18, 5, 14, 16], subsets))
    print(aggMolt(elem, [25, 22, 20, 18, 5, 14, 16], subsets))
