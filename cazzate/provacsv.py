__author__ = 'Davide'

import csv


def csv_mapper(csv_reader, mapping=None):
    def id_func(x):
        return x

    if mapping is None:
        mapping = {}

    if hasattr(csv_reader, "fieldnames"):
        # csv_reader returns a dict
        for line in csv_reader:
            yield {name: mapping.setdefault(name, id_func)(value)
                   for name, value in line.items()}
    else:
        # csv_reader returns a sequence
        for line in csv_reader:
            yield [mapping.setdefault(index, id_func)(value)
                   for index, value in enumerate(line)]


if __name__ == "__main__":
    fname = r"D:\prova.csv"

    with open(fname, newline='') as fi:
        reader = csv.DictReader(fi, delimiter=";")
        for line in csv_mapper(reader, {'id': int, 'age': int}):
            print(line)

    with open(fname, newline='') as fi:
        reader = csv.reader(fi, delimiter=";")
        next(reader)
        for line in csv_mapper(reader, {0: int, 2: int}):
            print(line)