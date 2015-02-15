__author__ = 'Davide'

import matplotlib.pyplot as plt
from scipy.sparse import lil_matrix
import numpy as np
import igraph

if __name__ == "__main__":
    graph = igraph.Graph.Erdos_Renyi(n=200, m=500, directed=True)

    matrix = lil_matrix(graph.get_adjacency().data)

    plt.spy(matrix, marker=".", markersize=2)
    plt.show()