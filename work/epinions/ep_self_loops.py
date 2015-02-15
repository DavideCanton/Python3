__author__ = 'Kami'

import re
from collections import Counter

if __name__ == "__main__":
    dataset_path = r"U:\home\kami\Documenti\Ext_Epinions\user_rating.txt"
    pattern = re.compile(r"^(\w+)\s+\1")
    c = Counter()
    with open(dataset_path) as file_in:
        for line in file_in:
            if pattern.match(line):
                c[line.split()[2]] += 1

    print(c)
