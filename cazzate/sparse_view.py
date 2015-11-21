__author__ = 'Davide'

from PIL import Image
import igraph

if __name__ == "__main__":
    n = 100
    m = 500
    g = igraph.Graph.Static_Power_Law(n, m, exponent_in=2.5,
                                      exponent_out=2)

    img = Image.new("L", (n, n), "white")
    pix = img.load()

    m = g.get_adjacency()

    for i in range(n):
        for j in range(n):
            pix[j, i] = int((1 - m[i, j]) * 255)

    img.show()

    igraph.plot(g)