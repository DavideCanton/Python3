__author__ = 'davide'

import igraph

if __name__ == "__main__":
    N = 10
    M = 20
    ind = [1, 1, 2, 2, 6, 3, 3, 0, 0, 2]
    outd = [2, 1, 0, 4, 0, 3, 2, 2, 5, 1]

    g = igraph.Graph.Degree_Sequence(ind, outd, "no_multiple")
    g.vs["label"] = [str(i) for i in range(N)]

    igraph.plot(g)