__author__ = 'Kami'

from datetime import date, timedelta
from collections import defaultdict
import numpy as np
import re

ONE_DAY = timedelta(1)

if __name__ == "__main__":
    dataset_path = r"complete-dataset"
    out_path = r"advogato_in_neighbors.txt"

    def to_date(text):
        year = 2000 + int(text[:2])
        month = int(text[2:4])
        day = int(text[4:])
        return date(year, month, day)

    in_neighbors = defaultdict(set)

    # pinto,zhp	080903#151#J,###,080911#401#J,###,090228#1453#J

    with open(dataset_path) as file_in:
        for line in file_in:
            _, dst, *certs = re.split("[,\s]", line)
            if len(certs) > 2:
                pass
            for cert in certs:
                if cert and cert != "###":
                    d, n, _ = cert.split("#")
                    cur_date = to_date(d)
                    for _ in range(int(n)):
                        in_neighbors[dst].add(cur_date.toordinal())
                        cur_date += ONE_DAY

    print("Read dataset.")

    with open(out_path, "w") as out_file:
        print("Node_id Range Mean Std", file=out_file)
        while in_neighbors:
            node, certs = in_neighbors.popitem()
            certs = sorted(certs)
            mean = np.mean(certs)
            std = np.std(certs)
            node_range = certs[-1] - certs[0]
            print(node, node_range, mean, std, file=out_file)

    print("End")