__author__ = 'davide'

import pandas as pd

FILE = r"../work/advogato/advogato_in_neighbors.txt"

if __name__ == "__main__":
    data = pd.read_csv(FILE, sep=" ")
    print(data)
    print()
    print(data["Range"].describe())