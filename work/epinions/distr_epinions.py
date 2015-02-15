__author__ = 'Kami'

from bisect import bisect
from datetime import date
from collections import defaultdict, namedtuple
import numpy as np


if __name__ == "__main__":
    dataset_path = r"U:\home\kami\Documenti\Ext_Epinions\user_rating.txt"
    out_path = r"epinions_in_neighbors.txt"

    to_date = lambda text: date(*(map(int, text.split("/"))))

    in_neighbors = defaultdict(list)
    vcount = 131828

    with open(dataset_path) as file_in:
        for line in file_in:
            _, dst, _, cur = line.split()
            cur_date = to_date(cur)
            pos = bisect(in_neighbors[dst], cur_date)
            in_neighbors[dst].insert(pos, cur_date)

    print("Read dataset.")

    at_least_one_in_neighbor = len(in_neighbors)
    one_in_neighbor = 0

    with open(out_path, "w") as out_file:
        print("Node_id GapMean GapStd Range", file=out_file)
        while in_neighbors:
            node, certs = in_neighbors.popitem()
            if len(certs) > 1:
                gaps = np.array([(b - a).days for a, b in zip(certs, certs[1:])])
                mean = np.mean(gaps)
                std = np.std(gaps)
                node_range = (certs[-1] - certs[0]).days
                print(node, mean, std, node_range, file=out_file)
            else:
                one_in_neighbor += 1

    print("End")
    print("Nodes with zero in-neighbors:", vcount - at_least_one_in_neighbor)
    print("Nodes with one in-neighbor:", one_in_neighbor)
    print("Nodes with more than one in-neighbor:", at_least_one_in_neighbor - one_in_neighbor)