# coding=utf-8
__author__ = 'davide'

import collections
import sys
import os
from datetime import datetime

# 0 per tutte le città, altrimenti il numero di città in output
CLASSIFICA_SIZE = 0

def to_date(date_, time_):
    # y-m-d h:m:s
    splitted_date = [int(x) for x in date_.split("-")]
    splitted_time = [int(x) for x in time_.split(":")]
    return datetime(*(splitted_date + splitted_time))

def make_counter(folder):
    count = 0
    counter = collections.Counter()
    for file_name in os.listdir(folder):
        if file_name[0] != "c":
            continue
        with open(os.path.join(folder, file_name)) as file_handle:
            for row in file_handle:
                city, _, date_, time_, *_ = row.split()
                try:
                    to_date(date_, time_)
                    counter[city] += 1
                    if count and count % 1000000 == 0:
                        print("Processed {} tuples...".format(count))
                    count += 1
                except ValueError:
                    pass
    print("Processed {} tuples...".format(count))
    return counter


def write_counter(counter, out_file_name):
    with open(out_file_name, "w") as outfile:
        size = CLASSIFICA_SIZE if CLASSIFICA_SIZE != 0 else len(counter)
        for elem in counter.most_common(size):
            outfile.write("{} {}\n".format(*elem))


def main(folder, out_file_name):
    counter = make_counter(folder)
    print("Writing in {}...".format(out_file_name))
    write_counter(counter, out_file_name)
    print("End!")

if __name__ == "__main__":
    #if len(sys.argv) != 3:
    #    exit("Parametri non validi!")
    folder = "res"#sys.argv[1]
    out_file = "p.txt"#sys.argv[2]
    main(folder, out_file)